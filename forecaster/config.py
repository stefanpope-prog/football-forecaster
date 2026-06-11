"""Configuration: paths, constants, and tournament metadata."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DOCS_DIR = ROOT / "docs"
DOCS_API_DIR = DOCS_DIR / "api"
TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

# Tournament window — anything outside this is ignored when filtering fixtures.
TOURNAMENT_START = "2026-06-11"
TOURNAMENT_END = "2026-07-19"

# Host countries get a small home-advantage bump even at "neutral" WC venues.
HOST_COUNTRIES = {"USA", "CAN", "MEX"}

# Dixon-Coles fitting defaults.
ELO_SCALE = 400.0           # standard Elo: 400-pt gap = 10x odds
GOAL_GRID_MAX = 8           # 8x8 grid covers >99.9% of scorelines

# adidas Forecaster scoring rule (per match).
SCORE_OUTCOME = 3
SCORE_PER_TEAM_GOAL = 1     # +1 each for home/away exact goals
SCORE_GOAL_DIFF = 1
SCORE_MAX = 6               # 3 + 1 + 1 + 1


def ensure_dirs() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    DOCS_DIR.mkdir(exist_ok=True)
    DOCS_API_DIR.mkdir(exist_ok=True)
