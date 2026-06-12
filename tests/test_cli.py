"""End-to-end pipeline smoke test."""
from __future__ import annotations

import datetime as dt
from unittest.mock import patch

import pandas as pd

from forecaster.cli import run_pipeline
from forecaster.schema import Fixture


def _fake_fixtures():
    return [
        Fixture(
            fixture_id="2026-06-11-MEX-RSA",
            utc_kickoff=dt.datetime(2026, 6, 11, 18, 0, tzinfo=dt.timezone.utc),
            home="MEX", away="RSA", venue_country="MEX",
            stage="GROUP", status="SCHEDULED",
            actual_home_goals=None, actual_away_goals=None,
        ),
    ]


def _fake_history():
    rows = []
    for i in range(50):
        rows.append({
            "date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=i),
            "home": "MEX" if i % 2 == 0 else "RSA",
            "away": "RSA" if i % 2 == 0 else "MEX",
            "home_goals": 2 if i % 2 == 0 else 0,
            "away_goals": 0 if i % 2 == 0 else 1,
            "neutral": True,
            "tournament": "Friendly",
        })
    return pd.DataFrame(rows)


def test_run_pipeline_produces_index_html(tmp_data_dir):
    from forecaster import config
    seed = {"MEX": 1825, "RSA": 1620}

    with (
        patch("forecaster.cli.fetch_fixtures", return_value=_fake_fixtures()),
        patch("forecaster.cli.fetch_historical_results", return_value=_fake_history()),
        patch("forecaster.cli.init_elo", return_value=seed),
    ):
        run_pipeline(force=True)

    assert (config.DOCS_DIR / "index.html").exists()
    assert (config.DOCS_DIR / "prompt-pack.md").exists()
    assert (config.DOCS_API_DIR / "2026-06-11-MEX-RSA.json").exists()
