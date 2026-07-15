# Football Forecaster - Prompt Pack

Generated 2026-07-15 04:11 UTC. Paste this whole document into Claude Chat, then ask any question about the upcoming fixtures.

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


### ENG vs ARG - Wed 15 Jul 19:00 UTC

- **Stage:** SF
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.14 pts)
- **W / D / L:** 9% / 35% / 56%
- **lambda_home / lambda_away:** 0.26 / 1.04
- **Top scorelines:**
  - 0:1 (29%)
  - 0:0 (27%)
  - 0:2 (15%)
  - 1:0 (7%)

- **Why:** ARG is the favourite. Recent form (last 5): ENG 3 wins, 1 draw, 1 loss; ARG 4 wins, 1 loss. Past 3 meetings: ENG won 2, drew 1. Model gives ENG 9%, draw 35%, ARG 56%.


### None vs None - Sat 18 Jul 21:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 3.01 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Sun 19 Jul 19:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 3.01 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.

