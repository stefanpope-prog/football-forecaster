# Football Forecaster v1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a working 2026 World Cup forecaster before group-stage kickoff: predictions per match, mobile-friendly static dashboard on GitHub Pages, paste-into-Claude-Chat prompt pack, refreshed by GitHub Actions on a free-tier budget.

**Architecture:** Python pipeline (ingest → ratings → model → picks → rationale → publish) writes parquet to `data/` and HTML/markdown to `docs/`. Dixon-Coles bivariate Poisson with Elo-derived strengths produces an 8×8 scoreline grid per fixture; an EV optimizer over the adidas Forecaster scoring rule (3 outcome + 1 per-team-score + 1 goal diff = 6 max) picks the recommended scoreline. GitHub Pages serves the HTML; GitHub Actions runs the pipeline hourly on match days. Out of scope for v1: tournament/Final-Four Monte Carlo (separate v1.5 plan).

**Tech Stack:** Python 3.12, `httpx`, `pandas` + `pyarrow`, `numpy`, `scipy`, `jinja2`, `anthropic`, `pytest`, GitHub Actions, GitHub Pages.

**Parallelization opportunities (subagent-driven runs only):**
- Tasks 3, 4, 5 (ingest variants + historical corpus) can run in parallel after Task 2.
- Tasks 11, 12, 13 (HTML dashboard, prompt pack, per-fixture JSON) can run in parallel after Task 10.
- Task 16 (backtest harness) can run in parallel with Tasks 11–14 after Task 10.

---

## Pre-flight checks (engineer reads this once, before starting)

- **Working directory:** `/Users/pabstste/Library/CloudStorage/OneDrive-adidas/Documents/Workspace/Football Forecaster`
- **Git already initialized** with one commit (the design spec).
- **Sandbox quirk:** writes to `.git` may require `dangerouslyDisableSandbox: true` because the project lives in OneDrive. Prefer running git operations from a terminal Bash tool with that flag when sandbox blocks.
- **Required secrets** (added later in Task 15, but get them ready):
  - `FOOTBALL_DATA_API_KEY` — free signup at https://www.football-data.org/client/register
  - `ANTHROPIC_API_KEY` — workspace key for Claude Sonnet
- **Stefan's GitHub username** is required for the public repo URL — ask before Task 15.

---

## Task 1: Project scaffold

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `README.md`
- Create: `forecaster/__init__.py`
- Create: `forecaster/config.py`
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Write `pyproject.toml`**

```toml
[project]
name = "forecaster"
version = "0.1.0"
description = "2026 World Cup match forecaster"
requires-python = ">=3.12"
dependencies = [
    "httpx>=0.27",
    "pandas>=2.2",
    "pyarrow>=16",
    "numpy>=2.0",
    "scipy>=1.13",
    "jinja2>=3.1",
    "anthropic>=0.40",
    "pydantic>=2.7",
]

[project.optional-dependencies]
dev = [
    "pytest>=8",
    "pytest-cov>=5",
    "ruff>=0.5",
]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers"

[tool.ruff]
line-length = 100
target-version = "py312"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["."]
include = ["forecaster*"]
```

- [ ] **Step 2: Write `.gitignore`**

```
.venv/
__pycache__/
*.pyc
.pytest_cache/
.coverage
htmlcov/
.DS_Store
*.egg-info/
.env
```

- [ ] **Step 3: Write `README.md`**

```markdown
# Football Forecaster

2026 FIFA World Cup match forecaster. Dixon-Coles bivariate Poisson with Elo-derived strengths. Static dashboard on GitHub Pages, paste-into-Claude-Chat prompt pack for mobile.

See `docs/superpowers/specs/2026-06-11-football-forecaster-design.md` for the design.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
export FOOTBALL_DATA_API_KEY=...      # free at football-data.org
export ANTHROPIC_API_KEY=...
python -m forecaster run
```

Outputs land in `docs/`. Run `pytest` for tests.
```

- [ ] **Step 4: Write `forecaster/__init__.py`**

```python
"""Football Forecaster v1."""

