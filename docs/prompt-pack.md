# Football Forecaster - Prompt Pack

Generated 2026-07-14 21:04 UTC. Paste this whole document into Claude Chat, then ask any question about the upcoming fixtures.

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


### FRA vs ESP - Tue 14 Jul 19:00 UTC

- **Stage:** SF
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 2.56 pts)
- **W / D / L:** 56% / 24% / 19%
- **lambda_home / lambda_away:** 1.89 / 1.04
- **Top scorelines:**
  - 1:1 (12%)
  - 2:1 (10%)
  - 2:0 (10%)
  - 1:0 (9%)

- **Why:** slight edge to FRA. Recent form (last 5): FRA 3 wins, 1 draw, 1 loss; ESP 2 wins, 3 draws. Past 3 meetings: FRA won 1, ESP won 2. Model gives FRA 56%, draw 24%, ESP 19%.


### ENG vs ARG - Wed 15 Jul 19:00 UTC

- **Stage:** SF
- **Recommended pick (EV-optimal):** 0-2 (EV ~ 3.37 pts)
- **W / D / L:** 6% / 14% / 80%
- **lambda_home / lambda_away:** 0.70 / 2.81
- **Top scorelines:**
  - 0:2 (12%)
  - 0:3 (11%)
  - 1:2 (8%)
  - 0:1 (8%)

- **Why:** ARG is the favourite. Recent form (last 5): ENG 3 wins, 1 draw, 1 loss; ARG 4 wins, 1 loss. Past 3 meetings: ENG won 2, drew 1. Model gives ENG 6%, draw 14%, ARG 80%.


### None vs None - Sat 18 Jul 21:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 1.87 pts)
- **W / D / L:** 36% / 28% / 36%
- **lambda_home / lambda_away:** 1.40 / 1.40
- **Top scorelines:**
  - 1:1 (13%)
  - 2:1 (8%)
  - 1:2 (8%)
  - 1:0 (7%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 36%, draw 28%, None 36%.


### None vs None - Sun 19 Jul 19:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 1.87 pts)
- **W / D / L:** 36% / 28% / 36%
- **lambda_home / lambda_away:** 1.40 / 1.40
- **Top scorelines:**
  - 1:1 (13%)
  - 2:1 (8%)
  - 1:2 (8%)
  - 1:0 (7%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 36%, draw 28%, None 36%.

