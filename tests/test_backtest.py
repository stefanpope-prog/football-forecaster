"""Backtest harness."""
from __future__ import annotations

import pandas as pd

from forecaster.backtest import backtest_brier, run_backtest


def test_brier_is_zero_for_perfect_predictions():
    actuals = ["W", "L", "D"]
    probs = [(1, 0, 0), (0, 0, 1), (0, 1, 0)]
    assert backtest_brier(actuals, probs) == 0.0


def test_brier_increases_for_worse_predictions():
    actuals = ["W"]
    perfect = backtest_brier(actuals, [(1, 0, 0)])
    uniform = backtest_brier(actuals, [(1/3, 1/3, 1/3)])
    assert uniform > perfect


def test_run_backtest_reports_forecaster_points():
    rows = []
    for i in range(80):
        rows.append({
            "date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=i),
            "home": "MEX" if i % 2 == 0 else "RSA",
            "away": "RSA" if i % 2 == 0 else "MEX",
            "home_goals": 2 if i % 2 == 0 else 0,
            "away_goals": 0 if i % 2 == 0 else 1,
            "neutral": True,
            "tournament": "Friendly",
        })
    history = pd.DataFrame(rows)
    elo = {"MEX": 1800, "RSA": 1600}

    metrics = run_backtest(history, elo, holdout_after=pd.Timestamp("2024-02-15"))
    assert "brier" in metrics
    assert "log_loss" in metrics
    assert "forecaster_points_per_match" in metrics
    assert metrics["n_matches"] >= 1
