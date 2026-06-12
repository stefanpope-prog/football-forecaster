"""Backtest harness for sanity-checking the model."""
from __future__ import annotations

from typing import Mapping

import numpy as np
import pandas as pd

from forecaster.model import dixon_coles_grid, expected_goals_from_elo, fit_params
from forecaster.picks import optimal_pick, score_pick
from forecaster.ratings import update_elo_from_results
from forecaster.schema import ScoreGrid


def backtest_brier(
    actuals: list[str], probs: list[tuple[float, float, float]]
) -> float:
    """Multiclass Brier score over W/D/L.

    actuals: list of "W", "D", "L" (home perspective).
    probs: list of (P_W, P_D, P_L).
    """
    targets = {"W": (1, 0, 0), "D": (0, 1, 0), "L": (0, 0, 1)}
    s = 0.0
    for a, p in zip(actuals, probs, strict=True):
        t = targets[a]
        s += sum((pi - ti) ** 2 for pi, ti in zip(p, t, strict=True))
    return s / len(actuals)


def _outcome(home: int, away: int) -> str:
    if home > away:
        return "W"
    if home < away:
        return "L"
    return "D"


def run_backtest(
    history: pd.DataFrame,
    elo_seed: Mapping[str, float],
    holdout_after: pd.Timestamp,
    k: float = 30.0,
) -> dict[str, float]:
    """Re-predict every match after `holdout_after` using only data before it.

    Returns: brier, log_loss, forecaster_points_per_match, n_matches.
    """
    history = history.copy()
    history["date"] = pd.to_datetime(history["date"])
    train = history[history["date"] <= holdout_after]
    test = history[history["date"] > holdout_after].sort_values("date")
    if len(test) == 0:
        return {"brier": float("nan"), "log_loss": float("nan"),
                "forecaster_points_per_match": float("nan"), "n_matches": 0}

    elo = update_elo_from_results(elo_seed, train, k=k)
    params = fit_params(train, elo, ref_date=holdout_after)
    actuals: list[str] = []
    probs: list[tuple[float, float, float]] = []
    points: list[int] = []
    rolling_elo = dict(elo)
    for _, row in test.iterrows():
        h, a = row["home"], row["away"]
        if h not in rolling_elo or a not in rolling_elo:
            continue
        lh, la = expected_goals_from_elo(
            rolling_elo[h], rolling_elo[a],
            base_goals=params["base_goals"],
            home_adv=params["home_adv"] if not row.get("neutral", True) else 1.0,
        )
        grid = dixon_coles_grid(lh, la, rho=params["rho"])
        sg = ScoreGrid(home=h, away=a, grid=grid)
        wdl = (sg.win_prob(), sg.draw_prob(), sg.loss_prob())
        actual_outcome = _outcome(int(row["home_goals"]), int(row["away_goals"]))
        actuals.append(actual_outcome)
        probs.append(wdl)
        pick, _ = optimal_pick(sg)
        points.append(score_pick(pick, (int(row["home_goals"]), int(row["away_goals"]))))
        rolling_elo = update_elo_from_results(
            rolling_elo,
            pd.DataFrame([row]),
            k=k,
        )

    if not actuals:
        return {"brier": float("nan"), "log_loss": float("nan"),
                "forecaster_points_per_match": float("nan"), "n_matches": 0}

    brier = backtest_brier(actuals, probs)
    log_loss = -np.mean([
        np.log(max(p[{"W": 0, "D": 1, "L": 2}[a]], 1e-9))
        for a, p in zip(actuals, probs, strict=True)
    ])
    return {
        "brier": float(brier),
        "log_loss": float(log_loss),
        "forecaster_points_per_match": float(np.mean(points)),
        "n_matches": len(actuals),
    }
