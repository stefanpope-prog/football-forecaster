"""Form summary - deterministic per-fixture rationale from data."""
from __future__ import annotations

import datetime as dt

import numpy as np
import pandas as pd

from forecaster.form import build_form_summary, last_n_results, summarise_all
from forecaster.schema import Fixture, Prediction, ScoreGrid


def _fix(fid="2026-06-11-MEX-RSA", home="MEX", away="RSA"):
    return Fixture(
        fixture_id=fid,
        utc_kickoff=dt.datetime(2026, 6, 11, 18, 0, tzinfo=dt.timezone.utc),
        home=home, away=away, venue_country="MEX",
        stage="GROUP", status="SCHEDULED",
        actual_home_goals=None, actual_away_goals=None,
    )


def _pred(fid="2026-06-11-MEX-RSA", home="MEX", away="RSA"):
    grid = np.zeros((3, 3))
    grid[1, 0] = 0.5; grid[0, 0] = 0.3; grid[1, 1] = 0.2
    return Prediction(
        fixture_id=fid,
        score_grid=ScoreGrid(home=home, away=away, grid=grid),
        lambda_home=1.4, lambda_away=0.7,
        recommended_pick=(1, 0), expected_points=4.5,
        top_scorelines=[((1, 0), 0.5), ((0, 0), 0.3), ((1, 1), 0.2)],
    )


def _history():
    rows = []
    base = pd.Timestamp("2026-03-01")
    mex_results = [("MEX", "USA", 2, 1), ("CAN", "MEX", 0, 3),
                   ("MEX", "BRA", 1, 1), ("ARG", "MEX", 2, 0),
                   ("MEX", "JPN", 1, 0)]
    for i, (h, a, hg, ag) in enumerate(mex_results):
        rows.append({"date": base + pd.Timedelta(days=i*7),
                     "home": h, "away": a,
                     "home_goals": hg, "away_goals": ag,
                     "neutral": True, "tournament": "Friendly"})
    rsa_results = [("RSA", "GHA", 0, 2), ("NGA", "RSA", 3, 1),
                   ("RSA", "MAR", 0, 0), ("EGY", "RSA", 1, 0),
                   ("RSA", "SEN", 0, 1)]
    for i, (h, a, hg, ag) in enumerate(rsa_results):
        rows.append({"date": base + pd.Timedelta(days=i*7),
                     "home": h, "away": a,
                     "home_goals": hg, "away_goals": ag,
                     "neutral": True, "tournament": "Friendly"})
    return pd.DataFrame(rows)


def test_last_n_results_filters_and_orders():
    history = _history()
    mex = last_n_results(history, "MEX", n=5)
    assert len(mex) == 5
    assert mex.iloc[0]["date"] >= mex.iloc[-1]["date"]


def test_build_form_summary_mentions_form_and_elo():
    text = build_form_summary(
        _fix(), _pred(),
        elo={"MEX": 1825, "RSA": 1620},
        history=_history(),
    )
    assert "MEX" in text and "RSA" in text
    assert any(w in text for w in ("favourite", "edge", "evenly matched"))
    assert any(w in text for w in ("win", "draw", "loss"))


def test_summarise_all_returns_dict_keyed_by_fixture_id():
    out = summarise_all(
        [_fix()], [_pred()],
        elo={"MEX": 1825, "RSA": 1620},
        history=_history(),
    )
    assert "2026-06-11-MEX-RSA" in out
    assert len(out["2026-06-11-MEX-RSA"]) > 20
