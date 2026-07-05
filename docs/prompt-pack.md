# Football Forecaster - Prompt Pack

Generated 2026-07-05 14:55 UTC. Paste this whole document into Claude Chat, then ask any question about the upcoming fixtures.

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


### BRA vs NOR - Sun 05 Jul 20:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 5.10 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 19.98 / 0.10
- **Top scorelines:**
  - 8:0 (57%)
  - 7:0 (23%)
  - 6:0 (8%)
  - 8:1 (6%)

- **Why:** BRA is the heavy favourite. Recent form (last 5): BRA 3 wins, 1 draw, 1 loss; NOR 2 wins, 2 draws, 1 loss. Past 3 meetings: drew 1, NOR won 2. Model gives BRA 100%, draw 0%, NOR 0%.


### MEX vs ENG - Mon 06 Jul 00:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 0-3 (EV ~ 3.68 pts)
- **W / D / L:** 2% / 8% / 90%
- **lambda_home / lambda_away:** 0.56 / 3.53
- **Top scorelines:**
  - 0:3 (12%)
  - 0:4 (11%)
  - 0:2 (11%)
  - 0:5 (8%)

- **Why:** ENG is the favourite. Recent form (last 5): MEX 4 wins, 1 draw; ENG 3 wins, 1 draw, 1 loss. Past 3 meetings: ENG won 3. Model gives MEX 2%, draw 8%, ENG 90%.


### POR vs ESP - Mon 06 Jul 19:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 1-2 (EV ~ 2.42 pts)
- **W / D / L:** 22% / 26% / 52%
- **lambda_home / lambda_away:** 1.10 / 1.78
- **Top scorelines:**
  - 1:1 (12%)
  - 1:2 (10%)
  - 0:2 (9%)
  - 0:1 (9%)

- **Why:** slight edge to ESP. Recent form (last 5): POR 3 wins, 1 draw, 1 loss; ESP 2 wins, 3 draws. Past 3 meetings: drew 2, ESP won 1. Model gives POR 22%, draw 26%, ESP 52%.


### USA vs BEL - Tue 07 Jul 00:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 1-2 (EV ~ 2.28 pts)
- **W / D / L:** 26% / 26% / 48%
- **lambda_home / lambda_away:** 1.17 / 1.67
- **Top scorelines:**
  - 1:1 (13%)
  - 1:2 (10%)
  - 0:1 (9%)
  - 0:2 (8%)

- **Why:** slight edge to BEL. Recent form (last 5): USA 2 wins, 3 losses; BEL 4 wins, 1 draw. Past 3 meetings: BEL won 3. Model gives USA 26%, draw 26%, BEL 48%. USA plays at home.


### ARG vs EGY - Tue 07 Jul 16:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 4.93 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 16.40 / 0.12
- **Top scorelines:**
  - 8:0 (49%)
  - 7:0 (24%)
  - 6:0 (10%)
  - 8:1 (6%)

- **Why:** ARG is the heavy favourite. Recent form (last 5): ARG 4 wins, 1 loss; EGY 2 wins, 2 draws, 1 loss. Past 2 meetings: ARG won 2. Model gives ARG 100%, draw 0%, EGY 0%.


### SUI vs COL - Tue 07 Jul 20:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 1-2 (EV ~ 2.32 pts)
- **W / D / L:** 25% / 26% / 49%
- **lambda_home / lambda_away:** 1.15 / 1.70
- **Top scorelines:**
  - 1:1 (12%)
  - 1:2 (10%)
  - 0:1 (9%)
  - 0:2 (8%)

- **Why:** slight edge to COL. Recent form (last 5): SUI 2 wins, 2 draws, 1 loss; COL 3 wins, 2 losses. Past 3 meetings: SUI won 1, COL won 2. Model gives SUI 25%, draw 26%, COL 49%.


### FRA vs MAR - Thu 09 Jul 20:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 5-0 (EV ~ 4.02 pts)
- **W / D / L:** 98% / 2% / 0%
- **lambda_home / lambda_away:** 5.43 / 0.36
- **Top scorelines:**
  - 5:0 (13%)
  - 4:0 (12%)
  - 6:0 (12%)
  - 7:0 (9%)

- **Why:** FRA is the clear favourite. Recent form (last 5): FRA 3 wins, 1 draw, 1 loss; MAR 2 wins, 3 draws. Past 3 meetings: FRA won 2, drew 1. Model gives FRA 98%, draw 2%, MAR 0%.


### None vs None - Fri 10 Jul 19:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 1.87 pts)
- **W / D / L:** 36% / 28% / 36%
- **lambda_home / lambda_away:** 1.40 / 1.40
- **Top scorelines:**
  - 1:1 (13%)
  - 2:1 (8%)
  - 1:2 (8%)
  - 1:0 (7%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 36%, draw 28%, None 36%.


### None vs None - Sat 11 Jul 21:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 1.87 pts)
- **W / D / L:** 36% / 28% / 36%
- **lambda_home / lambda_away:** 1.40 / 1.40
- **Top scorelines:**
  - 1:1 (13%)
  - 2:1 (8%)
  - 1:2 (8%)
  - 1:0 (7%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 36%, draw 28%, None 36%.


### None vs None - Sun 12 Jul 01:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 1.87 pts)
- **W / D / L:** 36% / 28% / 36%
- **lambda_home / lambda_away:** 1.40 / 1.40
- **Top scorelines:**
  - 1:1 (13%)
  - 2:1 (8%)
  - 1:2 (8%)
  - 1:0 (7%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 36%, draw 28%, None 36%.


### None vs None - Tue 14 Jul 19:00 UTC

- **Stage:** SF
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 1.87 pts)
- **W / D / L:** 36% / 28% / 36%
- **lambda_home / lambda_away:** 1.40 / 1.40
- **Top scorelines:**
  - 1:1 (13%)
  - 2:1 (8%)
  - 1:2 (8%)
  - 1:0 (7%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 36%, draw 28%, None 36%.


### None vs None - Wed 15 Jul 19:00 UTC

- **Stage:** SF
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 1.87 pts)
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
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 1.87 pts)
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
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 1.87 pts)
- **W / D / L:** 36% / 28% / 36%
- **lambda_home / lambda_away:** 1.40 / 1.40
- **Top scorelines:**
  - 1:1 (13%)
  - 2:1 (8%)
  - 1:2 (8%)
  - 1:0 (7%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 36%, draw 28%, None 36%.

