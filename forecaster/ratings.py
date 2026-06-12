"""Elo rating computation and maintenance."""
from __future__ import annotations

from pathlib import Path
from typing import Literal

import pandas as pd

from forecaster import config


def expected_score(elo_a: float, elo_b: float, scale: float = config.ELO_SCALE) -> float:
    """Standard Elo expected score for player A vs B."""
    return 1.0 / (1.0 + 10 ** ((elo_b - elo_a) / scale))


def update_elo_for_match(
    elo_home: float,
    elo_away: float,
    result: Literal["W", "D", "L"],
    k: float = 30.0,
    home_field: float = 100.0,
    neutral: bool = True,
) -> tuple[float, float]:
    """Return (new_home_elo, new_away_elo) after one match.

    `result` is from the home team's perspective. `home_field` is added to the
    home rating only when computing the expected score for non-neutral matches;
    it is never persisted to the rating itself.
    """
    home_eff = elo_home + (0.0 if neutral else home_field)
    e_home = expected_score(home_eff, elo_away)
    s_home = {"W": 1.0, "D": 0.5, "L": 0.0}[result]
    delta = k * (s_home - e_home)
    return elo_home + delta, elo_away - delta


def init_elo(seed_path: Path | str | None = None) -> dict[str, float]:
    """Load the seed CSV (team, elo) into a dict."""
    seed_path = seed_path or (config.DATA_DIR / "elo_seed.csv")
    df = pd.read_csv(seed_path)
    return {row["team"]: float(row["elo"]) for _, row in df.iterrows()}


def update_elo_from_results(
    seed: dict[str, float],
    results: pd.DataFrame,
    k: float = 30.0,
) -> dict[str, float]:
    """Apply a chronologically-sorted set of results to the seed ratings.

    Teams not in the seed start at 1500. Returns a *new* dict.
    """
    elo = dict(seed)
    results = results.sort_values("date")
    for _, row in results.iterrows():
        h, a = row["home"], row["away"]
        if h not in elo:
            elo[h] = 1500.0
        if a not in elo:
            elo[a] = 1500.0
        if row["home_goals"] > row["away_goals"]:
            result: Literal["W", "D", "L"] = "W"
        elif row["home_goals"] < row["away_goals"]:
            result = "L"
        else:
            result = "D"
        new_h, new_a = update_elo_for_match(
            elo[h], elo[a], result, k=k, neutral=bool(row.get("neutral", True))
        )
        elo[h], elo[a] = new_h, new_a
    return elo


def write_elo_parquet(elo: dict[str, float], path: Path | None = None) -> Path:
    path = path or (config.DATA_DIR / "elo.parquet")
    path.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(
        [{"team": t, "elo": r} for t, r in sorted(elo.items())]
    )
    df.to_parquet(path, index=False)
    return path


def read_elo_parquet(path: Path | None = None) -> dict[str, float]:
    path = path or (config.DATA_DIR / "elo.parquet")
    df = pd.read_parquet(path)
    return {row["team"]: float(row["elo"]) for _, row in df.iterrows()}
