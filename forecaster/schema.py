"""Dataclasses for fixtures, predictions, and scoreline grids."""
from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from typing import Any

import numpy as np


@dataclass(frozen=True)
class Fixture:
    fixture_id: str                      # stable: "YYYY-MM-DD-HOME-AWAY"
    utc_kickoff: dt.datetime
    home: str                            # 3-letter country code
    away: str
    venue_country: str                   # 3-letter; for home-adv adjustment
    stage: str                           # "GROUP" | "R32" | "R16" | "QF" | "SF" | "F"
    status: str                          # "SCHEDULED" | "LIVE" | "FINISHED"
    actual_home_goals: int | None
    actual_away_goals: int | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "utc_kickoff": self.utc_kickoff.isoformat(),
            "home": self.home,
            "away": self.away,
            "venue_country": self.venue_country,
            "stage": self.stage,
            "status": self.status,
            "actual_home_goals": self.actual_home_goals,
            "actual_away_goals": self.actual_away_goals,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Fixture":
        return cls(
            fixture_id=d["fixture_id"],
            utc_kickoff=dt.datetime.fromisoformat(d["utc_kickoff"]),
            home=d["home"],
            away=d["away"],
            venue_country=d["venue_country"],
            stage=d["stage"],
            status=d["status"],
            actual_home_goals=d["actual_home_goals"],
            actual_away_goals=d["actual_away_goals"],
        )


@dataclass
class ScoreGrid:
    """Probability matrix where grid[i, j] = P(home scores i, away scores j)."""
    home: str
    away: str
    grid: np.ndarray                     # shape (N, N)

    def win_prob(self) -> float:
        return float(np.tril(self.grid, k=-1).sum())  # home > away → below diag

    def draw_prob(self) -> float:
        return float(np.trace(self.grid))

    def loss_prob(self) -> float:
        return float(np.triu(self.grid, k=1).sum())   # home < away → above diag

    def home_marginal(self) -> np.ndarray:
        return self.grid.sum(axis=1)

    def away_marginal(self) -> np.ndarray:
        return self.grid.sum(axis=0)

    def to_dict(self) -> dict[str, Any]:
        return {"home": self.home, "away": self.away, "grid": self.grid.tolist()}


@dataclass
class Prediction:
    fixture_id: str
    score_grid: ScoreGrid
    lambda_home: float
    lambda_away: float
    recommended_pick: tuple[int, int]
    expected_points: float
    top_scorelines: list[tuple[tuple[int, int], float]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "fixture_id": self.fixture_id,
            "score_grid": self.score_grid.to_dict(),
            "lambda_home": self.lambda_home,
            "lambda_away": self.lambda_away,
            "recommended_pick": list(self.recommended_pick),
            "expected_points": self.expected_points,
            "top_scorelines": [
                {"score": list(s), "prob": p} for s, p in self.top_scorelines
            ],
        }
