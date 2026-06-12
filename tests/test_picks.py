"""Scoring rule + EV-optimal pick selection."""
from __future__ import annotations

import numpy as np

from forecaster.picks import (
    enrich_predictions,
    expected_points,
    optimal_pick,
    score_pick,
    top_n_scorelines,
)
from forecaster.schema import Prediction, ScoreGrid


def test_score_pick_perfect():
    # 2:1 vs 2:1 → outcome (3) + home (1) + away (1) + gd (1) = 6
    assert score_pick((2, 1), (2, 1)) == 6


def test_score_pick_correct_outcome_only():
    # 2:0 vs 1:0 → outcome ✓ (3) + away ✓ (1, both 0). Total 4.
    assert score_pick((2, 0), (1, 0)) == 4


def test_score_pick_outcome_plus_goal_diff_no_team_score_match():
    # 2:0 vs 3:1 → outcome ✓ (3) + gd ✓ (1). Total 4.
    assert score_pick((2, 0), (3, 1)) == 4


def test_score_pick_wrong_outcome():
    assert score_pick((2, 0), (0, 1)) == 0


def test_score_pick_draw_correct_outcome():
    # 1:1 vs 2:2 → outcome ✓ (3) + gd ✓ (1). Total 4.
    assert score_pick((1, 1), (2, 2)) == 4


def test_expected_points_uniform_grid():
    grid = np.full((3, 3), 1 / 9)
    sg = ScoreGrid(home="A", away="B", grid=grid)
    ep = expected_points((1, 1), sg)
    assert 0 < ep < 6


def test_optimal_pick_picks_highest_ev_cell():
    grid = np.zeros((4, 4))
    grid[1, 0] = 0.7
    grid[0, 0] = 0.1
    grid[2, 0] = 0.1
    grid[1, 1] = 0.1
    sg = ScoreGrid(home="A", away="B", grid=grid)
    pick, ev = optimal_pick(sg)
    assert pick == (1, 0)
    assert ev > 4


def test_top_n_scorelines_returns_descending():
    grid = np.zeros((3, 3))
    grid[1, 1] = 0.4
    grid[1, 0] = 0.3
    grid[0, 1] = 0.2
    grid[2, 2] = 0.1
    sg = ScoreGrid(home="A", away="B", grid=grid)
    top = top_n_scorelines(sg, n=3)
    assert top == [((1, 1), 0.4), ((1, 0), 0.3), ((0, 1), 0.2)]


def test_enrich_predictions_fills_pick_and_top_scorelines():
    grid = np.zeros((3, 3))
    grid[1, 0] = 0.5
    grid[0, 0] = 0.3
    grid[1, 1] = 0.2
    sg = ScoreGrid(home="A", away="B", grid=grid)
    p = Prediction(
        fixture_id="x", score_grid=sg, lambda_home=1.0, lambda_away=0.5,
        recommended_pick=(0, 0), expected_points=0.0, top_scorelines=[],
    )
    [enriched] = enrich_predictions([p])
    assert enriched.recommended_pick != (0, 0) or enriched.expected_points > 0
    assert len(enriched.top_scorelines) == 4
