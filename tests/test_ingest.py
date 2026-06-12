"""Ingest module — fixtures from OpenFootball JSON."""
from __future__ import annotations

import json
from pathlib import Path

from forecaster.ingest import (
    fetch_fixtures,
    parse_football_data,
    parse_openfootball,
    read_fixtures_parquet,
    write_fixtures_parquet,
)


def test_parse_openfootball_extracts_fixtures():
    sample = json.loads(
        (Path(__file__).parent / "data" / "openfootball_sample.json").read_text()
    )
    fixtures = parse_openfootball(sample)

    assert len(fixtures) == 2

    f1, f2 = fixtures
    assert f1.fixture_id == "2026-06-11-MEX-RSA"
    assert f1.home == "MEX"
    assert f1.away == "RSA"
    assert f1.venue_country == "MEX"
    assert f1.status == "FINISHED"
    assert f1.actual_home_goals == 1
    assert f1.actual_away_goals == 0
    assert f1.utc_kickoff.hour == 20

    assert f2.fixture_id == "2026-06-12-ARG-FRA"
    assert f2.status == "SCHEDULED"
    assert f2.actual_home_goals is None


def test_fixtures_parquet_round_trip(tmp_data_dir):
    sample = json.loads(
        (Path(__file__).parent / "data" / "openfootball_sample.json").read_text()
    )
    fixtures = parse_openfootball(sample)

    path = write_fixtures_parquet(fixtures, path=tmp_data_dir / "fixtures.parquet")
    assert path.exists()

    loaded = read_fixtures_parquet(path)
    assert loaded == fixtures


def test_parse_football_data_extracts_fixtures():
    sample = json.loads(
        (Path(__file__).parent / "data" / "football_data_sample.json").read_text()
    )
    fixtures = parse_football_data(sample)

    assert len(fixtures) == 2
    f1, f2 = fixtures
    assert f1.fixture_id == "2026-06-11-MEX-RSA"
    assert f1.status == "FINISHED"
    assert f1.actual_home_goals == 1
    assert f1.venue_country == "MEX"           # parsed from venue string
    assert f2.venue_country == "USA"
    assert f2.utc_kickoff.hour == 18


def test_fetch_fixtures_falls_back_when_no_api_key(monkeypatch):
    """If FOOTBALL_DATA_API_KEY missing, use OpenFootball."""
    monkeypatch.delenv("FOOTBALL_DATA_API_KEY", raising=False)
    sample = json.loads(
        (Path(__file__).parent / "data" / "openfootball_sample.json").read_text()
    )

    class StubClient:
        def get(self, url, headers=None):
            class Resp:
                status_code = 200
                def raise_for_status(self): pass
                def json(self_inner): return sample
            return Resp()

    fixtures = fetch_fixtures(client=StubClient())
    assert len(fixtures) == 2
    assert fixtures[0].home == "MEX"


def test_fetch_fixtures_uses_football_data_when_keyed(monkeypatch):
    """If FOOTBALL_DATA_API_KEY set, primary FD path is used."""
    monkeypatch.setenv("FOOTBALL_DATA_API_KEY", "test-key")
    sample = json.loads(
        (Path(__file__).parent / "data" / "football_data_sample.json").read_text()
    )

    class FdStubClient:
        captured_headers = None

        def get(self, url, headers=None):
            FdStubClient.captured_headers = headers
            class Resp:
                status_code = 200
                def raise_for_status(self): pass
                def json(self_inner): return sample
            return Resp()

    fixtures = fetch_fixtures(client=FdStubClient())
    assert len(fixtures) == 2
    assert fixtures[0].fixture_id == "2026-06-11-MEX-RSA"
    assert FdStubClient.captured_headers == {"X-Auth-Token": "test-key"}


def test_fetch_fixtures_falls_back_on_empty_football_data(monkeypatch):
    """If FD returns an empty match list, fall through to OpenFootball."""
    monkeypatch.setenv("FOOTBALL_DATA_API_KEY", "test-key")
    of_sample = json.loads(
        (Path(__file__).parent / "data" / "openfootball_sample.json").read_text()
    )

    class EmptyThenOfStubClient:
        def __init__(self):
            self.call = 0

        def get(self, url, headers=None):
            self.call += 1
            class Resp:
                status_code = 200
                def raise_for_status(self_inner): pass
                def json(self_inner):
                    # First call (FD): empty matches; second (OF): real sample.
                    if self.call == 1:
                        return {"matches": []}
                    return of_sample
            return Resp()

    fixtures = fetch_fixtures(client=EmptyThenOfStubClient())
    assert len(fixtures) == 2
    assert fixtures[0].home == "MEX"


def test_fetch_fixtures_falls_back_on_football_data_http_error(monkeypatch):
    """If FD raises an HTTPError, fall through to OpenFootball."""
    import httpx

    monkeypatch.setenv("FOOTBALL_DATA_API_KEY", "test-key")
    of_sample = json.loads(
        (Path(__file__).parent / "data" / "openfootball_sample.json").read_text()
    )

    class FailingThenOfStubClient:
        def __init__(self):
            self.call = 0

        def get(self, url, headers=None):
            self.call += 1
            class Resp:
                status_code = 200
                def raise_for_status(self_inner):
                    if self.call == 1:
                        raise httpx.HTTPError("boom")

                def json(self_inner): return of_sample
            return Resp()

    fixtures = fetch_fixtures(client=FailingThenOfStubClient())
    assert len(fixtures) == 2
    assert fixtures[0].home == "MEX"


def test_load_historical_csv_normalizes_columns(tmp_path):
    from forecaster.ingest import load_historical_csv

    src = tmp_path / "results.csv"
    src.write_text(
        "date,home_team,away_team,home_score,away_score,tournament,city,country,neutral\n"
        "2024-06-15,Germany,Scotland,5,1,UEFA Euro,Munich,Germany,FALSE\n"
        "2024-06-22,Spain,Italy,1,0,UEFA Euro,Gelsenkirchen,Germany,TRUE\n"
    )
    df = load_historical_csv(src)

    assert list(df.columns) == [
        "date", "home", "away", "home_goals", "away_goals", "tournament", "neutral"
    ]
    assert len(df) == 2
    assert df.iloc[0]["home"] == "Germany"
    assert df.iloc[0]["home_goals"] == 5
    assert bool(df.iloc[1]["neutral"]) is True
    assert bool(df.iloc[0]["neutral"]) is False


def test_country_to_tla_resolves_known_names():
    from forecaster.ingest import country_to_tla

    assert country_to_tla("Germany") == "GER"
    assert country_to_tla("United States") == "USA"
    assert country_to_tla("South Korea") == "KOR"
    assert country_to_tla("Mexico") == "MEX"
