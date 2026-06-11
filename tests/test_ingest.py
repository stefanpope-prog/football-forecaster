"""Ingest module — fixtures from OpenFootball JSON."""
from __future__ import annotations

import json
from pathlib import Path

from forecaster.ingest import (
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
    import json
    from pathlib import Path

    from forecaster.ingest import parse_football_data

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
    import json
    from pathlib import Path

    from forecaster.ingest import fetch_fixtures

    monkeypatch.delenv("FOOTBALL_DATA_API_KEY", raising=False)
    sample = json.loads(
        (Path(__file__).parent / "data" / "openfootball_sample.json").read_text()
    )

    class StubClient:
        def get(self, url):
            class Resp:
                status_code = 200
                def raise_for_status(self): pass
                def json(self_inner): return sample
            return Resp()

    fixtures = fetch_fixtures(client=StubClient())
    assert len(fixtures) == 2
    assert fixtures[0].home == "MEX"
