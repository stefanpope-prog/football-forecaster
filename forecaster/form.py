"""Deterministic 'Why' paragraph per fixture, built from on-disk data only."""
from __future__ import annotations

from typing import Mapping

import pandas as pd

from forecaster.schema import Fixture, Prediction


def last_n_results(history: pd.DataFrame, team: str, n: int = 5) -> pd.DataFrame:
    """Return the team's last n matches (any side), most-recent-first."""
    df = history[(history["home"] == team) | (history["away"] == team)].copy()
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date", ascending=False).head(n)
    return df


def _form_letters(rows: pd.DataFrame, team: str) -> str:
    """Return e.g. 'WWDLW' (most recent first)."""
    out = []
    for _, r in rows.iterrows():
        is_home = r["home"] == team
        team_goals = r["home_goals"] if is_home else r["away_goals"]
        opp_goals = r["away_goals"] if is_home else r["home_goals"]
        if team_goals > opp_goals:
            out.append("W")
        elif team_goals < opp_goals:
            out.append("L")
        else:
            out.append("D")
    return "".join(out)


def _head_to_head(history: pd.DataFrame, home: str, away: str, n: int = 3) -> str | None:
    h2h = history[
        ((history["home"] == home) & (history["away"] == away))
        | ((history["home"] == away) & (history["away"] == home))
    ].copy()
    h2h["date"] = pd.to_datetime(h2h["date"])
    h2h = h2h.sort_values("date", ascending=False).head(n)
    if len(h2h) == 0:
        return None
    home_wins = away_wins = draws = 0
    for _, r in h2h.iterrows():
        h_is_home_team = r["home"] == home
        h_goals = r["home_goals"] if h_is_home_team else r["away_goals"]
        a_goals = r["away_goals"] if h_is_home_team else r["home_goals"]
        if h_goals > a_goals:
            home_wins += 1
        elif h_goals < a_goals:
            away_wins += 1
        else:
            draws += 1
    parts = []
    if home_wins:
        parts.append(f"{home} won {home_wins}")
    if draws:
        parts.append(f"drew {draws}")
    if away_wins:
        parts.append(f"{away} won {away_wins}")
    return f"Past {len(h2h)} meetings: " + ", ".join(parts)


def _form_phrase(letters: str) -> str:
    """Turn 'WDWDW' into '3 wins, 2 draws'; 'DDDDD' into 'drew all 5'."""
    if not letters:
        return "no recent matches"
    n = len(letters)
    w, d, l = letters.count("W"), letters.count("D"), letters.count("L")
    if w == n:
        return f"won all {n}"
    if d == n:
        return f"drew all {n}"
    if l == n:
        return f"lost all {n}"
    parts = []
    if w:
        parts.append(f"{w} win{'s' if w != 1 else ''}")
    if d:
        parts.append(f"{d} draw{'s' if d != 1 else ''}")
    if l:
        parts.append(f"{l} loss{'es' if l != 1 else ''}")
    return ", ".join(parts)


def _edge_phrase(home: str, away: str, gap: float) -> str:
    """Translate Elo gap into plain football language."""
    abs_gap = abs(gap)
    favourite = home if gap > 0 else away
    if abs_gap < 30:
        return f"{home} and {away} look evenly matched"
    if abs_gap < 100:
        return f"slight edge to {favourite}"
    if abs_gap < 200:
        return f"{favourite} is the favourite"
    if abs_gap < 400:
        return f"{favourite} is the clear favourite"
    return f"{favourite} is the heavy favourite"


def build_form_summary(
    fixture: Fixture,
    prediction: Prediction,
    elo: Mapping[str, float],
    history: pd.DataFrame,
) -> str:
    """Compose a short factual paragraph for the dashboard 'Why' section."""
    home, away = fixture.home, fixture.away
    elo_h = elo.get(home, 1500)
    elo_a = elo.get(away, 1500)
    elo_gap = elo_h - elo_a

    home_form = _form_letters(last_n_results(history, home, n=5), home)
    away_form = _form_letters(last_n_results(history, away, n=5), away)

    edge = _edge_phrase(home, away, elo_gap)

    sg = prediction.score_grid
    wdl = (
        f"Model gives {home} {sg.win_prob()*100:.0f}%, "
        f"draw {sg.draw_prob()*100:.0f}%, "
        f"{away} {sg.loss_prob()*100:.0f}%"
    )

    pieces = [
        f"{edge}.",
        f"Recent form (last 5): {home} {_form_phrase(home_form)}; "
        f"{away} {_form_phrase(away_form)}.",
    ]
    h2h = _head_to_head(history, home, away)
    if h2h:
        pieces.append(h2h + ".")
    pieces.append(wdl + ".")
    if fixture.venue_country == home:
        pieces.append(f"{home} plays at home.")

    return " ".join(pieces)


def summarise_all(
    fixtures: list[Fixture],
    predictions: list[Prediction],
    elo: Mapping[str, float],
    history: pd.DataFrame,
) -> dict[str, str]:
    """Build form-summary text for every scheduled fixture."""
    pred_by_id = {p.fixture_id: p for p in predictions}
    out: dict[str, str] = {}
    for f in fixtures:
        if f.fixture_id not in pred_by_id or f.status == "FINISHED":
            continue
        out[f.fixture_id] = build_form_summary(
            f, pred_by_id[f.fixture_id], elo, history
        )
    return out
