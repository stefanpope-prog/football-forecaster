"""Dixon-Coles bivariate Poisson model for football scorelines."""
from __future__ import annotations

import numpy as np
from scipy.stats import poisson

from forecaster import config


def expected_goals_from_elo(
    elo_h: float,
    elo_a: float,
    base_goals: float,
    home_adv: float,
    scale: float = config.ELO_SCALE,
) -> tuple[float, float]:
    """Convert Elo ratings into expected goals for each side.

    home_adv == 1 is a true neutral venue: λ_h × λ_a == base². For home_adv > 1,
    λ_h is scaled up and λ_a scaled down by the same factor.
    """
    elo_diff = elo_h - elo_a
    lh = base_goals * (10 ** (elo_diff / scale)) * home_adv
    la = base_goals * (10 ** (-elo_diff / scale)) / home_adv
    return float(lh), float(la)


def poisson_grid(lambda_h: float, lambda_a: float, max_goals: int = 8) -> np.ndarray:
    """Independent-Poisson scoreline grid, shape (max_goals+1, max_goals+1)."""
    home_pmf = poisson.pmf(np.arange(max_goals + 1), lambda_h)
    away_pmf = poisson.pmf(np.arange(max_goals + 1), lambda_a)
    return np.outer(home_pmf, away_pmf)


def tau(
    home_goals: int,
    away_goals: int,
    lambda_h: float,
    lambda_a: float,
    rho: float,
) -> float:
    """Dixon-Coles low-score correction. Returns 1.0 outside the four low cells."""
    if home_goals == 0 and away_goals == 0:
        return 1.0 - lambda_h * lambda_a * rho
    if home_goals == 0 and away_goals == 1:
        return 1.0 + lambda_h * rho
    if home_goals == 1 and away_goals == 0:
        return 1.0 + lambda_a * rho
    if home_goals == 1 and away_goals == 1:
        return 1.0 - rho
    return 1.0


def dixon_coles_grid(
    lambda_h: float,
    lambda_a: float,
    rho: float,
    max_goals: int = 8,
) -> np.ndarray:
    """Dixon-Coles-corrected scoreline grid, normalised to sum to 1."""
    grid = poisson_grid(lambda_h, lambda_a, max_goals)
    grid[0, 0] *= tau(0, 0, lambda_h, lambda_a, rho)
    grid[0, 1] *= tau(0, 1, lambda_h, lambda_a, rho)
    grid[1, 0] *= tau(1, 0, lambda_h, lambda_a, rho)
    grid[1, 1] *= tau(1, 1, lambda_h, lambda_a, rho)
    return grid / grid.sum()
