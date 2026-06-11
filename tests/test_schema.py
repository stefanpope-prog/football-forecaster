"""Schema dataclasses round-trip through dicts."""
from __future__ import annotations

import datetime as dt

import numpy as np

from forecaster.schema import Fixture, Prediction, ScoreGrid


def test_fixture_round_trip():
    f = Fixture(
        fixture_id="2026-06-11-MEX-RSA",
        utc_kickoff=dt.datetime(2026, 6, 11, 18, 0, tzinfo=dt.timezone.utc),
        home="MEX",
        away="RSA",
        venue_country="MEX",
        stage="GROUP",
        status="SCHEDULED",
        actual_home_goals=None,
        actual_away_goals=None,
    )
    assert Fixture.from_dict(f.to_dict()) == f


def test_score_grid_normalized():
    grid = np.zeros((3, 3))
    grid[1, 0] = 0.5
    grid[0, 1] = 0.5
    sg = ScoreGrid(home="MEX", away="RSA", grid=grid)
    assert abs(sg.win_prob() + sg.draw_prob() + sg.loss_prob() - 1.0) < 1e-9
    assert sg.win_prob() == 0.5
    assert sg.draw_prob() == 0.0


def test_prediction_serialises_grid():
    grid = np.full((2, 2), 0.25)
    sg = ScoreGrid(home="MEX", away="RSA", grid=grid)
    p = Prediction(
        fixture_id="2026-06-11-MEX-RSA",
        score_grid=sg,
        lambda_home=1.4,
        lambda_away=1.0,
        recommended_pick=(2, 0),
        expected_points=2.7,
        top_scorelines=[((1, 0), 0.25), ((0, 0), 0.25)],
    )
    d = p.to_dict()
    assert d["recommended_pick"] == [2, 0]
    assert d["score_grid"]["grid"] == [[0.25, 0.25], [0.25, 0.25]]
