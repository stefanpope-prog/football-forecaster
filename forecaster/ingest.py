"""Ingest fixtures and historical results from public sources."""
from __future__ import annotations

import datetime as dt
import io
import json
import logging
from pathlib import Path
from typing import Any

import httpx
import pandas as pd

from forecaster import config
from forecaster.schema import Fixture

log = logging.getLogger(__name__)

# OpenFootball publishes world-cup-2026 in this repo.
OPENFOOTBALL_URL = (
    "https://raw.githubusercontent.com/openfootball/world-cup.json/master/2026/wc.json"
)


def parse_openfootball(payload: dict[str, Any]) -> list[Fixture]:
    """Parse OpenFootball JSON payload into Fixture objects."""
    fixtures: list[Fixture] = []
    for round_ in payload.get("rounds", []):
        for match in round_.get("matches", []):
            try:
                fixtures.append(_match_to_fixture(match))
            except (KeyError, ValueError) as e:
                log.warning("Skipping malformed match %r: %s", match, e)
    return fixtures


def _match_to_fixture(match: dict[str, Any]) -> Fixture:
    date_str = match["date"]
    time_str = match.get("time", "12:00")
    kickoff = dt.datetime.fromisoformat(f"{date_str}T{time_str}").replace(
        tzinfo=dt.timezone.utc
    )
    home_code = match["team1"]["code"]
    away_code = match["team2"]["code"]
    score = match.get("score", {}).get("ft")  # [home, away] when finished
    if score is None:
        status = "SCHEDULED"
        ah, aa = None, None
    else:
        status = "FINISHED"
        ah, aa = int(score[0]), int(score[1])
    return Fixture(
        fixture_id=f"{date_str}-{home_code}-{away_code}",
        utc_kickoff=kickoff,
        home=home_code,
        away=away_code,
        venue_country=match.get("venue_country", "USA"),  # default to USA host
        stage=match.get("stage", "GROUP"),
        status=status,
        actual_home_goals=ah,
        actual_away_goals=aa,
    )


def fetch_openfootball(client: httpx.Client | None = None) -> list[Fixture]:
    """Live fetch from OpenFootball. Used by the pipeline."""
    client = client or httpx.Client(timeout=30.0)
    resp = client.get(OPENFOOTBALL_URL)
    resp.raise_for_status()
    return parse_openfootball(resp.json())


def write_fixtures_parquet(fixtures: list[Fixture], path: Path | None = None) -> Path:
    """Persist fixtures as parquet for downstream modules."""
    path = path or (config.DATA_DIR / "fixtures.parquet")
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [f.to_dict() for f in fixtures]
    df = pd.DataFrame(rows)
    df.to_parquet(path, index=False)
    return path


def read_fixtures_parquet(path: Path | None = None) -> list[Fixture]:
    """Load fixtures back from parquet."""
    path = path or (config.DATA_DIR / "fixtures.parquet")
    df = pd.read_parquet(path)
    fixtures: list[Fixture] = []
    for row in df.to_dict(orient="records"):
        # Parquet round-trips missing ints as NaN — restore them to None and
        # coerce real values back to int (pandas may widen them to float).
        for key in ("actual_home_goals", "actual_away_goals"):
            value = row.get(key)
            if value is None or (isinstance(value, float) and pd.isna(value)):
                row[key] = None
            else:
                row[key] = int(value)
        fixtures.append(Fixture.from_dict(row))
    return fixtures
