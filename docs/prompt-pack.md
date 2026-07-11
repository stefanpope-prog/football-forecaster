# Football Forecaster - Prompt Pack

Generated 2026-07-11 06:27 UTC. Paste this whole document into Claude Chat, then ask any question about the upcoming fixtures.

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


### NOR vs ENG - Sat 11 Jul 21:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 0-8 (EV ~ 4.77 pts)
- **W / D / L:** 0% / 0% / 100%
- **lambda_home / lambda_away:** 0.14 / 13.80
- **Top scorelines:**
  - 0:8 (42%)
  - 0:7 (24%)
  - 0:6 (12%)
  - 1:8 (6%)

- **Why:** ENG is the clear favourite. Recent form (last 5): NOR 2 wins, 2 draws, 1 loss; ENG 3 wins, 1 draw, 1 loss. Past 3 meetings: drew 1, ENG won 2. Model gives NOR 0%, draw 0%, ENG 100%.


### ARG vs SUI - Sun 12 Jul 01:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 5-0 (EV ~ 4.07 pts)
- **W / D / L:** 99% / 1% / 0%
- **lambda_home / lambda_away:** 6.01 / 0.33
- **Top scorelines:**
  - 6:0 (14%)
  - 5:0 (14%)
  - 7:0 (12%)
  - 4:0 (11%)

- **Why:** ARG is the clear favourite. Recent form (last 5): ARG 4 wins, 1 loss; SUI 2 wins, 2 draws, 1 loss. Past 3 meetings: ARG won 2, drew 1. Model gives ARG 99%, draw 1%, SUI 0%.


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


### None vs None - Wed 15 Jul 19:00 UTC

- **Stage:** SF
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 1.87 pts)
- **W / D / L:** 36% / 28% / 36%
- **lambda_home / lambda_away:** 1.40 / 1.40
- **Top scorelines:**
  - 1:1 (13%)
  - 2:1 (8%)
  - 1:2 (8%)
  - 1:0 (7%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 36%, draw 28%, None 36%.


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

