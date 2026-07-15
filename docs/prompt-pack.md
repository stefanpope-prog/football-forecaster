# Football Forecaster - Prompt Pack

Generated 2026-07-15 18:14 UTC. Paste this whole document into Claude Chat, then ask any question about the upcoming fixtures.

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


### FRA vs None - Sat 18 Jul 21:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 4.97 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 14.20 / 0.02
- **Top scorelines:**
  - 8:0 (49%)
  - 7:0 (27%)
  - 6:0 (14%)
  - 5:0 (6%)

- **Why:** FRA is the heavy favourite. Recent form (last 5): FRA 3 wins, 1 draw, 1 loss; None no recent matches. Model gives FRA 100%, draw 0%, None 0%.


### ESP vs None - Sun 19 Jul 19:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 4.87 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 12.82 / 0.02
- **Top scorelines:**
  - 8:0 (44%)
  - 7:0 (28%)
  - 6:0 (15%)
  - 5:0 (7%)

- **Why:** ESP is the heavy favourite. Recent form (last 5): ESP 2 wins, 3 draws; None no recent matches. Model gives ESP 100%, draw 0%, None 0%.

