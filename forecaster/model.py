"""Dixon-Coles bivariate Poisson model for football scorelines."""
from __future__ import annotations

import datetime as dt
from typing import Mapping

import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import poisson

from forecaster import config
from forecaster.schema import Fixture, Prediction, ScoreGrid


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
    # τ can drive cells slightly negative when λ × |ρ| > 1; clip before renormalising.
    np.clip(grid, 0.0, None, out=grid)
    return grid / grid.sum()


def _log_likelihood_match(
    home_goals: int,
    away_goals: int,
    lambda_h: float,
    lambda_a: float,
    rho: float,
) -> float:
    """Log P(home_goals, away_goals | λ_h, λ_a, ρ) under Dixon-Coles."""
    log_p = (
        poisson.logpmf(home_goals, lambda_h)
        + poisson.logpmf(away_goals, lambda_a)
    )
    t = tau(home_goals, away_goals, lambda_h, lambda_a, rho)
    if t <= 0:
        return -1e9
    return float(log_p + np.log(t))


def fit_params(
    historical: pd.DataFrame,
    elo: Mapping[str, float],
    ref_date: pd.Timestamp | dt.date | None = None,
    initial: dict[str, float] | None = None,
) -> dict[str, float]:
    """Fit (base_goals, home_adv, rho, xi) by time-decayed maximum likelihood.

    Matches with teams not in `elo` are dropped.
    """
    ref = pd.Timestamp(ref_date) if ref_date else pd.Timestamp.utcnow().normalize()
    df = historical.copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["home"].isin(elo) & df["away"].isin(elo)].copy()
    df["days_ago"] = (ref - df["date"]).dt.days.clip(lower=0)
    df["elo_h"] = df["home"].map(elo)
    df["elo_a"] = df["away"].map(elo)

    init = initial or {"base_goals": 1.4, "home_adv": 1.3, "rho": -0.1, "xi": 0.0019}
    x0 = np.array([init["base_goals"], init["home_adv"], init["rho"], init["xi"]])

    days_ago = df["days_ago"].to_numpy()
    elo_h = df["elo_h"].to_numpy()
    elo_a = df["elo_a"].to_numpy()
    hg = df["home_goals"].to_numpy()
    ag = df["away_goals"].to_numpy()
    neutral = df["neutral"].to_numpy()

    def neg_ll(params: np.ndarray) -> float:
        base_goals, home_adv, rho, xi = params
        if base_goals <= 0 or home_adv <= 0 or xi < 0:
            return 1e9
        weights = np.exp(-xi * days_ago)
        ll = 0.0
        for w, h_elo, a_elo, h, a, n in zip(
            weights, elo_h, elo_a, hg, ag, neutral, strict=False,
        ):
            ha = 1.0 if n else home_adv
            lh = base_goals * (10 ** ((h_elo - a_elo) / config.ELO_SCALE)) * ha
            la = base_goals * (10 ** ((a_elo - h_elo) / config.ELO_SCALE)) / ha
            ll += w * _log_likelihood_match(int(h), int(a), lh, la, rho)
        return -ll

    # L-BFGS-B with bounds keeps the fit out of degenerate corners
    # (e.g. home_adv → ∞ paired with shrinking base_goals).
    result = minimize(
        neg_ll, x0,
        method="L-BFGS-B",
        bounds=[(0.5, 3.0), (0.8, 2.0), (-0.5, 0.5), (0.0, 0.01)],
        options={"maxiter": 2000},
    )
    base_goals, home_adv, rho, xi = result.x
    return {
        "base_goals": float(base_goals),
        "home_adv": float(home_adv),
        "rho": float(rho),
        "xi": float(xi),
    }


def predict_fixture(
    fixture: Fixture,
    elo: Mapping[str, float],
    params: Mapping[str, float],
    max_goals: int = config.GOAL_GRID_MAX,
) -> Prediction:
    """Produce a Dixon-Coles prediction for a single fixture."""
    elo_h = elo.get(fixture.home, 1500.0)
    elo_a = elo.get(fixture.away, 1500.0)
    is_home = fixture.venue_country == fixture.home
    home_adv = params["home_adv"] if is_home else 1.0
    lh, la = expected_goals_from_elo(
        elo_h, elo_a, base_goals=params["base_goals"], home_adv=home_adv
    )
    grid = dixon_coles_grid(lh, la, rho=params["rho"], max_goals=max_goals)
    return Prediction(
        fixture_id=fixture.fixture_id,
        score_grid=ScoreGrid(home=fixture.home, away=fixture.away, grid=grid),
        lambda_home=lh,
        lambda_away=la,
        recommended_pick=(0, 0),
        expected_points=0.0,
        top_scorelines=[],
    )


def predict_all(
    fixtures: list[Fixture],
    elo: Mapping[str, float],
    params: Mapping[str, float],
) -> list[Prediction]:
    """Predict every SCHEDULED fixture."""
    return [predict_fixture(f, elo, params) for f in fixtures if f.status == "SCHEDULED"]
