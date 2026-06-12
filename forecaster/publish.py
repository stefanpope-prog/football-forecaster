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