__version__ = "0.1.0"
```

- [ ] **Step 5: Write `forecaster/config.py`**

```python
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
```

- [ ] **Step 6: Write `tests/__init__.py` (empty) and `tests/conftest.py`**

```python
"""Shared pytest fixtures."""
from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def tmp_data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect DATA_DIR to a temp dir for tests."""
    from forecaster import config

    monkeypatch.setattr(config, "DATA_DIR", tmp_path / "data")
    monkeypatch.setattr(config, "DOCS_DIR", tmp_path / "docs")
    monkeypatch.setattr(config, "DOCS_API_DIR", tmp_path / "docs" / "api")
    config.ensure_dirs()
    return tmp_path / "data"
```

- [ ] **Step 7: Verify the package imports**

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
python -c "import forecaster; print(forecaster.__version__)"
```

Expected: `0.1.0`

- [ ] **Step 8: Commit**

```bash
git add pyproject.toml .gitignore README.md forecaster/__init__.py forecaster/config.py tests/__init__.py tests/conftest.py
git commit -m "feat: project scaffold (pyproject, config, package layout)"
```

---

## Task 2: Schema (dataclasses)

**Files:**
- Create: `forecaster/schema.py`
- Create: `tests/test_schema.py`

- [ ] **Step 1: Write the failing test**

`tests/test_schema.py`:

```python
"""Schema dataclasses round-trip through dicts."""
from __future__ import annotations

import datetime as dt

import numpy as np

from forecaster.schema import Fixture, Prediction, ScoreGrid


def test_fixture_round_trip():
    f = Fixture(
        fixture_id="2026-06-11-MEX-RSA",
        utc_kickoff=dt.datetime(2026, 6, 11, 18, 0, tzinfo=dt.timezone.utc),
        home="MEX",
        away="RSA",
        venue_country="MEX",
        stage="GROUP",
        status="SCHEDULED",
        actual_home_goals=None,
        actual_away_goals=None,
    )
    assert Fixture.from_dict(f.to_dict()) == f


def test_score_grid_normalized():
    grid = np.zeros((3, 3))
    grid[1, 0] = 0.5
    grid[0, 1] = 0.5
    sg = ScoreGrid(home="MEX", away="RSA", grid=grid)
    assert abs(sg.win_prob() + sg.draw_prob() + sg.loss_prob() - 1.0) < 1e-9
    assert sg.win_prob() == 0.5
    assert sg.draw_prob() == 0.0


def test_prediction_serialises_grid():
    grid = np.full((2, 2), 0.25)
    sg = ScoreGrid(home="MEX", away="RSA", grid=grid)
    p = Prediction(
        fixture_id="2026-06-11-MEX-RSA",
        score_grid=sg,
        lambda_home=1.4,
        lambda_away=1.0,
        recommended_pick=(2, 0),
        expected_points=2.7,
        top_scorelines=[((1, 0), 0.25), ((0, 0), 0.25)],
    )
    d = p.to_dict()
    assert d["recommended_pick"] == [2, 0]
    assert d["score_grid"]["grid"] == [[0.25, 0.25], [0.25, 0.25]]
```

- [ ] **Step 2: Run test to verify it fails**

```bash
pytest tests/test_schema.py -v
```

Expected: FAIL with `ImportError: cannot import name 'Fixture' from 'forecaster.schema'`

- [ ] **Step 3: Implement `forecaster/schema.py`**

```python
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
```

Note: `tril` is below-diagonal (home > away → home win); we put home goals on the row axis so cell `[i, j]` reads as "home i, away j", and "home wins" lives below the diagonal.

- [ ] **Step 4: Run test to verify it passes**

```bash
pytest tests/test_schema.py -v
```

Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add forecaster/schema.py tests/test_schema.py
git commit -m "feat: dataclasses for Fixture, ScoreGrid, Prediction"
```

---

## Task 3: Ingest fixtures from OpenFootball (no auth)

OpenFootball publishes World Cup fixtures as plain JSON on GitHub. Use this as the primary source; the football-data.org integration in Task 4 layers on top of it.

**Files:**
- Create: `forecaster/ingest.py`
- Create: `tests/test_ingest.py`
- Create: `tests/data/openfootball_sample.json`

- [ ] **Step 1: Vendor a small sample of OpenFootball JSON for tests**

Save to `tests/data/openfootball_sample.json`:

```json
{
  "name": "World Cup 2026",
  "rounds": [
    {
      "name": "Matchday 1",
      "matches": [
        {
          "date": "2026-06-11",
          "time": "20:00",
          "team1": { "name": "Mexico", "code": "MEX" },
          "team2": { "name": "South Africa", "code": "RSA" },
          "score": { "ft": [1, 0] },
          "stage": "GROUP",
          "venue_country": "MEX"
        },
        {
          "date": "2026-06-12",
          "time": "18:00",
          "team1": { "name": "Argentina", "code": "ARG" },
          "team2": { "name": "France", "code": "FRA" },
          "stage": "GROUP",
          "venue_country": "USA"
        }
      ]
    }
  ]
}
```

- [ ] **Step 2: Write the failing test**

`tests/test_ingest.py`:

```python
"""Ingest module — fixtures from OpenFootball JSON."""
from __future__ import annotations

import json
from pathlib import Path

from forecaster.ingest import parse_openfootball


def test_parse_openfootball_extracts_fixtures():
    sample = json.loads(
        (Path(__file__).parent / "data" / "openfootball_sample.json").read_text()
    )
    fixtures = parse_openfootball(sample)

    assert len(fixtures) == 2

    f1, f2 = fixtures
    assert f1.fixture_id == "2026-06-11-MEX-RSA"
    assert f1.home == "MEX"
    assert f1.away == "RSA"
    assert f1.venue_country == "MEX"
    assert f1.status == "FINISHED"
    assert f1.actual_home_goals == 1
    assert f1.actual_away_goals == 0
    assert f1.utc_kickoff.hour == 20

    assert f2.fixture_id == "2026-06-12-ARG-FRA"
    assert f2.status == "SCHEDULED"
    assert f2.actual_home_goals is None
```

- [ ] **Step 3: Run test to verify it fails**

```bash
pytest tests/test_ingest.py -v
```

Expected: FAIL — `parse_openfootball` does not exist.

- [ ] **Step 4: Implement `forecaster/ingest.py` (parse + fetch)**

```python
"""Ingest fixtures and historical results from public sources."""
from __future__ import annotations

import datetime as dt
import io
import json
import logging
from pathlib import Path
from typing import Any

import httpx
import pandas as pd

from forecaster import config
from forecaster.schema import Fixture

log = logging.getLogger(__name__)

# OpenFootball publishes world-cup-2026 in this repo.
OPENFOOTBALL_URL = (
    "https://raw.githubusercontent.com/openfootball/world-cup.json/master/2026/wc.json"
)


def parse_openfootball(payload: dict[str, Any]) -> list[Fixture]:
    """Parse OpenFootball JSON payload into Fixture objects."""
    fixtures: list[Fixture] = []
    for round_ in payload.get("rounds", []):
        for match in round_.get("matches", []):
            try:
                fixtures.append(_match_to_fixture(match))
            except (KeyError, ValueError) as e:
                log.warning("Skipping malformed match %r: %s", match, e)
    return fixtures


def _match_to_fixture(match: dict[str, Any]) -> Fixture:
    date_str = match["date"]
    time_str = match.get("time", "12:00")
    kickoff = dt.datetime.fromisoformat(f"{date_str}T{time_str}").replace(
        tzinfo=dt.timezone.utc
    )
    home_code = match["team1"]["code"]
    away_code = match["team2"]["code"]
    score = match.get("score", {}).get("ft")  # [home, away] when finished
    if score is None:
        status = "SCHEDULED"
        ah, aa = None, None
    else:
        status = "FINISHED"
        ah, aa = int(score[0]), int(score[1])
    return Fixture(
        fixture_id=f"{date_str}-{home_code}-{away_code}",
        utc_kickoff=kickoff,
        home=home_code,
        away=away_code,
        venue_country=match.get("venue_country", "USA"),  # default to USA host
        stage=match.get("stage", "GROUP"),
        status=status,
        actual_home_goals=ah,
        actual_away_goals=aa,
    )


def fetch_openfootball(client: httpx.Client | None = None) -> list[Fixture]:
    """Live fetch from OpenFootball. Used by the pipeline."""
    client = client or httpx.Client(timeout=30.0)
    resp = client.get(OPENFOOTBALL_URL)
    resp.raise_for_status()
    return parse_openfootball(resp.json())


def write_fixtures_parquet(fixtures: list[Fixture], path: Path | None = None) -> Path:
    """Persist fixtures as parquet for downstream modules."""
    path = path or (config.DATA_DIR / "fixtures.parquet")
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = [f.to_dict() for f in fixtures]
    df = pd.DataFrame(rows)
    df.to_parquet(path, index=False)
    return path


def read_fixtures_parquet(path: Path | None = None) -> list[Fixture]:
    """Load fixtures back from parquet."""
    path = path or (config.DATA_DIR / "fixtures.parquet")
    df = pd.read_parquet(path)
    return [Fixture.from_dict(row) for row in df.to_dict(orient="records")]
```

- [ ] **Step 5: Run test to verify it passes**

```bash
pytest tests/test_ingest.py -v
```

Expected: 1 passed.

- [ ] **Step 6: Add a round-trip parquet test**

Append to `tests/test_ingest.py`:

```python
def test_fixtures_parquet_round_trip(tmp_data_dir, monkeypatch):
    import json
    from pathlib import Path
    from forecaster.ingest import (
        parse_openfootball,
        read_fixtures_parquet,
        write_fixtures_parquet,
    )

    sample = json.loads(
        (Path(__file__).parent / "data" / "openfootball_sample.json").read_text()
    )
    fixtures = parse_openfootball(sample)

    path = write_fixtures_parquet(fixtures, path=tmp_data_dir / "fixtures.parquet")
    assert path.exists()

    loaded = read_fixtures_parquet(path)
    assert loaded == fixtures
```

- [ ] **Step 7: Run test**

```bash
pytest tests/test_ingest.py -v
```

Expected: 2 passed.

- [ ] **Step 8: Commit**

```bash
git add forecaster/ingest.py tests/test_ingest.py tests/data/openfootball_sample.json
git commit -m "feat(ingest): OpenFootball fixture parser + parquet round-trip"
```

---

## Task 4: Ingest fixtures from football-data.org with OpenFootball fallback

football-data.org provides better metadata (precise kickoff times, real-time score updates). Use it as the primary source when `FOOTBALL_DATA_API_KEY` is set; fall back to OpenFootball otherwise.

**Files:**
- Modify: `forecaster/ingest.py` (add `fetch_football_data` + `fetch_fixtures`)
- Modify: `tests/test_ingest.py`
- Create: `tests/data/football_data_sample.json`

- [ ] **Step 1: Vendor a small football-data.org sample**

`tests/data/football_data_sample.json`:

```json
{
  "matches": [
    {
      "id": 999001,
      "utcDate": "2026-06-11T20:00:00Z",
      "status": "FINISHED",
      "stage": "GROUP_STAGE",
      "homeTeam": { "tla": "MEX", "name": "Mexico" },
      "awayTeam": { "tla": "RSA", "name": "South Africa" },
      "score": { "fullTime": { "home": 1, "away": 0 } },
      "venue": "Estadio Azteca, Mexico City"
    },
    {
      "id": 999002,
      "utcDate": "2026-06-12T18:00:00Z",
      "status": "SCHEDULED",
      "stage": "GROUP_STAGE",
      "homeTeam": { "tla": "ARG", "name": "Argentina" },
      "awayTeam": { "tla": "FRA", "name": "France" },
      "score": { "fullTime": { "home": null, "away": null } },
      "venue": "MetLife Stadium, New Jersey"
    }
  ]
}
```

- [ ] **Step 2: Write the failing test**

Append to `tests/test_ingest.py`:

```python
def test_parse_football_data_extracts_fixtures():
    import json
    from pathlib import Path

    from forecaster.ingest import parse_football_data

    sample = json.loads(
        (Path(__file__).parent / "data" / "football_data_sample.json").read_text()
    )
    fixtures = parse_football_data(sample)

    assert len(fixtures) == 2
    f1, f2 = fixtures
    assert f1.fixture_id == "2026-06-11-MEX-RSA"
    assert f1.status == "FINISHED"
    assert f1.actual_home_goals == 1
    assert f1.venue_country == "MEX"           # parsed from venue string
    assert f2.venue_country == "USA"
    assert f2.utc_kickoff.hour == 18


def test_fetch_fixtures_falls_back_when_no_api_key(monkeypatch):
    """If FOOTBALL_DATA_API_KEY missing, use OpenFootball."""
    import json
    from pathlib import Path

    from forecaster.ingest import fetch_fixtures

    monkeypatch.delenv("FOOTBALL_DATA_API_KEY", raising=False)
    sample = json.loads(
        (Path(__file__).parent / "data" / "openfootball_sample.json").read_text()
    )

    class StubClient:
        def get(self, url):
            class Resp:
                status_code = 200
                def raise_for_status(self): pass
                def json(self_inner): return sample
            return Resp()

    fixtures = fetch_fixtures(client=StubClient())
    assert len(fixtures) == 2
    assert fixtures[0].home == "MEX"
```

- [ ] **Step 3: Run tests to verify they fail**

```bash
pytest tests/test_ingest.py -v
```

Expected: 2 failures (functions don't exist).

- [ ] **Step 4: Implement `parse_football_data` and `fetch_fixtures` in `forecaster/ingest.py`**

Add to `forecaster/ingest.py`:

```python
import os

FOOTBALL_DATA_URL = "https://api.football-data.org/v4/competitions/WC/matches"

# Minimal venue-string → country mapping for the 16 host cities.
_HOST_VENUE_COUNTRIES = {
    # USA
    "MetLife": "USA", "AT&T Stadium": "USA", "Arrowhead": "USA",
    "Lincoln Financial": "USA", "Levi's": "USA", "NRG": "USA",
    "Hard Rock": "USA", "Lumen": "USA", "Gillette": "USA", "SoFi": "USA",
    "Mercedes-Benz": "USA", "Estadio Azteca": "MEX", "Akron": "MEX",
    "BBVA": "MEX", "BMO": "CAN", "Vancouver": "CAN",
}


def _venue_country(venue_str: str | None) -> str:
    if not venue_str:
        return "USA"
    for needle, code in _HOST_VENUE_COUNTRIES.items():
        if needle.lower() in venue_str.lower():
            return code
    return "USA"


_STAGE_MAP = {
    "GROUP_STAGE": "GROUP",
    "LAST_16": "R16",
    "QUARTER_FINALS": "QF",
    "SEMI_FINALS": "SF",
    "FINAL": "F",
    "THIRD_PLACE": "F",
}


def parse_football_data(payload: dict[str, Any]) -> list[Fixture]:
    fixtures: list[Fixture] = []
    for m in payload.get("matches", []):
        try:
            kickoff = dt.datetime.fromisoformat(m["utcDate"].replace("Z", "+00:00"))
            home = m["homeTeam"]["tla"]
            away = m["awayTeam"]["tla"]
            ft = m.get("score", {}).get("fullTime", {})
            ah = ft.get("home")
            aa = ft.get("away")
            fixtures.append(Fixture(
                fixture_id=f"{kickoff.date().isoformat()}-{home}-{away}",
                utc_kickoff=kickoff,
                home=home,
                away=away,
                venue_country=_venue_country(m.get("venue")),
                stage=_STAGE_MAP.get(m.get("stage", "GROUP_STAGE"), "GROUP"),
                status=m.get("status", "SCHEDULED"),
                actual_home_goals=ah if ah is not None else None,
                actual_away_goals=aa if aa is not None else None,
            ))
        except (KeyError, ValueError) as e:
            log.warning("Skipping malformed FD match %r: %s", m, e)
    return fixtures


def fetch_football_data(client: httpx.Client) -> list[Fixture]:
    api_key = os.environ["FOOTBALL_DATA_API_KEY"]
    resp = client.get(FOOTBALL_DATA_URL, headers={"X-Auth-Token": api_key})
    resp.raise_for_status()
    return parse_football_data(resp.json())


def fetch_fixtures(client: Any | None = None) -> list[Fixture]:
    """Primary: football-data.org. Fallback: OpenFootball.

    `client` is an httpx-compatible client; injected for tests.
    """
    client = client or httpx.Client(timeout=30.0)
    api_key = os.environ.get("FOOTBALL_DATA_API_KEY")
    if api_key:
        try:
            fixtures = fetch_football_data(client)
            if fixtures:
                log.info("Fetched %d fixtures from football-data.org", len(fixtures))
                return fixtures
        except (httpx.HTTPError, KeyError) as e:
            log.warning("football-data.org failed (%s); falling back to OpenFootball", e)
    return fetch_openfootball(client)
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_ingest.py -v
```

Expected: 4 passed.

- [ ] **Step 6: Commit**

```bash
git add forecaster/ingest.py tests/test_ingest.py tests/data/football_data_sample.json
git commit -m "feat(ingest): football-data.org primary + OpenFootball fallback"
```

---

## Task 5: Ingest historical international results

Source: Mart Jürisoo's "International football results 1872–present" (Kaggle). The dataset is republished as a stable CSV; we vendor it once at repo-init time and refresh weekly. ~45k matches, ~3 MB compressed.

**Files:**
- Modify: `forecaster/ingest.py` (add `fetch_historical_results`)
- Modify: `tests/test_ingest.py`
- Create: `tests/data/historical_sample.csv`

- [ ] **Step 1: Vendor a 5-row CSV sample**

`tests/data/historical_sample.csv`:

```csv
date,home_team,away_team,home_score,away_score,tournament,city,country,neutral
2024-06-15,Germany,Scotland,5,1,UEFA Euro,Munich,Germany,FALSE
2024-06-16,Argentina,Canada,2,0,Copa America,Atlanta,United States,TRUE
2024-06-22,Spain,Italy,1,0,UEFA Euro,Gelsenkirchen,Germany,TRUE
2024-07-14,Spain,England,2,1,UEFA Euro,Berlin,Germany,TRUE
2024-07-14,Argentina,Colombia,1,0,Copa America,Miami,United States,TRUE
```

- [ ] **Step 2: Write the failing test**

Append to `tests/test_ingest.py`:

```python
def test_load_historical_csv_normalizes_columns(tmp_path):
    from forecaster.ingest import load_historical_csv

    src = tmp_path / "results.csv"
    src.write_text(
        "date,home_team,away_team,home_score,away_score,tournament,city,country,neutral\n"
        "2024-06-15,Germany,Scotland,5,1,UEFA Euro,Munich,Germany,FALSE\n"
        "2024-06-22,Spain,Italy,1,0,UEFA Euro,Gelsenkirchen,Germany,TRUE\n"
    )
    df = load_historical_csv(src)

    assert list(df.columns) == [
        "date", "home", "away", "home_goals", "away_goals", "tournament", "neutral"
    ]
    assert len(df) == 2
    assert df.iloc[0]["home"] == "Germany"
    assert df.iloc[0]["home_goals"] == 5
    assert df.iloc[1]["neutral"] is True


def test_country_to_tla_resolves_known_names():
    from forecaster.ingest import country_to_tla

    assert country_to_tla("Germany") == "GER"
    assert country_to_tla("United States") == "USA"
    assert country_to_tla("South Korea") == "KOR"
    assert country_to_tla("Mexico") == "MEX"
```

- [ ] **Step 3: Run tests, expect failure**

```bash
pytest tests/test_ingest.py -k "historical or country_to_tla" -v
```

Expected: 2 failures.

- [ ] **Step 4: Implement `load_historical_csv` and `country_to_tla`**

Append to `forecaster/ingest.py`:

```python
HISTORICAL_URL = (
    "https://raw.githubusercontent.com/martj42/international_results/master/results.csv"
)

# Country-to-TLA mapping for the historical corpus.
# Source: ISO + FIFA TLA conventions; manually curated for the names that appear
# in martj42/international_results.
_COUNTRY_TLA: dict[str, str] = {
    "Argentina": "ARG", "Australia": "AUS", "Austria": "AUT", "Belgium": "BEL",
    "Brazil": "BRA", "Cameroon": "CMR", "Canada": "CAN", "Chile": "CHI",
    "Colombia": "COL", "Costa Rica": "CRC", "Croatia": "CRO", "Czech Republic": "CZE",
    "Czechia": "CZE", "Denmark": "DEN", "Ecuador": "ECU", "Egypt": "EGY",
    "England": "ENG", "France": "FRA", "Germany": "GER", "Ghana": "GHA",
    "Greece": "GRE", "Honduras": "HON", "Iceland": "ISL", "Iran": "IRN",
    "Italy": "ITA", "Ivory Coast": "CIV", "Japan": "JPN", "Mexico": "MEX",
    "Morocco": "MAR", "Netherlands": "NED", "Nigeria": "NGA", "North Macedonia": "MKD",
    "Norway": "NOR", "Panama": "PAN", "Paraguay": "PAR", "Peru": "PER",
    "Poland": "POL", "Portugal": "POR", "Qatar": "QAT", "Republic of Ireland": "IRL",
    "Romania": "ROU", "Russia": "RUS", "Saudi Arabia": "KSA", "Scotland": "SCO",
    "Senegal": "SEN", "Serbia": "SRB", "Slovakia": "SVK", "South Africa": "RSA",
    "South Korea": "KOR", "Spain": "ESP", "Sweden": "SWE", "Switzerland": "SUI",
    "Tunisia": "TUN", "Turkey": "TUR", "Ukraine": "UKR", "United States": "USA",
    "Uruguay": "URU", "Venezuela": "VEN", "Wales": "WAL",
}


def country_to_tla(name: str) -> str:
    """Map a country name to its 3-letter team code; returns name unchanged if unknown."""
    if name in _COUNTRY_TLA:
        return _COUNTRY_TLA[name]
    log.debug("Unknown country name: %s", name)
    return name


def load_historical_csv(path: Path | str) -> pd.DataFrame:
    """Read martj42 results CSV, normalise columns, return a DataFrame."""
    df = pd.read_csv(path)
    df["date"] = pd.to_datetime(df["date"])
    df["home"] = df["home_team"].map(country_to_tla)
    df["away"] = df["away_team"].map(country_to_tla)
    df["neutral"] = df["neutral"].astype(str).str.lower().isin({"true", "1", "yes"})
    df = df.rename(columns={"home_score": "home_goals", "away_score": "away_goals"})
    return df[["date", "home", "away", "home_goals", "away_goals", "tournament", "neutral"]]


def fetch_historical_results(
    client: httpx.Client | None = None,
    cache_path: Path | None = None,
) -> pd.DataFrame:
    """Fetch the martj42 historical results CSV (cached for 7 days)."""
    cache_path = cache_path or (config.DATA_DIR / "historical.parquet")
    if cache_path.exists():
        age = dt.datetime.now() - dt.datetime.fromtimestamp(cache_path.stat().st_mtime)
        if age < dt.timedelta(days=7):
            return pd.read_parquet(cache_path)
    client = client or httpx.Client(timeout=60.0)
    resp = client.get(HISTORICAL_URL)
    resp.raise_for_status()
    df = load_historical_csv(io.StringIO(resp.text))
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(cache_path, index=False)
    return df
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_ingest.py -v
```

Expected: 6 passed.

- [ ] **Step 6: Commit**

```bash
git add forecaster/ingest.py tests/test_ingest.py tests/data/historical_sample.csv
git commit -m "feat(ingest): historical international results loader"
```

---

## Task 6: Ratings (Elo init + update)

Standard chess Elo with K=30. Initialized from a snapshot of eloratings.net once per tournament; we maintain it ourselves as WC matches finish, so day-N predictions reflect days 1..N-1 results.

**Files:**
- Create: `forecaster/ratings.py`
- Create: `tests/test_ratings.py`
- Create: `data/elo_seed.csv` (initial Elo per team — manually curated)

- [ ] **Step 1: Create the Elo seed file**

`data/elo_seed.csv`:

```csv
team,elo
ARG,2143
FRA,2076
BRA,2065
ENG,2018
ESP,2017
NED,1989
POR,1976
GER,1970
CRO,1925
ITA,1923
BEL,1910
COL,1898
URU,1879
SUI,1869
USA,1838
DEN,1830
MEX,1825
JPN,1813
KOR,1801
SEN,1797
MAR,1791
CAN,1781
AUS,1772
ECU,1769
SRB,1760
POL,1742
SCO,1738
WAL,1721
TUN,1700
NGA,1697
IRN,1690
EGY,1685
CMR,1679
CIV,1672
GHA,1659
QAT,1648
KSA,1633
RSA,1620
PAR,1614
PAN,1605
CRC,1592
HON,1565
NOR,1550
TUR,1545
SVK,1530
ROU,1518
GRE,1510
HUN,1500
```

(These are approximate eloratings.net values; the exact numbers don't matter for correctness — they get refit each pipeline run.)

- [ ] **Step 2: Write the failing test**

`tests/test_ratings.py`:

```python
"""Elo rating maintenance."""
from __future__ import annotations

import datetime as dt
from pathlib import Path

import pandas as pd

from forecaster.ratings import (
    expected_score,
    init_elo,
    update_elo_for_match,
    update_elo_from_results,
)


def test_expected_score_symmetric():
    e_a = expected_score(1500, 1500)
    e_b = expected_score(1500, 1500)
    assert abs(e_a - 0.5) < 1e-9
    assert abs(e_a + e_b - 1.0) < 1e-9


def test_expected_score_400_gap_is_10x_odds():
    e_high = expected_score(1900, 1500)
    e_low = expected_score(1500, 1900)
    assert abs(e_high - 10/11) < 1e-3      # 10:1 odds → 10/11 win probability
    assert abs(e_low - 1/11) < 1e-3


def test_update_after_upset_moves_ratings_strongly():
    a, b = update_elo_for_match(elo_home=1900, elo_away=1500, result="L", k=30)
    assert a < 1900   # underdog won, favourite drops
    assert b > 1500
    assert (1900 - a) > 20   # not a tiny update — we lost when expected to win


def test_init_elo_returns_team_to_rating_dict():
    seed = init_elo(Path(__file__).parent.parent / "data" / "elo_seed.csv")
    assert "ARG" in seed
    assert seed["ARG"] > seed["RSA"]


def test_update_elo_from_results_processes_in_chronological_order(tmp_path):
    seed = {"ARG": 2000, "RSA": 1600}
    results = pd.DataFrame([
        {"date": dt.date(2026, 6, 11), "home": "ARG", "away": "RSA",
         "home_goals": 2, "away_goals": 0, "neutral": True},
    ])
    updated = update_elo_from_results(seed, results, k=30)
    assert updated["ARG"] > 2000   # won as expected, small bump
    assert updated["RSA"] < 1600
```

- [ ] **Step 3: Run tests, expect failures**

```bash
pytest tests/test_ratings.py -v
```

Expected: 5 failures.

- [ ] **Step 4: Implement `forecaster/ratings.py`**

```python
"""Elo rating computation and maintenance."""
from __future__ import annotations

import datetime as dt
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

    `result` is from the home team's perspective. `home_field` is the implicit
    Elo bonus given to home teams in non-neutral matches when computing the
    expected score, but we never persist it to the rating itself.
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
            result = "W"
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
```

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_ratings.py -v
```

Expected: 5 passed.

- [ ] **Step 6: Commit**

```bash
git add forecaster/ratings.py tests/test_ratings.py data/elo_seed.csv
git commit -m "feat(ratings): Elo init + update from results"
```

---

## Task 7: Dixon-Coles math (Poisson grid + τ correction)

Implements the math primitives only. Fitting and predict-orchestration land in Task 8.

**Files:**
- Create: `forecaster/model.py`
- Create: `tests/test_model.py`

- [ ] **Step 1: Write failing tests for the math**

`tests/test_model.py`:

```python
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
    assert abs(grid.sum() - 1.0) < 1e-3   # truncation error tiny at max_goals=10


def test_tau_reduces_to_one_outside_low_score_cells():
    assert tau(2, 0, 1.4, 1.0, rho=-0.1) == 1.0
    assert tau(0, 2, 1.4, 1.0, rho=-0.1) == 1.0
    assert tau(2, 2, 1.4, 1.0, rho=-0.1) == 1.0


def test_tau_dixon_coles_corrections():
    # ρ < 0 ⇒ draws under-predicted by independent Poisson get a boost.
    rho = -0.1
    lh, la = 1.4, 1.0
    assert tau(0, 0, lh, la, rho) == 1 - lh * la * rho       # > 1
    assert tau(1, 0, lh, la, rho) == 1 + la * rho            # < 1
    assert tau(0, 1, lh, la, rho) == 1 + lh * rho            # < 1
    assert tau(1, 1, lh, la, rho) == 1 - rho                 # > 1


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
```

- [ ] **Step 2: Run tests, expect failures**

```bash
pytest tests/test_model.py -v
```

Expected: 6 failures.

- [ ] **Step 3: Implement `forecaster/model.py` (math primitives)**

```python
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

    λ_h = base * 10^((elo_h − elo_a)/scale) * home_adv
    λ_a = base * 10^((elo_a − elo_h)/scale) / home_adv

    The home_adv multiplier is symmetrically applied — if home_adv == 1 (true
    neutral venue), λ_h × λ_a == base². For home_adv > 1, the home team's
    expected goals get scaled up and the away team's down.
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
    # Apply τ to the four low-score cells.
    grid[0, 0] *= tau(0, 0, lambda_h, lambda_a, rho)
    grid[0, 1] *= tau(0, 1, lambda_h, lambda_a, rho)
    grid[1, 0] *= tau(1, 0, lambda_h, lambda_a, rho)
    grid[1, 1] *= tau(1, 1, lambda_h, lambda_a, rho)
    # Renormalise (truncation + τ both leave a tiny residual).
    grid = grid / grid.sum()
    return grid
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_model.py -v
```

Expected: 6 passed.

- [ ] **Step 5: Commit**

```bash
git add forecaster/model.py tests/test_model.py
git commit -m "feat(model): Dixon-Coles primitives (Poisson grid, tau, expected goals)"
```

---

## Task 8: Dixon-Coles fit + predict

Fits 4 parameters (`base_goals`, `home_adv`, `rho`, `xi`) by maximum likelihood on time-decayed historical results, then predicts for upcoming fixtures.

**Files:**
- Modify: `forecaster/model.py` (add `fit_params`, `predict_fixture`, `predict_all`)
- Modify: `tests/test_model.py`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_model.py`:

```python
def test_fit_params_recovers_synthetic_values():
    """Fit on data generated from known (base, home_adv, rho), recover them ±tolerance."""
    import datetime as dt
    import numpy as np
    import pandas as pd
    from forecaster.model import dixon_coles_grid, fit_params

    rng = np.random.default_rng(42)
    true = dict(base_goals=1.3, home_adv=1.25, rho=-0.05, xi=0.001)
    elos = {f"T{i}": 1500 + rng.normal(0, 200) for i in range(10)}
    rows = []
    for _ in range(2000):
        h, a = rng.choice(list(elos.keys()), size=2, replace=False)
        from forecaster.model import expected_goals_from_elo
        lh, la = expected_goals_from_elo(elos[h], elos[a],
                                         true["base_goals"], true["home_adv"])
        grid = dixon_coles_grid(lh, la, true["rho"], max_goals=10)
        flat = grid.flatten()
        idx = rng.choice(len(flat), p=flat / flat.sum())
        i, j = divmod(idx, grid.shape[1])
        rows.append({
            "date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=rng.integers(0, 365)),
            "home": h, "away": a,
            "home_goals": int(i), "away_goals": int(j),
            "neutral": False,
        })
    df = pd.DataFrame(rows)
    fitted = fit_params(df, elos, ref_date=pd.Timestamp("2025-01-01"))
    assert abs(fitted["base_goals"] - true["base_goals"]) < 0.2
    assert abs(fitted["home_adv"] - true["home_adv"]) < 0.2
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
    assert pred.lambda_home > pred.lambda_away  # MEX favoured at home
    assert abs(pred.score_grid.grid.sum() - 1.0) < 1e-9
```

- [ ] **Step 2: Run tests, expect failures**

```bash
pytest tests/test_model.py -v
```

Expected: 2 failures.

- [ ] **Step 3: Implement `fit_params` + `predict_fixture` + `predict_all`**

Append to `forecaster/model.py`:

```python
import datetime as dt
from typing import Mapping

import pandas as pd
from scipy.optimize import minimize
from scipy.stats import poisson as _poisson

from forecaster.schema import Fixture, Prediction, ScoreGrid


def _log_likelihood_match(
    home_goals: int,
    away_goals: int,
    lambda_h: float,
    lambda_a: float,
    rho: float,
) -> float:
    """Log P(home_goals, away_goals | λ_h, λ_a, ρ) under Dixon-Coles."""
    log_p = (
        _poisson.logpmf(home_goals, lambda_h)
        + _poisson.logpmf(away_goals, lambda_a)
    )
    t = tau(home_goals, away_goals, lambda_h, lambda_a, rho)
    if t <= 0:
        return -1e9   # invalid τ — heavy penalty so optimizer steers away
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

    def neg_ll(params: np.ndarray) -> float:
        base_goals, home_adv, rho, xi = params
        if base_goals <= 0 or home_adv <= 0 or xi < 0:
            return 1e9
        weights = np.exp(-xi * df["days_ago"].to_numpy())
        ll = 0.0
        for w, h_elo, a_elo, hg, ag, neutral in zip(
            weights,
            df["elo_h"].to_numpy(),
            df["elo_a"].to_numpy(),
            df["home_goals"].to_numpy(),
            df["away_goals"].to_numpy(),
            df["neutral"].to_numpy(),
            strict=False,
        ):
            ha = 1.0 if neutral else home_adv
            lh = base_goals * (10 ** ((h_elo - a_elo) / config.ELO_SCALE)) * ha
            la = base_goals * (10 ** ((a_elo - h_elo) / config.ELO_SCALE)) / ha
            ll += w * _log_likelihood_match(int(hg), int(ag), lh, la, rho)
        return -ll

    result = minimize(
        neg_ll, x0,
        method="Nelder-Mead",
        options={"xatol": 1e-4, "fatol": 1e-4, "maxiter": 2000},
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
    # Home advantage applies if the home team is from the venue country.
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
        recommended_pick=(0, 0),       # filled in by picks.py
        expected_points=0.0,           # filled in by picks.py
        top_scorelines=[],
    )


def predict_all(
    fixtures: list[Fixture],
    elo: Mapping[str, float],
    params: Mapping[str, float],
) -> list[Prediction]:
    """Predict every SCHEDULED fixture."""
    return [predict_fixture(f, elo, params) for f in fixtures if f.status == "SCHEDULED"]
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_model.py -v
```

Expected: 8 passed (the synthetic-recovery test takes ~5–15 s).

- [ ] **Step 5: Commit**

```bash
git add forecaster/model.py tests/test_model.py
git commit -m "feat(model): Dixon-Coles fit + predict_fixture"
```

---

## Task 9: Picks (scoring rule + EV optimizer)

The colleague-beating module. Implements the adidas Forecaster scoring rule (3 outcome + 1 per-team-score + 1 goal diff) and picks the EV-optimal scoreline by exhaustive search over the 8×8 grid.

**Files:**
- Create: `forecaster/picks.py`
- Create: `tests/test_picks.py`

- [ ] **Step 1: Write the failing tests**

`tests/test_picks.py`:

```python
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
    # Prediction matches actual exactly: 3 (outcome) + 1 (home) + 1 (away) + 1 (gd) = 6
    assert score_pick((2, 1), (2, 1)) == 6


def test_score_pick_correct_outcome_only():
    # Predicted 2:0, actual 1:0 → outcome ✓ +3, away score ✓ +1 (both 0). Total 4.
    assert score_pick((2, 0), (1, 0)) == 4


def test_score_pick_outcome_plus_goal_diff_no_team_score_match():
    # 2:0 vs 3:1 → outcome ✓ +3, gd ✓ +1, neither team's exact score matches. Total 4.
    assert score_pick((2, 0), (3, 1)) == 4


def test_score_pick_wrong_outcome():
    # Predicted home win, actual away win.
    assert score_pick((2, 0), (0, 1)) == 0


def test_score_pick_draw_correct_outcome():
    assert score_pick((1, 1), (2, 2)) == 3   # outcome ✓ + gd ✓ ... actually:
    # 1:1 vs 2:2 → both draws (outcome ✓ +3), neither team score matches (1≠2),
    # goal diff matches (0 == 0) → +1. Total 4.


def test_score_pick_draw_correct_outcome_recheck():
    # 1:1 vs 2:2 → outcome ✓ (both draw), gd ✓ (0 == 0), team scores ✗.
    # Outcome 3 + gd 1 = 4.
    assert score_pick((1, 1), (2, 2)) == 4


def test_expected_points_uniform_grid():
    grid = np.full((3, 3), 1 / 9)
    sg = ScoreGrid(home="A", away="B", grid=grid)
    ep = expected_points((1, 1), sg)
    # Sanity: must be in [0, 6].
    assert 0 < ep < 6


def test_optimal_pick_picks_highest_ev_cell():
    # Construct a grid where 1-0 is by far the most common outcome.
    grid = np.zeros((4, 4))
    grid[1, 0] = 0.7
    grid[0, 0] = 0.1
    grid[2, 0] = 0.1
    grid[1, 1] = 0.1
    sg = ScoreGrid(home="A", away="B", grid=grid)
    pick, ev = optimal_pick(sg)
    assert pick == (1, 0)
    assert ev > 4   # at least outcome + per-team-scores + goal-diff most of the time


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
    grid = np.full((3, 3), 1 / 9)
    sg = ScoreGrid(home="A", away="B", grid=grid)
    p = Prediction(
        fixture_id="x", score_grid=sg, lambda_home=1.0, lambda_away=1.0,
        recommended_pick=(0, 0), expected_points=0.0, top_scorelines=[],
    )
    [enriched] = enrich_predictions([p])
    assert enriched.recommended_pick != (0, 0) or enriched.expected_points > 0
    assert len(enriched.top_scorelines) == 4   # default n
```

(Note the duplicated draw test — I keep the corrected one. Delete the first `test_score_pick_draw_correct_outcome` from the file before running.)

- [ ] **Step 2: Run tests, expect failures**

```bash
pytest tests/test_picks.py -v
```

Expected: failures (functions don't exist).

- [ ] **Step 3: Implement `forecaster/picks.py`**

```python
"""adidas Forecaster scoring rule + EV-optimal pick selection."""
from __future__ import annotations

import numpy as np

from forecaster import config
from forecaster.schema import Prediction, ScoreGrid


def score_pick(predicted: tuple[int, int], actual: tuple[int, int]) -> int:
    """adidas Forecaster scoring: 3 outcome + 1 per-team-score + 1 goal diff."""
    p_h, p_a = predicted
    a_h, a_a = actual

    # Outcome (sign of goal difference).
    p_sign = (p_h > p_a) - (p_h < p_a)
    a_sign = (a_h > a_a) - (a_h < a_a)
    outcome = config.SCORE_OUTCOME if p_sign == a_sign else 0

    # Per-team correct score.
    home_match = config.SCORE_PER_TEAM_GOAL if p_h == a_h else 0
    away_match = config.SCORE_PER_TEAM_GOAL if p_a == a_a else 0

    # Goal difference (only counts when outcome is correct — a 1:1 prediction
    # vs a 0:0 result has the same gd but different outcome; per the app, the
    # goal-diff bonus implies the outcome is also right). For symmetric draws
    # (gd=0), p_sign == a_sign already covers it.
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
```

- [ ] **Step 4: Clean the duplicated test**

Open `tests/test_picks.py` and delete the first `test_score_pick_draw_correct_outcome` (the one with the incorrect inline assertion). Keep `test_score_pick_draw_correct_outcome_recheck`.

- [ ] **Step 5: Run tests**

```bash
pytest tests/test_picks.py -v
```

Expected: 9 passed.

- [ ] **Step 6: Commit**

```bash
git add forecaster/picks.py tests/test_picks.py
git commit -m "feat(picks): adidas Forecaster scoring rule + EV-optimal pick"
```

---

## Task 10: Publish — base orchestration + per-fixture JSON

Sets up the `publish` module skeleton, writes per-fixture JSON, and exposes hooks the HTML/markdown renderers (Tasks 11, 12) call.

**Files:**
- Create: `forecaster/publish.py`
- Create: `tests/test_publish.py`

- [ ] **Step 1: Write the failing test**

`tests/test_publish.py`:

```python
"""Publish module — JSON, HTML, prompt-pack."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

