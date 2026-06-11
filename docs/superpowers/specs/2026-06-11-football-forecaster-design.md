# Football Forecaster — Design

**Date:** 2026-06-11
**Status:** Approved (sections 1–3), ready for implementation plan
**Owner:** Stefan

## 1. Goal

Forecast every match of the 2026 FIFA World Cup well enough to win a Kicktipp-style office pool against football-nerd colleagues. Output is a calibrated scoreline distribution per match, plus an expected-value-optimal pick under the pool's scoring rule (default Kicktipp: 4 pts exact score / 3 pts correct goal difference / 2 pts correct winner).

The forecaster does not need to be state-of-the-art. It needs to be:

- **Better than gut feel.** A Dixon-Coles bivariate Poisson model fit on historical internationals beats human guessers in published evaluations.
- **Always available on Stefan's iPhone.** Including during a vacation week with only free Claude Chat available.
- **Cheap to run.** Free APIs only, free hosting, free CI.
- **Maintainable in evenings.** ~1,500–2,500 LOC of Python, no ML training infrastructure.

## 2. Non-goals

- Not modelling tournament progression (group winners, knockout simulation, trophy odds). Defer to v2.
- Not building a paid data pipeline. Free public sources only.
- Not replacing the model with an LLM. The LLM writes rationale and answers what-ifs; it never overrides the math.
- Not a real-time in-play model. Predictions refresh hourly on match days; in-play probability shifts are out of scope.
- Not multi-tournament. Built for the 2026 World Cup; can be generalized later.

## 3. Architecture

```
   GitHub Actions cron (twice daily; hourly on match days)
              │
              ▼
   forecaster pipeline (Python package)
              │
              │  ingest → ratings → model → picks → rationale → publish
              │
              ├──► docs/index.html      ─────► GitHub Pages ─► 📱 phone (read)
              ├──► docs/prompt-pack.md  ─────► GitHub Pages ─► 📱 paste into Claude Chat
              └──► docs/api/<id>.json   ─────► GitHub Pages ─► ad-hoc / per-match
```

### 3.1 Modules

| Module | Responsibility | Output |
|---|---|---|
| `ingest` | Fetch fixtures + final scores + historical match corpus | `data/fixtures.parquet`, `data/results.parquet`, `data/historical.parquet` |
| `ratings` | Maintain Elo per national team; initialized from public feed, updated as WC matches finish | `data/elo.parquet` |
| `model` | Fit Dixon-Coles params on time-decayed history; predict 8×8 scoreline grid per fixture | `data/model_params.json`, `data/predictions.parquet` |
| `picks` | Compute EV-optimal Kicktipp pick, top-3 most-likely scorelines, W/D/L probabilities | columns added to `predictions.parquet` |
| `rationale` | LLM call producing 3–5 sentence explanation per fixture, citing form / injuries / weather | `data/rationale.parquet` |
| `publish` | Render `index.html`, `prompt-pack.md`, per-match JSON | `docs/*` |

Each module communicates via DataFrames / dataclasses on disk. No shared mutable state. Any module can be re-run independently.

### 3.2 Boundaries

- **Pipeline ↔ dashboard:** the dashboard reads `docs/*` only. A broken dashboard never blocks predictions.
- **Pipeline ↔ Claude Chat:** Claude Chat (free tier) consumes `prompt-pack.md` and per-fixture briefings. It treats the pre-computed grid as ground truth; it does not recompute Poisson math.
- **Pipeline ↔ network:** isolated to `ingest` and `rationale`. Other modules are pure functions of on-disk inputs, so they're trivially testable without network.

## 4. Data sources

| Source | Use | Auth | Refresh |
|---|---|---|---|
| football-data.org (free tier) | Upcoming WC fixtures + final scores | Free API key | Every run |
| OpenFootball (GitHub JSON) | Fixtures/results fallback | None | Every run |
| Kaggle "International football results 1872–present" (Mart Jürisoo) | Historical corpus (~45k matches) for Dixon-Coles fit | Vendored CSV at repo init | Once at start, refreshed weekly |
| eloratings.net | Initial Elo per national team | None (HTML scrape, one page) | Once at start; we maintain ourselves thereafter |
| Anthropic API (local) / Claude Chat (mobile) web search | Injuries, suspensions, lineups, weather | API key (local only) | Per fixture, near kickoff |

Two fixture sources guarantees graceful degradation if one rate-limits or breaks.

## 5. Model

### 5.1 Dixon-Coles bivariate Poisson with Elo-derived strengths

For a fixture between teams A (notional home) and B (notional away):

