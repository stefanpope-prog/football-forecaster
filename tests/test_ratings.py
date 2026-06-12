"""Elo rating maintenance."""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import pandas as pd

from forecaster.ratings import (
    expected_score,
    init_elo,
    update_elo_for_match,
    update_elo_from_results,
)


def test_expected_score_symmetric():
    e_a = expected_score(1500, 1500)
    e_b = expected_score(1500, 1500)
    assert abs(e_a - 0.5) < 1e-9
    assert abs(e_a + e_b - 1.0) < 1e-9


def test_expected_score_400_gap_is_10x_odds():
    e_high = expected_score(1900, 1500)
    e_low = expected_score(1500, 1900)
    assert abs(e_high - 10 / 11) < 1e-3
    assert abs(e_low - 1 / 11) < 1e-3


def test_update_after_upset_moves_ratings_strongly():
    a, b = update_elo_for_match(elo_home=1900, elo_away=1500, result="L", k=30)
    assert a < 1900
    assert b > 1500
    assert (1900 - a) > 20


def test_init_elo_returns_team_to_rating_dict():
    seed = init_elo(Path(__file__).parent.parent / "data" / "elo_seed.csv")
    assert "ARG" in seed
    assert seed["ARG"] > seed["RSA"]


def test_update_elo_from_results_processes_in_chronological_order():
    seed = {"ARG": 2000, "RSA": 1600}
    results = pd.DataFrame([
        {"date": dt.date(2026, 6, 11), "home": "ARG", "away": "RSA",
         "home_goals": 2, "away_goals": 0, "neutral": True},
    ])
    updated = update_elo_from_results(seed, results, k=30)
    assert updated["ARG"] > 2000
    assert updated["RSA"] < 1600
