# Football Forecaster

2026 FIFA World Cup match forecaster. Dixon-Coles bivariate Poisson with Elo-derived strengths. Static dashboard on GitHub Pages, paste-into-Claude-Chat prompt pack for mobile.

See `docs/superpowers/specs/2026-06-11-football-forecaster-design.md` for the design.

## Live

Dashboard: https://stefanpope-prog.github.io/football-forecaster/
Prompt pack: https://stefanpope-prog.github.io/football-forecaster/prompt-pack.md

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
export FOOTBALL_DATA_API_KEY=...      # free at football-data.org
python -m forecaster run
```

Outputs land in `docs/`. Run `pytest` for tests.

For deeper analysis, the dashboard's "Open in Claude Chat" button copies a self-contained briefing to the clipboard and opens claude.ai — no paid API needed.
