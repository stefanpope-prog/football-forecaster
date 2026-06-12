"""Publish module — JSON, HTML, prompt-pack."""
from __future__ import annotations

import datetime as dt
import json

import numpy as np

from forecaster.publish import write_per_fixture_json
from forecaster.schema import Fixture, Prediction, ScoreGrid


def _make_pred(fixture_id: str = "2026-06-11-MEX-RSA") -> Prediction:
    grid = np.zeros((3, 3))
    grid[1, 0] = 0.5
    grid[0, 0] = 0.3
    grid[1, 1] = 0.2
    sg = ScoreGrid(home="MEX", away="RSA", grid=grid)
    return Prediction(
        fixture_id=fixture_id, score_grid=sg,
        lambda_home=1.4, lambda_away=0.7,
        recommended_pick=(1, 0), expected_points=4.5,
        top_scorelines=[((1, 0), 0.5), ((0, 0), 0.3), ((1, 1), 0.2)],
    )


def _make_fixture(fixture_id: str = "2026-06-11-MEX-RSA") -> Fixture:
    return Fixture(
        fixture_id=fixture_id,
        utc_kickoff=dt.datetime(2026, 6, 11, 18, 0, tzinfo=dt.timezone.utc),
        home="MEX", away="RSA", venue_country="MEX",
        stage="GROUP", status="SCHEDULED",
        actual_home_goals=None, actual_away_goals=None,
    )


def test_write_per_fixture_json_creates_file_per_fixture(tmp_data_dir):
    fixtures = [_make_fixture("a"), _make_fixture("b")]
    preds = [_make_pred("a"), _make_pred("b")]
    rationale = {"a": "test rationale a", "b": "test rationale b"}

    paths = write_per_fixture_json(fixtures, preds, rationale)
    assert len(paths) == 2

    payload = json.loads(paths[0].read_text())
    assert payload["fixture_id"] == "a"
    assert payload["recommended_pick"] == [1, 0]
    assert "rationale" in payload
    assert payload["w_d_l"]["draw"] >= 0