import numpy as np

from forecaster.publish import write_per_fixture_json
from forecaster.schema import Fixture, Prediction, ScoreGrid


def _make_pred(fixture_id: str = "2026-06-11-MEX-RSA") -> Prediction:
    grid = np.zeros((3, 3))
    grid[1, 0] = 0.5
    grid[0, 0] = 0.3
    grid[1, 1] = 0.2
    sg = ScoreGrid(home="MEX", away="RSA", grid=grid)
    return Prediction(
        fixture_id=fixture_id, score_grid=sg,
        lambda_home=1.4, lambda_away=0.7,
        recommended_pick=(1, 0), expected_points=4.5,
        top_scorelines=[((1, 0), 0.5), ((0, 0), 0.3), ((1, 1), 0.2)],
    )


def _make_fixture(fixture_id: str = "2026-06-11-MEX-RSA") -> Fixture:
    return Fixture(
        fixture_id=fixture_id,
        utc_kickoff=dt.datetime(2026, 6, 11, 18, 0, tzinfo=dt.timezone.utc),
        home="MEX", away="RSA", venue_country="MEX",
        stage="GROUP", status="SCHEDULED",
        actual_home_goals=None, actual_away_goals=None,
    )


def test_write_per_fixture_json_creates_file_per_fixture(tmp_data_dir, monkeypatch):
    from forecaster import config

    monkeypatch.setattr(config, "DOCS_API_DIR", tmp_data_dir.parent / "docs" / "api")
    config.DOCS_API_DIR.mkdir(parents=True, exist_ok=True)

    fixtures = [_make_fixture("a"), _make_fixture("b")]
    preds = [_make_pred("a"), _make_pred("b")]
    rationale = {"a": "test rationale a", "b": "test rationale b"}

    paths = write_per_fixture_json(fixtures, preds, rationale)
    assert len(paths) == 2

    payload = json.loads(paths[0].read_text())
    assert payload["fixture_id"] == "a"
    assert payload["recommended_pick"] == [1, 0]
    assert "rationale" in payload
    assert payload["w_d_l"]["draw"] >= 0
