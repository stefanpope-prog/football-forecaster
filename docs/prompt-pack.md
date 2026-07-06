# Football Forecaster - Prompt Pack

Generated 2026-07-06 21:02 UTC. Paste this whole document into Claude Chat, then ask any question about the upcoming fixtures.

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


### POR vs ESP - Mon 06 Jul 19:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.92 pts)
- **W / D / L:** 20% / 44% / 37%
- **lambda_home / lambda_away:** 0.41 / 0.67
- **Top scorelines:**
  - 0:0 (34%)
  - 0:1 (23%)
  - 1:0 (14%)
  - 1:1 (9%)

- **Why:** slight edge to ESP. Recent form (last 5): POR 3 wins, 1 draw, 1 loss; ESP 2 wins, 3 draws. Past 3 meetings: drew 2, ESP won 1. Model gives POR 20%, draw 44%, ESP 37%.


### USA vs BEL - Tue 07 Jul 00:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 2.93 pts)
- **W / D / L:** 12% / 38% / 50%
- **lambda_home / lambda_away:** 0.30 / 0.92
- **Top scorelines:**
  - 0:0 (29%)
  - 0:1 (27%)
  - 0:2 (13%)
  - 1:0 (9%)

- **Why:** slight edge to BEL. Recent form (last 5): USA 2 wins, 3 losses; BEL 4 wins, 1 draw. Past 3 meetings: BEL won 3. Model gives USA 12%, draw 38%, BEL 50%. USA plays at home.


### ARG vs EGY - Tue 07 Jul 16:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 6-0 (EV ~ 4.33 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 6.14 / 0.04
- **Top scorelines:**
  - 6:0 (18%)
  - 5:0 (18%)
  - 7:0 (16%)
  - 4:0 (15%)

- **Why:** ARG is the heavy favourite. Recent form (last 5): ARG 4 wins, 1 loss; EGY 2 wins, 2 draws, 1 loss. Past 2 meetings: ARG won 2. Model gives ARG 100%, draw 0%, EGY 0%.


### SUI vs COL - Tue 07 Jul 20:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.94 pts)
- **W / D / L:** 21% / 44% / 35%
- **lambda_home / lambda_away:** 0.43 / 0.64
- **Top scorelines:**
  - 0:0 (34%)
  - 0:1 (22%)
  - 1:0 (15%)
  - 1:1 (9%)

- **Why:** slight edge to COL. Recent form (last 5): SUI 2 wins, 2 draws, 1 loss; COL 3 wins, 2 losses. Past 3 meetings: SUI won 1, COL won 2. Model gives SUI 21%, draw 44%, COL 35%.


### FRA vs MAR - Thu 09 Jul 20:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 3.91 pts)
- **W / D / L:** 83% / 15% / 2%
- **lambda_home / lambda_away:** 2.03 / 0.14
- **Top scorelines:**
  - 2:0 (24%)
  - 1:0 (23%)
  - 3:0 (16%)
  - 0:0 (11%)

- **Why:** FRA is the clear favourite. Recent form (last 5): FRA 3 wins, 1 draw, 1 loss; MAR 2 wins, 3 draws. Past 3 meetings: FRA won 2, drew 1. Model gives FRA 83%, draw 15%, MAR 2%.


### None vs None - Fri 10 Jul 19:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.98 pts)
- **W / D / L:** 28% / 45% / 28%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 28%, draw 45%, None 28%.


### NOR vs ENG - Sat 11 Jul 21:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 0-5 (EV ~ 4.30 pts)
- **W / D / L:** 0% / 1% / 99%
- **lambda_home / lambda_away:** 0.05 / 5.16
- **Top scorelines:**
  - 0:5 (18%)
  - 0:4 (17%)
  - 0:6 (16%)
  - 0:3 (14%)

- **Why:** ENG is the clear favourite. Recent form (last 5): NOR 2 wins, 2 draws, 1 loss; ENG 3 wins, 1 draw, 1 loss. Past 3 meetings: drew 1, ENG won 2. Model gives NOR 0%, draw 1%, ENG 99%.


### None vs None - Sun 12 Jul 01:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.98 pts)
- **W / D / L:** 28% / 45% / 28%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 28%, draw 45%, None 28%.


### None vs None - Tue 14 Jul 19:00 UTC

- **Stage:** SF
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.98 pts)
- **W / D / L:** 28% / 45% / 28%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 28%, draw 45%, None 28%.


### None vs None - Wed 15 Jul 19:00 UTC

- **Stage:** SF
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.98 pts)
- **W / D / L:** 28% / 45% / 28%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 28%, draw 45%, None 28%.


### None vs None - Sat 18 Jul 21:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.98 pts)
- **W / D / L:** 28% / 45% / 28%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 28%, draw 45%, None 28%.


### None vs None - Sun 19 Jul 19:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.98 pts)
- **W / D / L:** 28% / 45% / 28%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 28%, draw 45%, None 28%.