1. **Expected goals from Elo:**

   ```
   λ_A = base * 10^((Elo_A − Elo_B) / 400) * home_adv_A
   λ_B = base * 10^((Elo_B − Elo_A) / 400) * home_adv_B
   ```

   `base` (≈ 1.4 for international football), `home_adv_A`, and `home_adv_B` are fitted from history. For neutral WC venues `home_adv ≈ 1`, but matches in a host country (USA, Canada, Mexico) for that country's team get a measurable boost.

2. **Score grid:** 8×8 matrix `P(i, j) = Poisson(i; λ_A) * Poisson(j; λ_B)` for i, j ∈ {0..7}. Truncating at 7 covers >99.9% of mass for international football.

3. **Dixon-Coles low-score correction:** multiply the four cells `{(0,0), (1,0), (0,1), (1,1)}` by τ-correction terms parameterized by ρ, then renormalize the grid. This corrects the well-documented under-prediction of draws by independent Poisson.

4. **Time-decay weighting in the fit:** each historical match contributes weight `exp(-ξ * days_ago)` to the likelihood. ξ chosen via cross-validation on past tournaments; expected to be ≈ 0.0019 (half-life ~1 year).

### 5.2 Outputs per fixture

- 8×8 scoreline grid (probabilities)
- W/D/L probabilities (sums of the relevant cells)
- λ_A, λ_B (for explanation/debugging)
- Top-3 most-likely scorelines

### 5.3 EV-optimal Kicktipp pick

Given pool scoring rule `points(predicted, actual)`:

```
EV(i, j) = Σ over (a, b) in 8×8 grid:  P(a, b) * points((i, j), (a, b))
```

Pick `(i*, j*) = argmax EV(i, j)`. Default scoring is Kicktipp (4/3/2); the rule is configurable so other pools can be supported by changing one function.

This is the colleague-beating bit. For evenly matched fixtures, the EV-optimal pick is often slightly different from the modal scoreline (e.g. 2-1 over 1-0) because it covers more near-miss probability mass.

## 6. Outputs

### 6.1 Static dashboard — `docs/index.html`

Mobile-first HTML, no JS framework, dark-mode-aware via `prefers-color-scheme`. Optimized for Chrome on iOS (393pt portrait viewport, ≥44pt tap targets, Apple touch icon for "Add to Home Screen").

Layout:

```
TODAY
  ARG ── 18:00 UTC ── FRA
    My pick:        2 − 1   ★
    Most likely:    1 − 1   (12%)
    W / D / L:      48% / 27% / 25%
    Top scorelines: 1-1 12% / 2-1 10% / 1-0 9% / 2-2 7%
    Why: [3-5 sentences from `rationale`]
    [ Open in Claude Chat ]   [ Share ]

TOMORROW
  ...

PAST (collapsed)
  Model accuracy so far: 6 of last 8 outcomes correct.
  ...
```

The `[ Open in Claude Chat ]` button uses the iOS-Chrome-supported Clipboard API: copies a self-contained per-fixture briefing, then opens `claude.ai` in a new tab.

`last_updated` timestamp visible on the page.

### 6.2 Tournament-wide prompt pack — `docs/prompt-pack.md`

Single markdown file containing:

