"""Ingest fixtures and historical results from public sources."""
from __future__ import annotations

import datetime as dt
import logging
import os
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
                fixtures.append(_openfootball_match_to_fixture(match))
            except (KeyError, ValueError, IndexError, TypeError) as e:
                log.warning("Skipping malformed match %r: %s", match, e)
    return fixtures


def _openfootball_match_to_fixture(match: dict[str, Any]) -> Fixture:
    date_str = match["date"]
    time_str = match.get("time", "12:00")
    # OpenFootball "time" is naive; we tag it UTC as a best effort.
    # football-data.org (Task 4) supplies real UTC and supersedes this when keyed.
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
        venue_country=match.get("venue_country", "USA"),  # 2026 hosts USA/CAN/MEX
        stage=match.get("stage", "GROUP"),
        status=status,
        actual_home_goals=ah,
        actual_away_goals=aa,
    )


def fetch_openfootball(client: httpx.Client | None = None) -> list[Fixture]:
    """Live fetch from OpenFootball. Used by the pipeline."""
    if client is not None:
        resp = client.get(OPENFOOTBALL_URL)
        resp.raise_for_status()
        return parse_openfootball(resp.json())
    with httpx.Client(timeout=30.0) as owned:
        resp = owned.get(OPENFOOTBALL_URL)
        resp.raise_for_status()
        return parse_openfootball(resp.json())


FOOTBALL_DATA_URL = "https://api.football-data.org/v4/competitions/WC/matches"

# Minimal venue-string -> country mapping for the 16 host cities.
_HOST_VENUE_COUNTRIES = {
    # USA
    "MetLife": "USA", "AT&T Stadium": "USA", "Arrowhead": "USA",
    "Lincoln Financial": "USA", "Levi's": "USA", "NRG": "USA",
    "Hard Rock": "USA", "Lumen": "USA", "Gillette": "USA", "SoFi": "USA",
    "Mercedes-Benz": "USA", "Estadio Azteca": "MEX", "Akron": "MEX",
    "BBVA": "MEX", "BMO": "CAN", "Vancouver": "CAN",
}


def _venue_country(venue_str: str | None) -> str:
    if not venue_str:
        return "USA"
    for needle, code in _HOST_VENUE_COUNTRIES.items():
        if needle.lower() in venue_str.lower():
            return code
    return "USA"


_STAGE_MAP = {
    "GROUP_STAGE": "GROUP",
    "LAST_16": "R16",
    "QUARTER_FINALS": "QF",
    "SEMI_FINALS": "SF",
    "FINAL": "F",
    "THIRD_PLACE": "F",
}


def parse_football_data(payload: dict[str, Any]) -> list[Fixture]:
    """Parse a football-data.org /matches payload into Fixture objects."""
    fixtures: list[Fixture] = []
    for m in payload.get("matches", []):
        try:
            kickoff = dt.datetime.fromisoformat(m["utcDate"].replace("Z", "+00:00"))
            home = m["homeTeam"]["tla"]
            away = m["awayTeam"]["tla"]
            ft = m.get("score", {}).get("fullTime", {})
            ah = ft.get("home")
            aa = ft.get("away")
            fixtures.append(Fixture(
                fixture_id=f"{kickoff.date().isoformat()}-{home}-{away}",
                utc_kickoff=kickoff,
                home=home,
                away=away,
                venue_country=_venue_country(m.get("venue")),
                stage=_STAGE_MAP.get(m.get("stage", "GROUP_STAGE"), "GROUP"),
                status=m.get("status", "SCHEDULED"),
                actual_home_goals=ah if ah is not None else None,
                actual_away_goals=aa if aa is not None else None,
            ))
        except (KeyError, ValueError) as e:
            log.warning("Skipping malformed FD match %r: %s", m, e)
    return fixtures


def fetch_football_data(client: httpx.Client) -> list[Fixture]:
    """Live fetch from football-data.org. Requires FOOTBALL_DATA_API_KEY."""
    api_key = os.environ["FOOTBALL_DATA_API_KEY"]
    resp = client.get(FOOTBALL_DATA_URL, headers={"X-Auth-Token": api_key})
    resp.raise_for_status()
    return parse_football_data(resp.json())


def fetch_fixtures(client: Any | None = None) -> list[Fixture]:
    """Primary: football-data.org. Fallback: OpenFootball.

    `client` is an httpx-compatible client; injected for tests. When omitted,
    a default client is opened (and closed) inside this call.
    """
    if client is None:
        with httpx.Client(timeout=30.0) as owned:
            return _fetch_fixtures_with_client(owned)
    return _fetch_fixtures_with_client(client)


def _fetch_fixtures_with_client(client: Any) -> list[Fixture]:
    api_key = os.environ.get("FOOTBALL_DATA_API_KEY")
    if api_key:
        try:
            fixtures = fetch_football_data(client)
            if fixtures:
                log.info("Fetched %d fixtures from football-data.org", len(fixtures))
                return fixtures
        except (httpx.HTTPError, KeyError) as e:
            log.warning("football-data.org failed (%s); falling back to OpenFootball", e)
    return fetch_openfootball(client)


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
