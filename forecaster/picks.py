"""adidas Forecaster scoring rule + EV-optimal pick selection."""
from __future__ import annotations

import numpy as np

from forecaster import config
from forecaster.schema import Prediction, ScoreGrid


def score_pick(predicted: tuple[int, int], actual: tuple[int, int]) -> int:
    """adidas Forecaster scoring: 3 outcome + 1 per-team-score + 1 goal diff."""
    p_h, p_a = predicted
    a_h, a_a = actual

    p_sign = (p_h > p_a) - (p_h < p_a)
    a_sign = (a_h > a_a) - (a_h < a_a)
    outcome = config.SCORE_OUTCOME if p_sign == a_sign else 0

    home_match = config.SCORE_PER_TEAM_GOAL if p_h == a_h else 0
    away_match = config.SCORE_PER_TEAM_GOAL if p_a == a_a else 0

    goal_diff = config.SCORE_GOAL_DIFF if (p_h - p_a) == (a_h - a_a) else 0

    return outcome + home_match + away_match + goal_diff


def expected_points(predicted: tuple[int, int], grid: ScoreGrid) -> float:
    """E[points] under the scoreline distribution."""
    n = grid.grid.shape[0]
    ev = 0.0
    for i in range(n):
        for j in range(n):
            p = grid.grid[i, j]
            if p > 0:
                ev += p * score_pick(predicted, (i, j))
    return ev


def optimal_pick(grid: ScoreGrid) -> tuple[tuple[int, int], float]:
    """Return ((home, away), expected_points) for the EV-maximising pick."""
    n = grid.grid.shape[0]
    best = ((0, 0), -1.0)
    for i in range(n):
        for j in range(n):
            ev = expected_points((i, j), grid)
            if ev > best[1]:
                best = ((i, j), ev)
    return best


def top_n_scorelines(
    grid: ScoreGrid, n: int = 4
) -> list[tuple[tuple[int, int], float]]:
    """Top-n most-likely scorelines, descending."""
    flat = grid.grid.flatten()
    idx = np.argsort(flat)[::-1][:n]
    cols = grid.grid.shape[1]
    return [((int(k // cols), int(k % cols)), float(flat[k])) for k in idx]


def enrich_predictions(
    predictions: list[Prediction], top_n: int = 4
) -> list[Prediction]:
    """Fill in `recommended_pick`, `expected_points`, `top_scorelines` for each."""
    out = []
    for p in predictions:
        pick, ev = optimal_pick(p.score_grid)
        out.append(Prediction(
            fixture_id=p.fixture_id,
            score_grid=p.score_grid,
            lambda_home=p.lambda_home,
            lambda_away=p.lambda_away,
            recommended_pick=pick,
            expected_points=ev,
            top_scorelines=top_n_scorelines(p.score_grid, n=top_n),
        ))
    return out
