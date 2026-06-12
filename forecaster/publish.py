"""Publish predictions: per-fixture JSON, HTML dashboard, prompt pack."""
from __future__ import annotations

import datetime as dt
import json
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Iterable

from jinja2 import Environment, FileSystemLoader, select_autoescape

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
    top_max = p.top_scorelines[0][1] if p.top_scorelines else 1.0
    top = [
        {
            "h": s[0], "a": s[1],
            "pct": _percent(prob),
            "bar_pct": min(100, _percent(prob / max(top_max, 1e-6))),
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
                grid_lines.append(f"- {i}:{j} -> {prob*100:.1f}%")
    grid_block = "\n".join(grid_lines)
    return f"""You are advising me on a Kicktipp-style prediction. Scoring rule:
- Correct outcome: +3
- Each correct team score: +1
- Correct goal difference: +1
- Max per match: 6

Match: **{f.home} vs {f.away}** ({f.stage}, {f.utc_kickoff.isoformat()})

Pre-computed Dixon-Coles probabilities (trust these - don't recompute):
- lambda home (expected goals): {p.lambda_home:.2f}
- lambda away (expected goals): {p.lambda_away:.2f}
- W / D / L: {sg.win_prob()*100:.1f}% / {sg.draw_prob()*100:.1f}% / {sg.loss_prob()*100:.1f}%

Likely scorelines (>= 0.5%):
{grid_block}

Recommended pick (EV-optimal): **{p.recommended_pick[0]}-{p.recommended_pick[1]}** (EV ~ {p.expected_points:.2f} pts)

Form context (from the model):
{rationale or '(no form summary)'}

Your job:
1. If you have web search, look up the latest injury/lineup news, weather, and any tactical context for this match.
2. Help me decide which scoreline to actually submit. If I'm risk-averse, lean toward higher-probability picks; if I'm chasing the leaderboard, suggest a higher-variance gamble.
3. **Trust the probability numbers above as ground truth - don't recompute them.** Use qualitative inputs only as caveats ("model doesn't price in Mbappe being out").
"""


def _group_by_day(
    fixtures: Iterable[Fixture], now_utc: dt.datetime
) -> tuple[list[dict], list[Fixture]]:
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
        if d == today:
            label = "TODAY"
        elif d == today + dt.timedelta(days=1):
            label = "TOMORROW"
        else:
            label = d.strftime("%A %d %b").upper()
        days.append({
            "date": d, "label": label,
            "fixtures": sorted(upcoming[d], key=lambda f: f.utc_kickoff),
        })
    return days, sorted(past, key=lambda f: f.utc_kickoff, reverse=True)


def write_html_dashboard(
    fixtures: list[Fixture],
    predictions: list[Prediction],
    rationale: dict[str, str],
    now_utc: dt.datetime | None = None,
) -> Path:
    """Render `docs/index.html` from the templates."""
    from forecaster.picks import score_pick

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
        actual = (f.actual_home_goals, f.actual_away_goals)
        pts = score_pick(p.recommended_pick, actual)
        pick_sign = (p.recommended_pick[0] > p.recommended_pick[1]) - (p.recommended_pick[0] < p.recommended_pick[1])
        actual_sign = (actual[0] > actual[1]) - (actual[0] < actual[1])
        if pick_sign == actual_sign:
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
        accuracy=f"{n_outcome_correct} of {len(past_cards)}" if past_cards else "-",
        upcoming_days=days_view,
        past_cards=past_cards,
        accuracy_outcome=accuracy_outcome,
        total_points=total_points,
        briefings_json=json.dumps(briefings),
    )
    config.DOCS_DIR.mkdir(parents=True, exist_ok=True)
    out = config.DOCS_DIR / "index.html"
    out.write_text(html)
    shutil.copy(config.TEMPLATES_DIR / "style.css", config.DOCS_DIR / "style.css")
    return out