```

- [ ] **Step 2: Run tests, expect failure**

```bash
pytest tests/test_publish.py -v
```

Expected: import error (function doesn't exist).

- [ ] **Step 3: Implement `forecaster/publish.py` (skeleton + JSON writer)**

```python
"""Publish predictions: per-fixture JSON, HTML dashboard, prompt pack."""
from __future__ import annotations

import datetime as dt
import json
from pathlib import Path

from forecaster import config
from forecaster.schema import Fixture, Prediction


def _wdl(prediction: Prediction) -> dict[str, float]:
    sg = prediction.score_grid
    return {"win": sg.win_prob(), "draw": sg.draw_prob(), "loss": sg.loss_prob()}


def _payload(
    fixture: Fixture, prediction: Prediction, rationale: str | None
) -> dict:
    return {
        "fixture_id": fixture.fixture_id,
        "kickoff_utc": fixture.utc_kickoff.isoformat(),
        "home": fixture.home,
        "away": fixture.away,
        "stage": fixture.stage,
        "status": fixture.status,
        "actual": (
            None if fixture.actual_home_goals is None
            else [fixture.actual_home_goals, fixture.actual_away_goals]
        ),
        "recommended_pick": list(prediction.recommended_pick),
        "expected_points": round(prediction.expected_points, 3),
        "lambda_home": round(prediction.lambda_home, 3),
        "lambda_away": round(prediction.lambda_away, 3),
        "w_d_l": {k: round(v, 4) for k, v in _wdl(prediction).items()},
        "top_scorelines": [
            {"score": list(s), "prob": round(p, 4)}
            for s, p in prediction.top_scorelines
        ],
        "score_grid": [
            [round(v, 5) for v in row] for row in prediction.score_grid.grid.tolist()
        ],
        "rationale": rationale,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
    }


