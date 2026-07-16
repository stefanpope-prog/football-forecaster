# Football Forecaster - Prompt Pack

Generated 2026-07-16 00:02 UTC. Paste this whole document into Claude Chat, then ask any question about the upcoming fixtures.

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


### FRA vs None - Sat 18 Jul 21:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 5.51 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 38.57 / 0.05
- **Top scorelines:**
  - 8:0 (76%)
  - 7:0 (16%)
  - 8:1 (4%)
  - 6:0 (3%)

- **Why:** FRA is the heavy favourite. Recent form (last 5): FRA 3 wins, 1 draw, 1 loss; None no recent matches. Model gives FRA 100%, draw 0%, None 0%.


### ESP vs None - Sun 19 Jul 19:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 5.46 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 34.81 / 0.06
- **Top scorelines:**
  - 8:0 (74%)
  - 7:0 (17%)
  - 8:1 (4%)
  - 6:0 (3%)

- **Why:** ESP is the heavy favourite. Recent form (last 5): ESP 2 wins, 3 draws; None no recent matches. Model gives ESP 100%, draw 0%, None 0%.

