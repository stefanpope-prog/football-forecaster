# Football Forecaster - Prompt Pack

Generated 2026-07-01 23:02 UTC. Paste this whole document into Claude Chat, then ask any question about the upcoming fixtures.

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


### USA vs BIH - Thu 02 Jul 00:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 2-0 (EV ~ 4.11 pts)
- **W / D / L:** 90% / 9% / 1%
- **lambda_home / lambda_away:** 2.57 / 0.11
- **Top scorelines:**
  - 2:0 (23%)
  - 3:0 (20%)
  - 1:0 (18%)
  - 4:0 (13%)

- **Why:** USA is the clear favourite. Recent form (last 5): USA 2 wins, 3 losses; BIH drew all 5. Past 3 meetings: USA won 2, drew 1. Model gives USA 90%, draw 9%, BIH 1%. USA plays at home.


### ESP vs AUT - Thu 02 Jul 19:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 4.58 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 9.36 / 0.03
- **Top scorelines:**
  - 8:0 (30%)
  - 7:0 (26%)
  - 6:0 (19%)
  - 5:0 (12%)

- **Why:** ESP is the heavy favourite. Recent form (last 5): ESP 2 wins, 3 draws; AUT 3 wins, 1 draw, 1 loss. Past 3 meetings: ESP won 2, drew 1. Model gives ESP 100%, draw 0%, AUT 0%.


### POR vs CRO - Thu 02 Jul 23:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.94 pts)
- **W / D / L:** 36% / 44% / 20%
- **lambda_home / lambda_away:** 0.65 / 0.42
- **Top scorelines:**
  - 0:0 (34%)
  - 1:0 (22%)
  - 0:1 (15%)
  - 1:1 (9%)

- **Why:** slight edge to POR. Recent form (last 5): POR 3 wins, 1 draw, 1 loss; CRO 2 wins, 1 draw, 2 losses. Past 3 meetings: POR won 1, drew 1, CRO won 1. Model gives POR 36%, draw 44%, CRO 20%.


### SUI vs ALG - Fri 03 Jul 03:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 4-0 (EV ~ 4.28 pts)
- **W / D / L:** 98% / 2% / 0%
- **lambda_home / lambda_away:** 4.19 / 0.06
- **Top scorelines:**
  - 4:0 (19%)
  - 3:0 (18%)
  - 5:0 (16%)
  - 2:0 (13%)

- **Why:** SUI is the clear favourite. Recent form (last 5): SUI 2 wins, 2 draws, 1 loss; ALG 3 wins, 1 draw, 1 loss. Past 2 meetings: SUI won 2. Model gives SUI 98%, draw 2%, ALG 0%.


### AUS vs EGY - Fri 03 Jul 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.85 pts)
- **W / D / L:** 41% / 42% / 16%
- **lambda_home / lambda_away:** 0.75 / 0.36
- **Top scorelines:**
  - 0:0 (33%)
  - 1:0 (25%)
  - 0:1 (12%)
  - 2:0 (9%)

- **Why:** slight edge to AUS. Recent form (last 5): AUS 2 wins, 1 draw, 2 losses; EGY 2 wins, 2 draws, 1 loss. Past 2 meetings: drew 1, EGY won 1. Model gives AUS 41%, draw 42%, EGY 16%.


### ARG vs CPV - Fri 03 Jul 22:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 5.16 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 18.02 / 0.02
- **Top scorelines:**
  - 8:0 (58%)
  - 7:0 (26%)
  - 6:0 (10%)
  - 5:0 (3%)

- **Why:** ARG is the heavy favourite. Recent form (last 5): ARG 4 wins, 1 loss; CPV 2 wins, 2 draws, 1 loss. Model gives ARG 100%, draw 0%, CPV 0%.


### COL vs GHA - Sat 04 Jul 01:30 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 3.88 pts)
- **W / D / L:** 82% / 16% / 2%
- **lambda_home / lambda_away:** 1.95 / 0.14
- **Top scorelines:**
  - 1:0 (24%)
  - 2:0 (24%)
  - 3:0 (15%)
  - 0:0 (12%)

- **Why:** COL is the clear favourite. Recent form (last 5): COL 3 wins, 2 losses; GHA 1 draw, 4 losses. Model gives COL 82%, draw 16%, GHA 2%.


### CAN vs MAR - Sat 04 Jul 17:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.86 pts)
- **W / D / L:** 17% / 42% / 41%
- **lambda_home / lambda_away:** 0.37 / 0.74
- **Top scorelines:**
  - 0:0 (33%)
  - 0:1 (25%)
  - 1:0 (12%)
  - 0:2 (9%)

- **Why:** slight edge to MAR. Recent form (last 5): CAN 2 wins, 3 draws; MAR 2 wins, 3 draws. Past 3 meetings: drew 1, MAR won 2. Model gives CAN 17%, draw 42%, MAR 41%.


### PAR vs FRA - Sat 04 Jul 21:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 0-6 (EV ~ 4.34 pts)
- **W / D / L:** 0% / 0% / 100%
- **lambda_home / lambda_away:** 0.04 / 6.23
- **Top scorelines:**
  - 0:6 (19%)
  - 0:5 (18%)
  - 0:7 (17%)
  - 0:4 (14%)

- **Why:** FRA is the heavy favourite. Recent form (last 5): PAR 2 wins, 3 losses; FRA 3 wins, 1 draw, 1 loss. Past 3 meetings: drew 2, FRA won 1. Model gives PAR 0%, draw 0%, FRA 100%.


### BRA vs NOR - Sun 05 Jul 20:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 7-0 (EV ~ 4.40 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 7.45 / 0.04
- **Top scorelines:**
  - 7:0 (21%)
  - 6:0 (20%)
  - 8:0 (20%)
  - 5:0 (16%)

- **Why:** BRA is the heavy favourite. Recent form (last 5): BRA 3 wins, 1 draw, 1 loss; NOR 2 wins, 2 draws, 1 loss. Past 3 meetings: drew 1, NOR won 2. Model gives BRA 100%, draw 0%, NOR 0%.


### None vs None - Mon 06 Jul 00:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Mon 06 Jul 19:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Tue 07 Jul 00:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Tue 07 Jul 16:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Tue 07 Jul 20:00 UTC

- **Stage:** R16
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Thu 09 Jul 20:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Fri 10 Jul 19:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Sat 11 Jul 21:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Sun 12 Jul 01:00 UTC

- **Stage:** QF
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Tue 14 Jul 19:00 UTC

- **Stage:** SF
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Wed 15 Jul 19:00 UTC

- **Stage:** SF
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.


### None vs None - Sat 18 Jul 21:00 UTC

- **Stage:** F
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
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
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.99 pts)
- **W / D / L:** 27% / 45% / 27%
- **lambda_home / lambda_away:** 0.52 / 0.52
- **Top scorelines:**
  - 0:0 (35%)
  - 1:0 (19%)
  - 0:1 (19%)
  - 1:1 (9%)

- **Why:** None and None look evenly matched. Recent form (last 5): None no recent matches; None no recent matches. Model gives None 27%, draw 45%, None 27%.