def write_per_fixture_json(
    fixtures: list[Fixture],
    predictions: list[Prediction],
    rationale: dict[str, str],
) -> list[Path]:
    """Write one JSON file per fixture under `docs/api/`."""
    config.DOCS_API_DIR.mkdir(parents=True, exist_ok=True)
    pred_by_id = {p.fixture_id: p for p in predictions}
    paths: list[Path] = []
    for f in fixtures:
        if f.fixture_id not in pred_by_id:
            continue
        path = config.DOCS_API_DIR / f"{f.fixture_id}.json"
        path.write_text(json.dumps(
            _payload(f, pred_by_id[f.fixture_id], rationale.get(f.fixture_id)),
            indent=2,
        ))
        paths.append(path)
    return paths
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_publish.py -v
```

Expected: 1 passed.

- [ ] **Step 5: Commit**

```bash
git add forecaster/publish.py tests/test_publish.py
git commit -m "feat(publish): per-fixture JSON output"
```

---

## Task 11: Publish — HTML dashboard

Mobile-first static HTML, dark-mode-aware, Apple touch icon for "Add to Home Screen", "Open in Claude Chat" copy-and-redirect button per fixture.

**Files:**
- Create: `forecaster/templates/index.html.j2`
- Create: `forecaster/templates/style.css`
- Modify: `forecaster/publish.py` (add `write_html_dashboard`)
- Modify: `tests/test_publish.py`
- Create: `docs/apple-touch-icon.png` (placeholder; user can replace)

- [ ] **Step 1: Add a placeholder icon**

```bash
python -c "
from struct import pack
import zlib
def png(w, h, rgba):
    sig = b'\x89PNG\r\n\x1a\n'
    def chunk(t, d): return pack('>I', len(d)) + t + d + pack('>I', zlib.crc32(t + d))
    ihdr = chunk(b'IHDR', pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0))
    raw = b''
    for y in range(h):
        raw += b'\x00' + bytes(rgba) * w
    idat = chunk(b'IDAT', zlib.compress(raw))
    iend = chunk(b'IEND', b'')
    return sig + ihdr + idat + iend
open('docs/apple-touch-icon.png', 'wb').write(png(180, 180, [16, 16, 16, 255]))
"
```

This creates a 180×180 dark-grey square. You can replace it later with a proper football icon.

- [ ] **Step 2: Write the CSS** (`forecaster/templates/style.css`)

```css
:root {
  --bg: #0d1117;
  --card: #161b22;
  --fg: #e6edf3;
  --muted: #8b949e;
  --accent: #ff6b35;
  --win: #3fb950;
  --draw: #d29922;
  --loss: #f85149;
  --border: #30363d;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg: #ffffff;
    --card: #f6f8fa;
    --fg: #1f2328;
    --muted: #59636e;
    --accent: #cc4b13;
    --win: #1a7f37;
    --draw: #9a6700;
    --loss: #cf222e;
    --border: #d0d7de;
  }
}
* { box-sizing: border-box; }
html, body {
  margin: 0; padding: 0;
  background: var(--bg); color: var(--fg);
  font: 16px/1.5 -apple-system, BlinkMacSystemFont, system-ui, sans-serif;
}
.container { max-width: 480px; margin: 0 auto; padding: 16px; }
header h1 { font-size: 18px; margin: 8px 0 4px; }
header .meta { color: var(--muted); font-size: 13px; margin-bottom: 16px; }
.day-heading {
  font-size: 13px; text-transform: uppercase; letter-spacing: 1px;
  color: var(--muted); margin: 24px 0 8px;
}
.card {
  background: var(--card); border: 1px solid var(--border);
  border-radius: 12px; padding: 16px; margin-bottom: 12px;
}
.matchup { display: flex; justify-content: space-between; align-items: center; }
.matchup .team { font-weight: 600; font-size: 18px; }
.matchup .vs { color: var(--muted); font-size: 13px; }
.row { display: flex; justify-content: space-between; margin: 6px 0; font-size: 14px; }
.row .label { color: var(--muted); }
.pick { font-weight: 700; color: var(--accent); }
.wdl-bar {
  display: flex; height: 8px; border-radius: 4px; overflow: hidden;
  margin: 8px 0;
}
.wdl-bar .w { background: var(--win); }
.wdl-bar .d { background: var(--draw); }
.wdl-bar .l { background: var(--loss); }
.scoreline-row {
  display: flex; align-items: center; font-size: 13px;
  margin: 2px 0; gap: 8px;
}
.scoreline-row .score { width: 36px; font-variant-numeric: tabular-nums; }
.scoreline-row .pct { width: 36px; color: var(--muted); }
.scoreline-row .bar { flex: 1; height: 6px; background: var(--border); border-radius: 3px; }
.scoreline-row .bar > span { display: block; height: 100%; background: var(--accent); border-radius: 3px; }
.why { font-size: 14px; color: var(--fg); margin-top: 12px; }
.why .caveats { color: var(--muted); font-size: 13px; margin-top: 4px; }
.btn {
  display: inline-block; min-height: 44px; line-height: 44px;
  background: var(--accent); color: white; border: none;
  border-radius: 8px; padding: 0 16px; font-weight: 600;
  text-decoration: none; cursor: pointer; margin-top: 12px;
  width: 100%; text-align: center;
}
.btn:active { opacity: 0.8; }
details.past { margin-top: 24px; }
details.past summary {
  font-size: 13px; text-transform: uppercase; letter-spacing: 1px;
  color: var(--muted); cursor: pointer;
}
.accuracy { font-size: 13px; color: var(--muted); margin: 8px 0; }
```

- [ ] **Step 3: Write the Jinja template** (`forecaster/templates/index.html.j2`)

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="theme-color" content="#0d1117">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="stylesheet" href="/style.css">
  <title>⚽ Forecaster</title>
</head>
<body>
<div class="container">
  <header>
    <h1>⚽ Forecaster</h1>
    <div class="meta">Updated {{ generated_at_utc }} UTC · Model accuracy: {{ accuracy }}</div>
  </header>

  {% for day in upcoming_days %}
    <div class="day-heading">{{ day.label }}</div>
    {% for card in day.cards %}
      <article class="card" id="{{ card.fixture_id }}">
        <div class="matchup">
          <span class="team">{{ card.home }}</span>
          <span class="vs">{{ card.kickoff_local }}</span>
          <span class="team">{{ card.away }}</span>
        </div>
        <div class="row"><span class="label">My pick</span><span class="pick">{{ card.pick[0] }} − {{ card.pick[1] }} ★</span></div>
        <div class="row"><span class="label">Most likely</span><span>{{ card.most_likely[0] }} − {{ card.most_likely[1] }} ({{ card.most_likely_pct }}%)</span></div>
        <div class="row"><span class="label">W / D / L</span><span>{{ card.w_pct }}% / {{ card.d_pct }}% / {{ card.l_pct }}%</span></div>
        <div class="wdl-bar">
          <div class="w" style="width: {{ card.w_pct }}%"></div>
          <div class="d" style="width: {{ card.d_pct }}%"></div>
          <div class="l" style="width: {{ card.l_pct }}%"></div>
        </div>
        <div class="row"><span class="label">Top scorelines</span><span></span></div>
        {% for sl in card.top_scorelines %}
          <div class="scoreline-row">
            <span class="score">{{ sl.h }}-{{ sl.a }}</span>
            <span class="pct">{{ sl.pct }}%</span>
            <span class="bar"><span style="width: {{ sl.bar_pct }}%"></span></span>
          </div>
        {% endfor %}
        <div class="why">
          <strong>Why</strong><br>{{ card.why }}
        </div>
        <button class="btn" data-fixture="{{ card.fixture_id }}" onclick="copyAndOpen(this)">Open in Claude Chat</button>
      </article>
    {% endfor %}
  {% endfor %}

  {% if past_cards %}
    <details class="past">
      <summary>Past matches ({{ past_cards|length }})</summary>
      <p class="accuracy">Outcome: {{ accuracy_outcome }} · Total points so far: {{ total_points }}</p>
      {% for card in past_cards %}
        <article class="card">
          <div class="matchup">
            <span class="team">{{ card.home }}</span>
            <span class="vs">{{ card.actual[0] }} − {{ card.actual[1] }}</span>
            <span class="team">{{ card.away }}</span>
          </div>
          <div class="row"><span class="label">Picked</span><span>{{ card.pick[0] }} − {{ card.pick[1] }}</span></div>
          <div class="row"><span class="label">Points</span><span class="pick">+{{ card.points }}</span></div>
        </article>
      {% endfor %}
    </details>
  {% endif %}
</div>

<script type="application/json" id="briefings">{{ briefings_json|safe }}</script>
<script>
async function copyAndOpen(btn) {
  const id = btn.dataset.fixture;
  const briefings = JSON.parse(document.getElementById('briefings').textContent);
  const text = briefings[id];
  if (!text) return;
  try {
    await navigator.clipboard.writeText(text);
    btn.textContent = "✓ Copied — opening Claude…";
  } catch (e) {
    // Fallback: select-all in a hidden textarea so user long-presses copy.
    const ta = document.createElement('textarea');
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand('copy');
    ta.remove();
    btn.textContent = "✓ Copied — opening Claude…";
  }
  setTimeout(() => window.open('https://claude.ai/new', '_blank'), 400);
}
</script>
</body>
</html>
```

