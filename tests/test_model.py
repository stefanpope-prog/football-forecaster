"""Dixon-Coles math: Poisson grid + low-score correction."""
from __future__ import annotations

import numpy as np

from forecaster.model import (
    dixon_coles_grid,
    expected_goals_from_elo,
    poisson_grid,
    tau,
)


def test_poisson_grid_sums_to_one_with_large_max():
    grid = poisson_grid(lambda_h=1.4, lambda_a=1.0, max_goals=10)
    assert grid.shape == (11, 11)
    assert abs(grid.sum() - 1.0) < 1e-3


def test_tau_reduces_to_one_outside_low_score_cells():
    assert tau(2, 0, 1.4, 1.0, rho=-0.1) == 1.0
    assert tau(0, 2, 1.4, 1.0, rho=-0.1) == 1.0
    assert tau(2, 2, 1.4, 1.0, rho=-0.1) == 1.0


def test_tau_dixon_coles_corrections():
    rho = -0.1
    lh, la = 1.4, 1.0
    assert tau(0, 0, lh, la, rho) == 1 - lh * la * rho
    assert tau(1, 0, lh, la, rho) == 1 + la * rho
    assert tau(0, 1, lh, la, rho) == 1 + lh * rho
    assert tau(1, 1, lh, la, rho) == 1 - rho


def test_dixon_coles_grid_normalised():
    grid = dixon_coles_grid(lambda_h=1.4, lambda_a=1.0, rho=-0.1, max_goals=8)
    assert abs(grid.sum() - 1.0) < 1e-9
    assert grid.shape == (9, 9)


def test_expected_goals_from_elo_symmetric_at_equal_ratings():
    lh, la = expected_goals_from_elo(elo_h=1800, elo_a=1800, base_goals=1.3,
                                     home_adv=1.0)
    assert abs(lh - la) < 1e-9
    assert abs(lh - 1.3) < 1e-9


def test_expected_goals_from_elo_favours_higher_rated():
    lh, la = expected_goals_from_elo(elo_h=2000, elo_a=1600, base_goals=1.3,
                                     home_adv=1.0)
    assert lh > la
    assert lh > 1.3