1. System prompt for Claude (treat numbers as ground truth; don't recompute).
2. Kicktipp scoring rule (or configured alternative).
3. For every fixture in the next ~7 days: scoreline grid (numeric), recommended pick, W/D/L probs, recent form summary, key injury/lineup notes, head-to-head.

Use case: paste once into Claude Chat on the plane, then chat through every match without further uploads.

### 6.3 Per-fixture JSON — `docs/api/<fixture_id>.json`

Same data as a card on `index.html`, machine-readable. For ad-hoc use (other tools, future v2 integrations).

## 7. Phone-side experience

### Mode A — passive read

Open Safari/Chrome bookmark. Static page loads instantly, works offline once cached. No Claude needed. Stefan's primary use case while on vacation.

### Mode B — interactive what-ifs

For follow-up questions ("what if Mbappé sits?", "argue 2-1 vs 1-1 with me"):

- Per-fixture: tap **[Open in Claude Chat]** → briefing copied → paste into Claude Chat.
- Tournament-wide: bookmark the prompt pack URL, copy on demand, paste once for the day.

The system prompt tells Claude to *use* the pre-computed grid, not recompute. This keeps free-tier message count low and answers numerically consistent with the model.

## 8. Hosting & automation

### 8.1 Repo

New **public** repo on Stefan's personal GitHub. Public is required for free GitHub Pages without GitHub Pro.

### 8.2 GitHub Pages

Pages serves `docs/` from the default branch. URL: `https://<handle>.github.io/football-forecaster/`.

### 8.3 GitHub Actions

Single workflow with a single hourly schedule (`cron: "0 * * * *"`). The pipeline starts with an "is today a match day?" check:

- **On match days** (any WC fixture scheduled in the next 24h): run the full pipeline.
- **On non-match days:** run the full pipeline only at 06:00 and 18:00 UTC; other hours exit early.

This gives hourly freshness when it matters and protects the free-tier API quota when nothing's happening.

Workflow steps: checkout → install Python deps → run pipeline → commit `data/*` and `docs/*` → push.

Secrets: `FOOTBALL_DATA_API_KEY`, `ANTHROPIC_API_KEY`. Both stored in GitHub Actions repo secrets.

### 8.4 Cost

Zero. Free APIs, free hosting, GitHub Actions free tier (well under the 2,000 minutes/month limit).

## 9. Project layout

```
football-forecaster/
├── .github/workflows/forecast.yml
├── forecaster/
│   ├── __init__.py
│   ├── ingest.py
│   ├── ratings.py
│   ├── model.py
│   ├── picks.py
│   ├── rationale.py
│   ├── publish.py
│   └── cli.py            # `python -m forecaster run`
├── tests/
│   ├── test_model.py     # known-input → known-output for Poisson + Dixon-Coles
│   ├── test_picks.py     # EV calculation against a hand-checked grid
│   └── test_publish.py   # HTML renders, prompt-pack contains required sections
├── data/                 # parquet + json, committed back by CI
├── docs/                 # GitHub Pages root
│   ├── index.html
│   ├── prompt-pack.md
│   ├── api/
│   ├── style.css
│   └── superpowers/specs/  # this design doc lives here
├── pyproject.toml
└── README.md
```

## 10. Testing strategy

- **Unit tests** for the math: Poisson probabilities, Dixon-Coles τ-correction, EV calculation against hand-computed examples.
- **Snapshot tests** for HTML/markdown rendering: small fixture set → expected output.
- **Backtest** at the end of each module milestone: re-predict the most recent completed international tournament (Euro 2024 or Copa América 2024) using only data available before each match. Report Brier score and log-loss against actuals; sanity-check vs. published Dixon-Coles benchmarks.
- **Live eval during the WC:** the dashboard's "Past" section shows actual vs. predicted, so we'll spot regressions in real time.

## 11. Risks & mitigations

| Risk | Mitigation |
|---|---|
| football-data.org rate-limits us | OpenFootball fallback; cache aggressively; only refresh fixtures, not history |
| Group stage starts before pipeline is ready | MVP scope is deliberately lean; modules can ship in stages — predictions before rationale, dashboard before prompt pack |
| Model is poorly calibrated for international football (vs. club football where Dixon-Coles is most validated) | Backtest on Euro 2024 / Copa 2024 before the WC. Decision threshold (Brier on W/D/L) to be set during backtest by comparing against (a) bookmaker-implied probabilities and (b) a pure-Elo baseline. If we can't beat the Elo baseline by a meaningful margin, fall back to pure Elo W/D/L and stop publishing exact-score picks. |
| LLM rationale invents facts | Rationale prompt is constrained to "explain *the model's* numbers using the provided form/injury data"; web search citations required |
| Stefan's vacation network is bad | Static page, offline-cacheable; prompt pack stored as plain markdown, paste-once design |
| GitHub Actions outage during tournament | Manual "Run workflow" button as fallback; pipeline can also be run locally and pushed by hand |
| Phone clipboard API quirks on iOS Chrome | Test on real device before vacation; fall back to a `<textarea>` you long-press to copy if needed |

## 12. Open decisions for plan/implementation

- Confirm Stefan's GitHub username (needed to set up the repo + Pages URL).
- Confirm the colleague pool's exact scoring rule. Default is Kicktipp 4/3/2; if different, swap in `picks.py::scoring_rule`.
- Pick the historical corpus version: vendor the Kaggle CSV at v1, or auto-fetch from a stable mirror. Vendoring is simpler and reproducible.

## 13. Out of scope for v1, candidates for v2+

- Monte Carlo tournament simulation (group standings, knockout bracket, trophy odds).
- Player-level features (Mbappé-out as a numeric input rather than a rationale caveat).
- Automated calibration monitoring with alerts.
- Multi-tournament generalization.
- Ensemble with a second model (e.g. xG-based or gradient boosting) for robustness.