- [ ] **Step 4: Add `write_html_dashboard` to `forecaster/publish.py`**

Append to `forecaster/publish.py`:

```python
import shutil
from collections import defaultdict
from typing import Iterable

from jinja2 import Environment, FileSystemLoader, select_autoescape


def _percent(p: float) -> int:
    return int(round(p * 100))


def _build_card(
    f: Fixture, p: Prediction, rationale: str | None
) -> dict:
    sg = p.score_grid
    most_likely = max(
        ((i, j) for i in range(sg.grid.shape[0]) for j in range(sg.grid.shape[1])),
        key=lambda ij: sg.grid[ij],
    )
    most_likely_pct = _percent(sg.grid[most_likely])
    top = [
        {
            "h": s[0], "a": s[1],
            "pct": _percent(prob),
            "bar_pct": min(100, _percent(prob / max(p.top_scorelines[0][1], 1e-6))),
        }
        for s, prob in p.top_scorelines
    ]
    return {
        "fixture_id": f.fixture_id,
        "home": f.home, "away": f.away,
        "kickoff_local": f.utc_kickoff.strftime("%H:%M UTC"),
        "pick": list(p.recommended_pick),
        "most_likely": list(most_likely),
        "most_likely_pct": most_likely_pct,
        "w_pct": _percent(sg.win_prob()),
        "d_pct": _percent(sg.draw_prob()),
        "l_pct": _percent(sg.loss_prob()),
        "top_scorelines": top,
        "why": rationale or "(rationale unavailable)",
    }


def _build_briefing(f: Fixture, p: Prediction, rationale: str | None) -> str:
    """Self-contained markdown briefing copied to clipboard for Claude Chat."""
    sg = p.score_grid
    grid_lines = []
    for i, row in enumerate(sg.grid):
        for j, prob in enumerate(row):
            if prob >= 0.005:
                grid_lines.append(f"- {i}:{j} → {prob*100:.1f}%")
    return f"""You are advising me on a Kicktipp-style prediction. Scoring rule:
- Correct outcome: +3
- Each correct team score: +1
- Correct goal difference: +1
- Max per match: 6

Match: **{f.home} vs {f.away}** ({f.stage}, {f.utc_kickoff.isoformat()})

Pre-computed Dixon-Coles probabilities (trust these — don't recompute):
- λ home (expected goals): {p.lambda_home:.2f}
- λ away (expected goals): {p.lambda_away:.2f}
- W / D / L: {sg.win_prob()*100:.1f}% / {sg.draw_prob()*100:.1f}% / {sg.loss_prob()*100:.1f}%

Likely scorelines (≥ 0.5%):
{chr(10).join(grid_lines)}

Recommended pick (EV-optimal): **{p.recommended_pick[0]}-{p.recommended_pick[1]}** (EV ≈ {p.expected_points:.2f} pts)

Context:
{rationale or '(no rationale provided)'}

Help me reason about which scoreline to actually submit. If I'm risk-averse, lean toward higher-probability picks; if I'm chasing the leaderboard, suggest a higher-variance gamble. Use the numbers above; do not invent new ones.
"""


def _group_by_day(
    fixtures: Iterable[Fixture], now_utc: dt.datetime
) -> tuple[list[dict], list[dict]]:
    """Return (upcoming_days, past_fixtures)."""
    today = now_utc.date()
    upcoming: dict[dt.date, list[Fixture]] = defaultdict(list)
    past: list[Fixture] = []
    for f in fixtures:
        d = f.utc_kickoff.date()
        if d < today or f.status == "FINISHED":
            past.append(f)
        else:
            upcoming[d].append(f)
    days = []
    for d in sorted(upcoming):
        label = "TODAY" if d == today else (
            "TOMORROW" if d == today + dt.timedelta(days=1)
            else d.strftime("%A %d %b").upper()
        )
        days.append({"date": d, "label": label, "fixtures": sorted(upcoming[d], key=lambda f: f.utc_kickoff)})
    return days, sorted(past, key=lambda f: f.utc_kickoff, reverse=True)


def write_html_dashboard(
    fixtures: list[Fixture],
    predictions: list[Prediction],
    rationale: dict[str, str],
    now_utc: dt.datetime | None = None,
) -> Path:
    """Render `docs/index.html` from the templates."""
    now_utc = now_utc or dt.datetime.now(dt.timezone.utc)
    pred_by_id = {p.fixture_id: p for p in predictions}

    upcoming_days, past_fixtures = _group_by_day(fixtures, now_utc)
    days_view = [
        {
            "label": d["label"],
            "cards": [
                _build_card(f, pred_by_id[f.fixture_id], rationale.get(f.fixture_id))
                for f in d["fixtures"] if f.fixture_id in pred_by_id
            ],
        }
        for d in upcoming_days
    ]

    past_cards = []
    n_outcome_correct = 0
    total_points = 0
    for f in past_fixtures:
        p = pred_by_id.get(f.fixture_id)
        if p is None or f.actual_home_goals is None:
            continue
        from forecaster.picks import score_pick
        actual = (f.actual_home_goals, f.actual_away_goals)
        pts = score_pick(p.recommended_pick, actual)
        if (p.recommended_pick[0] > p.recommended_pick[1]) == (actual[0] > actual[1]) and \
           (p.recommended_pick[0] < p.recommended_pick[1]) == (actual[0] < actual[1]):
            n_outcome_correct += 1
        total_points += pts
        past_cards.append({
            "home": f.home, "away": f.away,
            "actual": list(actual),
            "pick": list(p.recommended_pick),
            "points": pts,
        })

    accuracy_outcome = (
        f"{n_outcome_correct}/{len(past_cards)}" if past_cards else "n/a"
    )
    briefings = {
        f.fixture_id: _build_briefing(f, pred_by_id[f.fixture_id], rationale.get(f.fixture_id))
        for f in fixtures if f.fixture_id in pred_by_id
    }

    env = Environment(
        loader=FileSystemLoader(config.TEMPLATES_DIR),
        autoescape=select_autoescape(["html"]),
    )
    template = env.get_template("index.html.j2")
    html = template.render(
        generated_at_utc=now_utc.strftime("%Y-%m-%d %H:%M"),
        accuracy=f"{n_outcome_correct} of {len(past_cards)}" if past_cards else "—",
        upcoming_days=days_view,
        past_cards=past_cards,
        accuracy_outcome=accuracy_outcome,
        total_points=total_points,
        briefings_json=json.dumps(briefings),
    )
    out = config.DOCS_DIR / "index.html"
    out.write_text(html)
    # Copy CSS alongside.
    shutil.copy(config.TEMPLATES_DIR / "style.css", config.DOCS_DIR / "style.css")
    return out
```

- [ ] **Step 5: Add an HTML test**

Append to `tests/test_publish.py`:

```python
def test_write_html_dashboard_renders_today_card(tmp_data_dir, monkeypatch):
    import datetime as dt
    from forecaster import config
    from forecaster.publish import write_html_dashboard

    monkeypatch.setattr(config, "DOCS_DIR", tmp_data_dir.parent / "docs")
    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)

    fixture = _make_fixture()
    prediction = _make_pred()
    rationale = {fixture.fixture_id: "MEX favoured at home; weather hot."}

    out = write_html_dashboard(
        [fixture], [prediction], rationale,
        now_utc=dt.datetime(2026, 6, 11, 12, 0, tzinfo=dt.timezone.utc),
    )
    assert out.exists()
    html = out.read_text()
    assert "MEX" in html and "RSA" in html
    assert "★" in html
    assert "TODAY" in html
    assert "Open in Claude Chat" in html
    assert "MEX favoured at home" in html
```

- [ ] **Step 6: Run tests**

```bash
pytest tests/test_publish.py -v
```

Expected: 2 passed.

- [ ] **Step 7: Commit**

```bash
git add forecaster/templates forecaster/publish.py tests/test_publish.py docs/apple-touch-icon.png
git commit -m "feat(publish): mobile-first HTML dashboard"
```

---

## Task 12: Publish — prompt pack (markdown)

The tournament-wide briefing you paste into Claude Chat once per day. Self-contained: scoring rule + every upcoming fixture's grid + system prompt.

**Files:**
- Create: `forecaster/templates/prompt-pack.md.j2`
- Modify: `forecaster/publish.py` (add `write_prompt_pack`)
- Modify: `tests/test_publish.py`

- [ ] **Step 1: Write the Jinja template**

`forecaster/templates/prompt-pack.md.j2`:

```markdown
# Football Forecaster — Prompt Pack

Generated {{ generated_at_utc }} UTC. Paste this whole document into Claude Chat, then ask any question about the upcoming fixtures.

## System prompt for Claude

You are advising me on a Kicktipp-style football prediction pool. **Trust the numbers below as ground truth — do not recompute Poisson math.** Your job is to help me reason about *which scoreline to submit* given the pre-computed probability distribution and the scoring rule.

### Scoring rule (per match)

| Component | Points |
| --- | --- |
| Correct outcome (W/D/L) | +3 |
| Each team's exact goal count | +1 each (max +2) |
| Correct goal difference | +1 |
| **Max per match** | **6** |

When I ask about a specific match, look it up below. When I ask "which is safer" or "which gambles for points", reason about the trade-off using the listed probabilities and EV. If I provide late news (injuries, weather), adjust qualitatively but don't invent numbers.

---

## Fixtures

{% for f in fixtures %}
### {{ f.home }} vs {{ f.away }} — {{ f.kickoff_label }}

- **Stage:** {{ f.stage }}
- **Recommended pick (EV-optimal):** {{ f.pick[0] }}-{{ f.pick[1] }} (EV ≈ {{ f.ev }} pts)
- **W / D / L:** {{ f.w_pct }}% / {{ f.d_pct }}% / {{ f.l_pct }}%
- **λ_home / λ_away:** {{ f.lambda_home }} / {{ f.lambda_away }}
- **Top scorelines:**
{% for sl in f.top_scorelines %}  - {{ sl.h }}:{{ sl.a }} ({{ sl.pct }}%)
{% endfor %}
- **Why:** {{ f.why }}

{% endfor %}
```

- [ ] **Step 2: Implement `write_prompt_pack`**

Append to `forecaster/publish.py`:

```python
def write_prompt_pack(
    fixtures: list[Fixture],
    predictions: list[Prediction],
    rationale: dict[str, str],
    now_utc: dt.datetime | None = None,
) -> Path:
    """Render `docs/prompt-pack.md`."""
    now_utc = now_utc or dt.datetime.now(dt.timezone.utc)
    pred_by_id = {p.fixture_id: p for p in predictions}

    rows = []
    for f in sorted(fixtures, key=lambda f: f.utc_kickoff):
        if f.status == "FINISHED" or f.fixture_id not in pred_by_id:
            continue
        p = pred_by_id[f.fixture_id]
        sg = p.score_grid
        rows.append({
            "home": f.home, "away": f.away,
            "stage": f.stage,
            "kickoff_label": f.utc_kickoff.strftime("%a %d %b %H:%M UTC"),
            "pick": list(p.recommended_pick),
            "ev": f"{p.expected_points:.2f}",
            "w_pct": _percent(sg.win_prob()),
            "d_pct": _percent(sg.draw_prob()),
            "l_pct": _percent(sg.loss_prob()),
            "lambda_home": f"{p.lambda_home:.2f}",
            "lambda_away": f"{p.lambda_away:.2f}",
            "top_scorelines": [
                {"h": s[0], "a": s[1], "pct": _percent(prob)}
                for s, prob in p.top_scorelines
            ],
            "why": rationale.get(f.fixture_id, "—"),
        })

    env = Environment(
        loader=FileSystemLoader(config.TEMPLATES_DIR),
        autoescape=False,
    )
    template = env.get_template("prompt-pack.md.j2")
    md = template.render(
        generated_at_utc=now_utc.strftime("%Y-%m-%d %H:%M"),
        fixtures=rows,
    )
    out = config.DOCS_DIR / "prompt-pack.md"
    out.write_text(md)
    return out
```

