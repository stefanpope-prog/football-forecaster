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


def test_fit_params_recovers_synthetic_values():
    """Fit on data generated from known (base, home_adv, rho), recover them ±tolerance."""
    import pandas as pd
    from forecaster.model import dixon_coles_grid, fit_params, expected_goals_from_elo

    rng = np.random.default_rng(42)
    true = dict(base_goals=1.3, home_adv=1.25, rho=-0.05, xi=0.001)
    elos = {f"T{i}": 1500 + rng.normal(0, 200) for i in range(10)}
    rows = []
    for _ in range(2000):
        h, a = rng.choice(list(elos.keys()), size=2, replace=False)
        lh, la = expected_goals_from_elo(elos[h], elos[a],
                                         true["base_goals"], true["home_adv"])
        grid = dixon_coles_grid(lh, la, true["rho"], max_goals=10)
        flat = grid.flatten()
        idx = rng.choice(len(flat), p=flat / flat.sum())
        i, j = divmod(idx, grid.shape[1])
        rows.append({
            "date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=int(rng.integers(0, 365))),
            "home": h, "away": a,
            "home_goals": int(i), "away_goals": int(j),
            "neutral": False,
        })
    df = pd.DataFrame(rows)
    fitted = fit_params(df, elos, ref_date=pd.Timestamp("2025-01-01"))
    # Tolerances are wide because the τ-corrected log-likelihood treats τ as a
    # multiplicative factor without re-normalising the joint density (the
    # Dixon-Coles paper's Z(λ_h, λ_a, ρ) ≈ 1). That introduces a small bias in
    # base_goals ↔ home_adv. We're only asserting "rough recovery".
    assert abs(fitted["base_goals"] - true["base_goals"]) < 0.4
    assert abs(fitted["home_adv"] - true["home_adv"]) < 0.4
    assert abs(fitted["rho"] - true["rho"]) < 0.1


def test_predict_fixture_returns_score_grid_and_lambdas():
    import datetime as dt
    from forecaster.model import predict_fixture
    from forecaster.schema import Fixture

    fixture = Fixture(
        fixture_id="2026-06-11-MEX-RSA",
        utc_kickoff=dt.datetime(2026, 6, 11, 18, 0, tzinfo=dt.timezone.utc),
        home="MEX", away="RSA", venue_country="MEX",
        stage="GROUP", status="SCHEDULED",
        actual_home_goals=None, actual_away_goals=None,
    )
    elo = {"MEX": 1825, "RSA": 1620}
    params = {"base_goals": 1.4, "home_adv": 1.3, "rho": -0.1, "xi": 0.001}
    pred = predict_fixture(fixture, elo, params)
    assert pred.score_grid.grid.shape == (9, 9)
    assert pred.lambda_home > pred.lambda_away
    assert abs(pred.score_grid.grid.sum() - 1.0) < 1e-9
