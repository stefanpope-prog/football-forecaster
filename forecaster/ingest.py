"""Ingest fixtures and historical results from public sources."""
from __future__ import annotations

import datetime as dt
import io
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
    "https://raw.githubusercontent.com/openfootball/world-cup.json/master/2026/worldcup.json"
)

HISTORICAL_URL = (
    "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
)

# Country-to-TLA mapping for the historical corpus.
# Source: ISO + FIFA TLA conventions; manually curated for the names that appear
# in martj42/international_results.
_COUNTRY_TLA: dict[str, str] = {
    "Algeria": "ALG", "Argentina": "ARG", "Australia": "AUS", "Austria": "AUT",
    "Belgium": "BEL", "Bosnia & Herzegovina": "BIH",
    "Bosnia and Herzegovina": "BIH", "Brazil": "BRA", "Cameroon": "CMR",
    "Canada": "CAN", "Cape Verde": "CPV", "Chile": "CHI", "Colombia": "COL",
    "Costa Rica": "CRC", "Croatia": "CRO", "Curaçao": "CUW", "Curacao": "CUW",
    "Czech Republic": "CZE", "Czechia": "CZE",
    "DR Congo": "COD", "Congo DR": "COD", "Denmark": "DEN", "Ecuador": "ECU",
    "Egypt": "EGY", "England": "ENG", "France": "FRA", "Germany": "GER",
    "Ghana": "GHA", "Greece": "GRE", "Haiti": "HAI", "Honduras": "HON",
    "Iceland": "ISL", "Iran": "IRN", "Iraq": "IRQ", "Italy": "ITA",
    "Ivory Coast": "CIV", "Japan": "JPN", "Jordan": "JOR", "Mexico": "MEX",
    "Morocco": "MAR", "Netherlands": "NED", "New Zealand": "NZL",
    "Nigeria": "NGA", "North Macedonia": "MKD", "Norway": "NOR", "Panama": "PAN",
    "Paraguay": "PAR", "Peru": "PER", "Poland": "POL", "Portugal": "POR",
    "Qatar": "QAT", "Republic of Ireland": "IRL", "Romania": "ROU",
    "Russia": "RUS", "Saudi Arabia": "KSA", "Scotland": "SCO", "Senegal": "SEN",
    "Serbia": "SRB", "Slovakia": "SVK", "South Africa": "RSA",
    "South Korea": "KOR", "Korea Republic": "KOR", "Spain": "ESP",
    "Sweden": "SWE", "Switzerland": "SUI", "Tunisia": "TUN", "Turkey": "TUR",
    "Ukraine": "UKR", "United States": "USA", "USA": "USA",
    "Uruguay": "URU", "Uzbekistan": "UZB", "Venezuela": "VEN", "Wales": "WAL",
}


# 2026 host cities mapped to host countries — used to normalise OpenFootball's
# flat "ground" string (e.g. "Mexico City") into the venue_country code.
_OPENFOOTBALL_GROUND_COUNTRY: dict[str, str] = {
    # USA (11 host cities)
    "Atlanta": "USA", "Boston": "USA", "Dallas": "USA", "Houston": "USA",
    "Kansas City": "USA", "Los Angeles": "USA", "Miami": "USA", "New York": "USA",
    "New York New Jersey": "USA", "Philadelphia": "USA", "San Francisco": "USA",
    "Seattle": "USA", "East Rutherford": "USA",
    # MEX (3)
    "Mexico City": "MEX", "Guadalajara": "MEX", "Monterrey": "MEX",
    # CAN (2)
    "Toronto": "CAN", "Vancouver": "CAN",
}


def _round_to_stage(round_str: str | None) -> str:
    if not round_str:
        return "GROUP"
    r = round_str.lower()
    if "matchday" in r or "group" in r:
        return "GROUP"
    if "round of 32" in r or "r32" in r:
        return "R32"
    if "round of 16" in r or "r16" in r:
        return "R16"
    if "quarter" in r:
        return "QF"
    if "semi" in r:
        return "SF"
    if "third" in r:
        return "F"
    if "final" in r:
        return "F"
    return "GROUP"


def _strip_tz_suffix(time_str: str) -> str:
    """OpenFootball 'time' field can be 'HH:MM' or 'HH:MM UTC-6'. Drop the suffix."""
    return time_str.split(" ")[0] if time_str else "12:00"


def parse_openfootball(payload: dict[str, Any]) -> list[Fixture]:
    """Parse OpenFootball JSON payload into Fixture objects.

    Schema (post-2025): flat `matches` array, `team1`/`team2` are country
    name strings (or knockout-slot placeholders like "2A", "W74"). We resolve
    names to FIFA TLA codes via `_COUNTRY_TLA`; placeholders are skipped until
    OpenFootball fills them in after the group stage.
    """
    fixtures: list[Fixture] = []
    for match in payload.get("matches", []):
        try:
            fixture = _openfootball_match_to_fixture(match)
        except (KeyError, ValueError, IndexError, TypeError, AttributeError) as e:
            log.warning("Skipping malformed match %r: %s", match, e)
            continue
        if fixture is not None:
            fixtures.append(fixture)
    return fixtures