- [ ] **Step 3: Add a prompt-pack test**

Append to `tests/test_publish.py`:

```python
def test_write_prompt_pack_includes_rule_and_fixtures(tmp_data_dir, monkeypatch):
    from forecaster import config
    from forecaster.publish import write_prompt_pack

    monkeypatch.setattr(config, "DOCS_DIR", tmp_data_dir.parent / "docs")
    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)

    fixture = _make_fixture()
    prediction = _make_pred()
    rationale = {fixture.fixture_id: "MEX strong at home."}

    out = write_prompt_pack([fixture], [prediction], rationale)
    text = out.read_text()
    assert "Scoring rule" in text
    assert "MEX vs RSA" in text
    assert "Recommended pick" in text
    assert "MEX strong at home." in text
    assert "+3" in text and "+1 each" in text
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_publish.py -v
```

Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add forecaster/templates/prompt-pack.md.j2 forecaster/publish.py tests/test_publish.py
git commit -m "feat(publish): tournament-wide prompt pack for Claude Chat"
```

---

## Task 13: Rationale (Anthropic SDK + web search)

Per-fixture LLM call. The system prompt constrains Claude to *explain* the model's numbers using fetched form/injury data, not invent new probabilities.

**Files:**
- Create: `forecaster/rationale.py`
- Create: `tests/test_rationale.py`

- [ ] **Step 1: Write the failing test (mocked Anthropic client)**

`tests/test_rationale.py`:

```python
"""Rationale module — Claude API call with mocked client."""
from __future__ import annotations

import datetime as dt
from unittest.mock import MagicMock

import numpy as np

from forecaster.rationale import build_user_prompt, generate_rationale, generate_all
from forecaster.schema import Fixture, Prediction, ScoreGrid


def _fix(fid="2026-06-11-MEX-RSA"):
    return Fixture(
        fixture_id=fid,
        utc_kickoff=dt.datetime(2026, 6, 11, 18, 0, tzinfo=dt.timezone.utc),
        home="MEX", away="RSA", venue_country="MEX",
        stage="GROUP", status="SCHEDULED",
        actual_home_goals=None, actual_away_goals=None,
    )


def _pred(fid="2026-06-11-MEX-RSA"):
    grid = np.zeros((3, 3))
    grid[1, 0] = 0.5; grid[0, 0] = 0.3; grid[1, 1] = 0.2
    return Prediction(
        fixture_id=fid,
        score_grid=ScoreGrid(home="MEX", away="RSA", grid=grid),
        lambda_home=1.4, lambda_away=0.7,
        recommended_pick=(1, 0), expected_points=4.5,
        top_scorelines=[((1, 0), 0.5), ((0, 0), 0.3), ((1, 1), 0.2)],
    )


def test_build_user_prompt_includes_numbers():
    text = build_user_prompt(_fix(), _pred(), elo={"MEX": 1825, "RSA": 1620})
    assert "MEX" in text and "RSA" in text
    assert "1825" in text and "1620" in text
    assert "1-0" in text  # recommended pick
    assert "50.0%" in text or "50%" in text  # most likely cell


def test_generate_rationale_uses_client_response():
    client = MagicMock()
    client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="MEX favoured: 200-pt Elo edge, home crowd, dry conditions.")]
    )
    text = generate_rationale(_fix(), _pred(), elo={"MEX": 1825, "RSA": 1620},
                              client=client, web_search=False)
    assert "MEX favoured" in text
    client.messages.create.assert_called_once()


def test_generate_all_returns_dict_keyed_by_fixture_id():
    client = MagicMock()
    client.messages.create.return_value = MagicMock(
        content=[MagicMock(text="rationale text")]
    )
    out = generate_all([_fix()], [_pred()], elo={"MEX": 1825, "RSA": 1620},
                      client=client, web_search=False)
    assert out["2026-06-11-MEX-RSA"] == "rationale text"
```

- [ ] **Step 2: Run tests, expect failures**

```bash
pytest tests/test_rationale.py -v
```

Expected: 3 failures.

- [ ] **Step 3: Implement `forecaster/rationale.py`**

```python
"""LLM-written rationale per fixture (Claude Sonnet via Anthropic SDK)."""
from __future__ import annotations

import logging
import os
from typing import Mapping

import anthropic

from forecaster.schema import Fixture, Prediction

log = logging.getLogger(__name__)

SYSTEM_PROMPT = """You write 3-5 sentence rationale paragraphs explaining a football match prediction. You are given:
- The two teams and their Elo ratings
- A pre-computed Dixon-Coles model output (W/D/L probabilities, expected goals λ, recommended pick)
- (When web search is enabled) the ability to look up recent form, injuries, suspended players, lineups, and weather

RULES:
- Treat the model's probabilities as ground truth. Do NOT invent new ones.
- Cite specific qualitative factors (e.g. "Mbappé doubtful per L'Équipe") when web search returned them.
- If a key player is out or weather is extreme, FLAG IT as a caveat the model doesn't account for — but do NOT contradict the recommended pick.
- 3-5 short sentences. No bullet points. No headers. Plain prose.
- End with one specific caveat if any qualitative input is uncertain ("model doesn't price in...").
"""

DEFAULT_MODEL = "claude-sonnet-4-6"


def build_user_prompt(
    fixture: Fixture, prediction: Prediction, elo: Mapping[str, float]
) -> str:
    sg = prediction.score_grid
    most_likely = max(
        ((i, j) for i in range(sg.grid.shape[0]) for j in range(sg.grid.shape[1])),
        key=lambda ij: sg.grid[ij],
    )
    return (
        f"Match: {fixture.home} vs {fixture.away} ({fixture.stage}, "
        f"{fixture.utc_kickoff.isoformat()})\n"
        f"Venue country: {fixture.venue_country}\n"
        f"Elo: {fixture.home} {elo.get(fixture.home, 1500):.0f} vs "
        f"{fixture.away} {elo.get(fixture.away, 1500):.0f}\n"
        f"Expected goals (λ): {prediction.lambda_home:.2f} / {prediction.lambda_away:.2f}\n"
        f"W/D/L: {sg.win_prob()*100:.1f}% / {sg.draw_prob()*100:.1f}% / "
        f"{sg.loss_prob()*100:.1f}%\n"
        f"Most likely scoreline: {most_likely[0]}-{most_likely[1]} "
        f"({sg.grid[most_likely]*100:.1f}%)\n"
        f"Recommended pick (EV-optimal): {prediction.recommended_pick[0]}-"
        f"{prediction.recommended_pick[1]} (EV {prediction.expected_points:.2f} pts)\n\n"
        f"Look up recent form, injuries, and weather for {fixture.home} vs "
        f"{fixture.away} in {fixture.utc_kickoff.date().isoformat()}, then write "
        f"the rationale paragraph."
    )


def generate_rationale(
    fixture: Fixture,
    prediction: Prediction,
    elo: Mapping[str, float],
    client: anthropic.Anthropic | None = None,
    model: str = DEFAULT_MODEL,
    web_search: bool = True,
) -> str:
    client = client or anthropic.Anthropic()
    user = build_user_prompt(fixture, prediction, elo)
    tools = [{"type": "web_search_20250305", "name": "web_search"}] if web_search else []
    try:
        resp = client.messages.create(
            model=model,
            max_tokens=400,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user}],
            tools=tools,
        )
    except Exception as e:
        log.warning("Rationale failed for %s: %s", fixture.fixture_id, e)
        return ""
    parts = []
    for block in resp.content:
        text = getattr(block, "text", None)
        if text:
            parts.append(text)
    return " ".join(parts).strip()


def generate_all(
    fixtures: list[Fixture],
    predictions: list[Prediction],
    elo: Mapping[str, float],
    client: anthropic.Anthropic | None = None,
    web_search: bool = True,
) -> dict[str, str]:
    """Per-fixture rationale; returns {fixture_id: text}."""
    client = client or anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    pred_by_id = {p.fixture_id: p for p in predictions}
    out: dict[str, str] = {}
    for f in fixtures:
        if f.fixture_id not in pred_by_id or f.status == "FINISHED":
            continue
        out[f.fixture_id] = generate_rationale(
            f, pred_by_id[f.fixture_id], elo, client=client, web_search=web_search
        )
    return out
```

Note: the `web_search_20250305` tool ID and exact API surface should be verified against the current Anthropic Python SDK at implementation time — confirm with `claude-api` skill if uncertain.

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_rationale.py -v
```

Expected: 3 passed.

- [ ] **Step 5: Commit**

```bash
git add forecaster/rationale.py tests/test_rationale.py
git commit -m "feat(rationale): per-fixture Claude-written rationale"
```

---

## Task 14: CLI orchestration

Glue everything together: `python -m forecaster run` ingests, fits, predicts, picks, rationalizes, and publishes in one call.

**Files:**
- Create: `forecaster/cli.py`
- Create: `forecaster/__main__.py`
- Create: `tests/test_cli.py`

- [ ] **Step 1: Write the smoke test**

`tests/test_cli.py`:

```python
"""End-to-end pipeline smoke test."""
from __future__ import annotations

import datetime as dt
from unittest.mock import patch

import pandas as pd

from forecaster.cli import run_pipeline
from forecaster.schema import Fixture


def _fake_fixtures():
    return [
        Fixture(
            fixture_id="2026-06-11-MEX-RSA",
            utc_kickoff=dt.datetime(2026, 6, 11, 18, 0, tzinfo=dt.timezone.utc),
            home="MEX", away="RSA", venue_country="MEX",
            stage="GROUP", status="SCHEDULED",
            actual_home_goals=None, actual_away_goals=None,
        ),
    ]


def _fake_history():
    rows = []
    for i in range(50):
        rows.append({
            "date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=i),
            "home": "MEX" if i % 2 == 0 else "RSA",
            "away": "RSA" if i % 2 == 0 else "MEX",
            "home_goals": 2 if i % 2 == 0 else 0,
            "away_goals": 0 if i % 2 == 0 else 1,
            "neutral": True,
            "tournament": "Friendly",
        })
    return pd.DataFrame(rows)


def test_run_pipeline_produces_index_html(tmp_data_dir, monkeypatch):
    from forecaster import config
    monkeypatch.setattr(config, "DOCS_DIR", tmp_data_dir.parent / "docs")
    monkeypatch.setattr(config, "DOCS_API_DIR", tmp_data_dir.parent / "docs" / "api")
    config.ensure_dirs()

    seed = {"MEX": 1825, "RSA": 1620}

    with (
        patch("forecaster.cli.fetch_fixtures", return_value=_fake_fixtures()),
        patch("forecaster.cli.fetch_historical_results", return_value=_fake_history()),
        patch("forecaster.cli.init_elo", return_value=seed),
        patch("forecaster.cli.generate_all", return_value={"2026-06-11-MEX-RSA": "test rationale"}),
    ):
        run_pipeline(skip_rationale=False)

    assert (config.DOCS_DIR / "index.html").exists()
    assert (config.DOCS_DIR / "prompt-pack.md").exists()
    assert (config.DOCS_API_DIR / "2026-06-11-MEX-RSA.json").exists()
```

