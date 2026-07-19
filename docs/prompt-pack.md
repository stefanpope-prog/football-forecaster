# Football Forecaster - Prompt Pack

Generated 2026-07-19 06:36 UTC. Paste this whole document into Claude Chat, then ask any question about the upcoming fixtures.

## System prompt for Claude

You are advising me on a Kicktipp-style football prediction pool. **Trust the numbers below as ground truth - do not recompute Poisson math.** Your job is to help me reason about *which scoreline to submit* given the pre-computed probability distribution and the scoring rule.

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


### ESP vs ARG - Sun 19 Jul 19:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 2.99 pts)
- **W / D / L:** 11% / 38% / 52%
- **lambda_home / lambda_away:** 0.28 / 0.94
- **Top scorelines:**
  - 0:0 (29%)
  - 0:1 (28%)
  - 0:2 (13%)
  - 1:0 (8%)

- **Why:** ARG is the favourite. Recent form (last 5): ESP 2 wins, 3 draws; ARG 4 wins, 1 loss. Past 3 meetings: ESP won 2, ARG won 1. Model gives ESP 11%, draw 38%, ARG 52%.