def _openfootball_match_to_fixture(match: dict[str, Any]) -> Fixture | None:
    date_str = match["date"]
    time_str = _strip_tz_suffix(match.get("time", "12:00"))
    # The published time is the local kickoff; we tag UTC as a best effort.
    # football-data.org supplies real UTC when keyed and supersedes this.
    kickoff = dt.datetime.fromisoformat(f"{date_str}T{time_str}").replace(
        tzinfo=dt.timezone.utc
    )
    team1 = match["team1"]
    team2 = match["team2"]
    if not (isinstance(team1, str) and isinstance(team2, str)):
        return None
    # Skip knockout placeholders ("2A", "W74", etc.) — the home/away aren't
    # yet known. They'll appear once OpenFootball fills them in.
    if team1 not in _COUNTRY_TLA or team2 not in _COUNTRY_TLA:
        return None
    home_code = _COUNTRY_TLA[team1]
    away_code = _COUNTRY_TLA[team2]

    score = match.get("score", {}).get("ft")
    if score is None:
        status = "SCHEDULED"
        ah, aa = None, None
    else:
        status = "FINISHED"
        ah, aa = int(score[0]), int(score[1])

    ground = match.get("ground") or ""
    venue_country = _OPENFOOTBALL_GROUND_COUNTRY.get(ground, "USA")

    return Fixture(
        fixture_id=f"{date_str}-{home_code}-{away_code}",
        utc_kickoff=kickoff,
        home=home_code,
        away=away_code,
        venue_country=venue_country,
        stage=_round_to_stage(match.get("round")),
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
# Best-effort substring match; FD venue strings are not stable schema.
# A mis-tagged venue downgrades home-advantage accuracy by one country —
# we accept that risk vs. maintaining a strict allowlist.
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
    log.debug("Unmapped venue %r — defaulting to USA", venue_str)
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
            # football-data.org uses a richer status vocabulary (TIMED, IN_PLAY,
            # PAUSED, ...). Downstream only cares about FINISHED vs not.
            raw_status = m.get("status", "SCHEDULED")
            status = "FINISHED" if raw_status == "FINISHED" else "SCHEDULED"
            fixtures.append(Fixture(
                fixture_id=f"{kickoff.date().isoformat()}-{home}-{away}",
                utc_kickoff=kickoff,
                home=home,
                away=away,
                venue_country=_venue_country(m.get("venue")),
                stage=_STAGE_MAP.get(m.get("stage", "GROUP_STAGE"), "GROUP"),
                status=status,
                actual_home_goals=ah,
                actual_away_goals=aa,
            ))
        except (KeyError, ValueError, IndexError, TypeError, AttributeError) as e:
            log.warning("Skipping malformed FD match %r: %s", m, e)
    return fixtures


def fetch_football_data(client: httpx.Client) -> list[Fixture]:
    """Live fetch from football-data.org. Requires FOOTBALL_DATA_API_KEY."""
    api_key = os.environ.get("FOOTBALL_DATA_API_KEY")
    if not api_key:
        raise RuntimeError("FOOTBALL_DATA_API_KEY is not set")
    resp = client.get(FOOTBALL_DATA_URL, headers={"X-Auth-Token": api_key})
    resp.raise_for_status()
    return parse_football_data(resp.json())


def fetch_fixtures(client: httpx.Client | None = None) -> list[Fixture]:
    """Primary: football-data.org. Fallback: OpenFootball.

    `client` is an httpx-compatible client; injected for tests. When omitted,
    a default client is opened (and closed) inside this call.
    """
    if client is None:
        with httpx.Client(timeout=30.0) as owned:
            return _fetch_fixtures_with_client(owned)
    return _fetch_fixtures_with_client(client)


def _fetch_fixtures_with_client(client: httpx.Client) -> list[Fixture]:
    api_key = os.environ.get("FOOTBALL_DATA_API_KEY")
    if api_key:
        try:
            fixtures = fetch_football_data(client)
            if fixtures:
                log.info("Fetched %d fixtures from football-data.org", len(fixtures))
                return fixtures
        except (httpx.HTTPError, RuntimeError) as e:
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


def country_to_tla(name: str) -> str:
    """Map a country name to its 3-letter team code; returns name unchanged if unknown."""
    if name in _COUNTRY_TLA:
        return _COUNTRY_TLA[name]
    log.debug("Unknown country name: %s", name)
    return name


def load_historical_csv(path: Path | str | io.StringIO) -> pd.DataFrame:
    """Read martj42 results CSV, normalise columns, return a DataFrame.

    Rows with missing scores (abandoned / forfeit / future) are dropped — the
    Dixon-Coles fitter cannot handle NaN goal counts.
    """
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df["neutral"] = df["neutral"].astype(str).str.lower().isin({"true", "1", "yes"})
    df = df.rename(
        columns={
            "home_team": "home",
            "away_team": "away",
            "home_score": "home_goals",
            "away_score": "away_goals",
        }
    )
    df = df.dropna(subset=["home_goals", "away_goals"]).copy()
    df["home_goals"] = df["home_goals"].astype(int)
    df["away_goals"] = df["away_goals"].astype(int)
    return df[["date", "home", "away", "home_goals", "away_goals", "tournament", "neutral"]]


def fetch_historical_results(
    client: httpx.Client | None = None,
    cache_path: Path | None = None,
) -> pd.DataFrame:
    """Fetch the martj42 historical results CSV (cached for 7 days)."""
    cache_path = cache_path or (config.DATA_DIR / "historical.parquet")
    if cache_path.exists():
        age = dt.datetime.now() - dt.datetime.fromtimestamp(cache_path.stat().st_mtime)
        if age < dt.timedelta(days=7):
            return pd.read_parquet(cache_path)
    if client is not None:
        resp = client.get(HISTORICAL_URL)
        resp.raise_for_status()
        df = load_historical_csv(io.StringIO(resp.text))
    else:
        with httpx.Client(timeout=60.0) as owned:
            resp = owned.get(HISTORICAL_URL)
            resp.raise_for_status()
            df = load_historical_csv(io.StringIO(resp.text))
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cache_path, index=False)
    return df