- [ ] **Step 2: Implement `forecaster/cli.py`**

```python
"""Pipeline orchestration: ingest → ratings → model → picks → rationale → publish."""
from __future__ import annotations

import argparse
import datetime as dt
import logging
import os
import sys

import pandas as pd

from forecaster import config
from forecaster.ingest import (
    fetch_fixtures,
    fetch_historical_results,
    write_fixtures_parquet,
)
from forecaster.model import fit_params, predict_all
from forecaster.picks import enrich_predictions
from forecaster.publish import (
    write_html_dashboard,
    write_per_fixture_json,
    write_prompt_pack,
)
from forecaster.rationale import generate_all
from forecaster.ratings import (
    init_elo,
    update_elo_from_results,
    write_elo_parquet,
)


def _has_match_in_next_24h(fixtures: list, now: dt.datetime) -> bool:
    return any(
        now <= f.utc_kickoff <= now + dt.timedelta(days=1)
        for f in fixtures
        if f.status == "SCHEDULED"
    )


def run_pipeline(skip_rationale: bool = False, force: bool = False) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    log = logging.getLogger("forecaster")

    config.ensure_dirs()

    log.info("ingest: fixtures")
    fixtures = fetch_fixtures()
    write_fixtures_parquet(fixtures)

    now = dt.datetime.now(dt.timezone.utc)
    is_match_day = _has_match_in_next_24h(fixtures, now)
    is_scheduled_full_run = now.hour in (6, 18)
    if not (is_match_day or is_scheduled_full_run or force):
        log.info("Quiet hour and no fixture in next 24h — exiting early.")
        return

    log.info("ingest: historical")
    history = fetch_historical_results()

    log.info("ratings")
    seed = init_elo()
    # Update Elo with WC results that have already finished, in chronological order.
    finished = pd.DataFrame([{
        "date": pd.Timestamp(f.utc_kickoff),
        "home": f.home, "away": f.away,
        "home_goals": f.actual_home_goals, "away_goals": f.actual_away_goals,
        "neutral": f.venue_country not in {f.home, f.away},
    } for f in fixtures if f.status == "FINISHED"])
    if len(finished):
        seed = update_elo_from_results(seed, finished, k=30.0)
    # Combine with full history for the fit but use updated seed for prediction.
    elo = update_elo_from_results(
        seed,
        pd.concat([history, finished], ignore_index=True) if len(finished) else history,
        k=15.0,   # smaller K for old matches to avoid overfitting recent
    )
    write_elo_parquet(elo)

    log.info("model: fit")
    params = fit_params(history, elo, ref_date=pd.Timestamp(now.date()))
    log.info("fitted params: %s", params)

    log.info("model: predict")
    predictions = predict_all(fixtures, elo, params)

    log.info("picks: EV optimisation")
    predictions = enrich_predictions(predictions)

    if skip_rationale or not os.environ.get("ANTHROPIC_API_KEY"):
        log.info("Skipping rationale (skip_rationale=%s, key set=%s)",
                 skip_rationale, bool(os.environ.get("ANTHROPIC_API_KEY")))
        rationale = {}
    else:
        log.info("rationale")
        rationale = generate_all(fixtures, predictions, elo)

    log.info("publish")
    write_per_fixture_json(fixtures, predictions, rationale)
    write_html_dashboard(fixtures, predictions, rationale)
    write_prompt_pack(fixtures, predictions, rationale)
    log.info("done; outputs in %s", config.DOCS_DIR)


def main() -> int:
    parser = argparse.ArgumentParser(prog="forecaster")
    sub = parser.add_subparsers(dest="cmd", required=True)
    run = sub.add_parser("run", help="Run the full pipeline")
    run.add_argument("--skip-rationale", action="store_true",
                     help="Skip the LLM rationale step")
    run.add_argument("--force", action="store_true",
                     help="Run even on quiet hours of a non-match day")
    args = parser.parse_args()
    if args.cmd == "run":
        run_pipeline(skip_rationale=args.skip_rationale, force=args.force)
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 3: Add `forecaster/__main__.py`**

```python
from forecaster.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
```

- [ ] **Step 4: Run the test**

```bash
pytest tests/test_cli.py -v
```

Expected: 1 passed (takes ~10–15 s for the synthetic fit).

- [ ] **Step 5: Smoke-test the CLI locally**

```bash
python -m forecaster run --skip-rationale --force
ls -la docs/
```

Expected: `docs/index.html`, `docs/prompt-pack.md`, `docs/api/*.json` exist. Open `docs/index.html` in Chrome and visually check the layout.

- [ ] **Step 6: Commit**

```bash
git add forecaster/cli.py forecaster/__main__.py tests/test_cli.py
git commit -m "feat(cli): pipeline orchestration + match-day gating"
```

---

## Task 15: GitHub Actions workflow

**Pre-requisite:** ask Stefan for his GitHub username so the README and Pages URL can be set correctly.

**Files:**
- Create: `.github/workflows/forecast.yml`
- Modify: `README.md` (add live URL section)

- [ ] **Step 1: Write the workflow**

`.github/workflows/forecast.yml`:

```yaml
name: forecast

on:
  schedule:
    # Hourly. The pipeline self-gates on match-day status.
    - cron: "0 * * * *"
  workflow_dispatch:

permissions:
  contents: write
  pages: write
  id-token: write

concurrency:
  group: forecast
  cancel-in-progress: false

jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install
        run: |
          python -m pip install --upgrade pip
          pip install -e .

      - name: Run pipeline
        env:
          FOOTBALL_DATA_API_KEY: ${{ secrets.FOOTBALL_DATA_API_KEY }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: python -m forecaster run

      - name: Commit data + docs
        run: |
          git config user.name "forecaster-bot"
          git config user.email "actions@github.com"
          git add data docs
          if git diff --staged --quiet; then
            echo "no changes"
          else
            git commit -m "ci: pipeline run $(date -u +%Y-%m-%dT%H:%MZ)"
            git push
          fi

  deploy-pages:
    needs: run
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - uses: actions/checkout@v4
        with:
          ref: ${{ github.ref }}
      - uses: actions/configure-pages@v5
      - uses: actions/upload-pages-artifact@v3
        with:
          path: ./docs
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Update the README with the live URL**

Add a "Live" section near the top of `README.md`:

```markdown
## Live

Dashboard: `https://<GITHUB_USERNAME>.github.io/<REPO>/`
Prompt pack: `https://<GITHUB_USERNAME>.github.io/<REPO>/prompt-pack.md`
```

(Replace placeholders once Stefan provides the username/repo.)

- [ ] **Step 3: Commit the workflow**

```bash
git add .github/workflows/forecast.yml README.md
git commit -m "ci: hourly GitHub Actions pipeline + Pages deploy"
```

- [ ] **Step 4: One-time GitHub setup (Stefan, manual)**

- [ ] Create a public repo on GitHub.
- [ ] Push the local repo: `git remote add origin <url> && git push -u origin main`
- [ ] In repo Settings → Pages: Source = "GitHub Actions".
- [ ] In repo Settings → Secrets and variables → Actions: add `FOOTBALL_DATA_API_KEY` and `ANTHROPIC_API_KEY`.
- [ ] Trigger the workflow manually from Actions tab to verify it runs end-to-end.

---

## Task 16: Backtest harness (sanity check before kickoff)

Re-predicts every match of Euro 2024 and Copa América 2024 using only data available *before each match*, then reports W/D/L Brier score, log-loss, and Forecaster-rule total points. Ensures the model is at least as good as a pure-Elo baseline.

**Files:**
- Create: `forecaster/backtest.py`
- Create: `tests/test_backtest.py`

- [ ] **Step 1: Write the failing test (small synthetic backtest)**

`tests/test_backtest.py`:

```python
"""Backtest harness."""
from __future__ import annotations

import datetime as dt

import pandas as pd

from forecaster.backtest import backtest_brier, run_backtest


def test_brier_is_zero_for_perfect_predictions():
    actuals = ["W", "L", "D"]
    probs = [(1, 0, 0), (0, 0, 1), (0, 1, 0)]
    assert backtest_brier(actuals, probs) == 0.0


def test_brier_increases_for_worse_predictions():
    actuals = ["W"]
    perfect = backtest_brier(actuals, [(1, 0, 0)])
    uniform = backtest_brier(actuals, [(1/3, 1/3, 1/3)])
    assert uniform > perfect


def test_run_backtest_reports_forecaster_points(tmp_path):
    rows = []
    for i in range(80):
        rows.append({
            "date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=i),
            "home": "MEX" if i % 2 == 0 else "RSA",
            "away": "RSA" if i % 2 == 0 else "MEX",
            "home_goals": 2 if i % 2 == 0 else 0,
            "away_goals": 0 if i % 2 == 0 else 1,
            "neutral": True,
            "tournament": "Friendly",
        })
    history = pd.DataFrame(rows)
    elo = {"MEX": 1800, "RSA": 1600}

    metrics = run_backtest(history, elo, holdout_after=pd.Timestamp("2024-02-15"))
    assert "brier" in metrics
    assert "log_loss" in metrics
    assert "forecaster_points_per_match" in metrics
    assert metrics["n_matches"] >= 1
```

- [ ] **Step 2: Run tests, expect failures**

```bash
pytest tests/test_backtest.py -v
```

Expected: 3 failures.

- [ ] **Step 3: Implement `forecaster/backtest.py`**

```python
"""Backtest harness for sanity-checking the model."""
from __future__ import annotations

import datetime as dt
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

    # Walk forward: for each test match, fit on data up to the day before, predict.
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
        # Update rolling Elo with the now-revealed result.
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
```

- [ ] **Step 4: Run tests**

```bash
pytest tests/test_backtest.py -v
```

Expected: 3 passed.

- [ ] **Step 5: Run a real backtest**

```bash
python -c "
import pandas as pd
from forecaster.backtest import run_backtest
from forecaster.ingest import fetch_historical_results
from forecaster.ratings import init_elo

history = fetch_historical_results()
elo = init_elo()
# Holdout: Euro 2024 + Copa America 2024 (June onwards).
m = run_backtest(history, elo, holdout_after=pd.Timestamp('2024-06-01'))
print(m)
"
```

Expected: a dict with `brier`, `log_loss`, `forecaster_points_per_match`, `n_matches`.

**Acceptance:** `forecaster_points_per_match` should be ≥ 1.5 (uniform-random would be ~1.0). If lower, investigate before kickoff — most likely culprits are country-name mapping gaps in `country_to_tla` or stale Elo seed.

- [ ] **Step 6: Commit**

```bash
git add forecaster/backtest.py tests/test_backtest.py
git commit -m "feat(backtest): walk-forward backtest harness with Brier + points/match"
```

---

## Final acceptance checklist

- [ ] `pytest -v` runs green (~25–30 tests across modules).
- [ ] `python -m forecaster run --skip-rationale --force` produces `docs/index.html`, `docs/prompt-pack.md`, `docs/api/*.json` locally.
- [ ] `docs/index.html` opens correctly in Chrome on iOS (test on Stefan's iPhone) — try "Add to Home Screen".
- [ ] **[Open in Claude Chat]** button on a fixture card copies the briefing and opens claude.ai. Paste it; verify Claude can answer "should I pick 2-1 or 1-1?" using the supplied numbers.
- [ ] `prompt-pack.md` contains every upcoming fixture and the scoring rule.
- [ ] Backtest on Euro 2024 + Copa 2024 reports `forecaster_points_per_match ≥ 1.5` and `brier < 0.3`.
- [ ] GitHub Actions runs successfully end-to-end on `workflow_dispatch`.
- [ ] GitHub Pages serves the dashboard at the configured URL.
