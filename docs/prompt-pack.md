# Football Forecaster - Prompt Pack

Generated 2026-06-12 09:33 UTC. Paste this whole document into Claude Chat, then ask any question about the upcoming fixtures.

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


### CAN vs BIH - Fri 12 Jun 15:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 2-0 (EV ~ 4.09 pts)
- **W / D / L:** 91% / 8% / 1%
- **lambda_home / lambda_away:** 2.74 / 0.13
- **Top scorelines:**
  - 2:0 (21%)
  - 3:0 (20%)
  - 1:0 (15%)
  - 4:0 (13%)

- **Why:** CAN edge: +281 Elo over BIH. Form (last 5): CAN DWDDW, BIH DDDDD. Model: CAN 91% / draw 8% / BIH 1%. CAN at home.


### USA vs PAR - Fri 12 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 3.80 pts)
- **W / D / L:** 81% / 17% / 2%
- **lambda_home / lambda_away:** 1.97 / 0.18
- **Top scorelines:**
  - 2:0 (23%)
  - 1:0 (22%)
  - 3:0 (15%)
  - 0:0 (12%)

- **Why:** USA edge: +224 Elo over PAR. Form (last 5): USA LWLLW, PAR LWWLL. H2H last 3: USA 3W-0D-0L. Model: USA 81% / draw 17% / PAR 2%. USA at home.


### QAT vs SUI - Sat 13 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-2 (EV ~ 3.87 pts)
- **W / D / L:** 2% / 15% / 83%
- **lambda_home / lambda_away:** 0.17 / 2.12
- **Top scorelines:**
  - 0:2 (23%)
  - 0:1 (21%)
  - 0:3 (16%)
  - 0:0 (11%)

- **Why:** SUI edge: +221 Elo over QAT. Form (last 5): QAT LLLLW, SUI DWDLW. H2H last 1: QAT 1W-0D-0L. Model: QAT 2% / draw 15% / SUI 83%.


### BRA vs MAR - Sat 13 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 2-0 (EV ~ 4.11 pts)
- **W / D / L:** 92% / 7% / 1%
- **lambda_home / lambda_away:** 2.88 / 0.12
- **Top scorelines:**
  - 2:0 (21%)
  - 3:0 (20%)
  - 4:0 (14%)
  - 1:0 (14%)

- **Why:** BRA edge: +274 Elo over MAR. Form (last 5): BRA WWWLD, MAR DWDWD. H2H last 3: BRA 2W-0D-1L. Model: BRA 92% / draw 7% / MAR 1%.


### HAI vs SCO - Sat 13 Jun 21:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-2 (EV ~ 3.98 pts)
- **W / D / L:** 1% / 12% / 87%
- **lambda_home / lambda_away:** 0.15 / 2.34
- **Top scorelines:**
  - 0:2 (23%)
  - 0:1 (19%)
  - 0:3 (18%)
  - 0:4 (10%)

- **Why:** SCO edge: +238 Elo over HAI. Form (last 5): HAI LWDLW, SCO WLLWL. Model: HAI 1% / draw 12% / SCO 87%.


### AUS vs TUR - Sat 13 Jun 21:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 2-0 (EV ~ 3.91 pts)
- **W / D / L:** 85% / 14% / 2%
- **lambda_home / lambda_away:** 2.19 / 0.16
- **Top scorelines:**
  - 2:0 (23%)
  - 1:0 (20%)
  - 3:0 (17%)
  - 0:0 (10%)

- **Why:** AUS edge: +227 Elo over TUR. Form (last 5): AUS DLWWL, TUR WWWDL. H2H last 2: AUS 0W-0D-2L. Model: AUS 85% / draw 14% / TUR 2%.


### GER vs CUW - Sun 14 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 4.52 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 8.89 / 0.04
- **Top scorelines:**
  - 8:0 (27%)
  - 7:0 (25%)
  - 6:0 (19%)
  - 5:0 (13%)

- **Why:** GER edge: +470 Elo over CUW. Form (last 5): GER WWWWL, CUW LLLDW. Model: GER 100% / draw 0% / CUW 0%.


### NED vs JPN - Sun 14 Jun 15:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 3.62 pts)
- **W / D / L:** 73% / 23% / 4%
- **lambda_home / lambda_away:** 1.64 / 0.22
- **Top scorelines:**
  - 1:0 (25%)
  - 2:0 (21%)
  - 0:0 (16%)
  - 3:0 (11%)

- **Why:** NED edge: +176 Elo over JPN. Form (last 5): NED WLDWD, JPN WWWWW. H2H last 3: NED 2W-1D-0L. Model: NED 73% / draw 23% / JPN 4%.


### CIV vs ECU - Sun 14 Jun 19:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 2.94 pts)
- **W / D / L:** 11% / 37% / 52%
- **lambda_home / lambda_away:** 0.34 / 1.04
- **Top scorelines:**
  - 0:0 (26%)
  - 0:1 (25%)
  - 0:2 (14%)
  - 1:1 (10%)

- **Why:** ECU edge: +97 Elo over CIV. Form (last 5): CIV WWWLD, ECU WDDWD. Model: CIV 11% / draw 37% / ECU 52%.


### SWE vs TUN - Sun 14 Jun 20:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.76 pts)
- **W / D / L:** 3% / 19% / 79%
- **lambda_home / lambda_away:** 0.19 / 1.88
- **Top scorelines:**
  - 0:1 (23%)
  - 0:2 (22%)
  - 0:3 (14%)
  - 0:0 (13%)

- **Why:** TUN edge: +200 Elo over SWE. Form (last 5): SWE DLWWL, TUN LLDWL. H2H last 3: SWE 2W-0D-1L. Model: SWE 3% / draw 19% / TUN 79%.


### BEL vs EGY - Mon 15 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 2-0 (EV ~ 3.90 pts)
- **W / D / L:** 84% / 14% / 2%
- **lambda_home / lambda_away:** 2.17 / 0.16
- **Top scorelines:**
  - 2:0 (23%)
  - 1:0 (21%)
  - 3:0 (17%)
  - 0:0 (10%)

- **Why:** BEL edge: +225 Elo over EGY. Form (last 5): BEL WWDWW, EGY LWDWD. H2H last 3: BEL 1W-0D-2L. Model: BEL 84% / draw 14% / EGY 2%.


### ESP vs CPV - Mon 15 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 4.78 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 11.65 / 0.03
- **Top scorelines:**
  - 8:0 (40%)
  - 7:0 (27%)
  - 6:0 (16%)
  - 5:0 (8%)

- **Why:** ESP edge: +517 Elo over CPV. Form (last 5): ESP WDDWD, CPV WLDDW. Model: ESP 100% / draw 0% / CPV 0%.


### IRN vs NZL - Mon 15 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 3.70 pts)
- **W / D / L:** 77% / 20% / 3%
- **lambda_home / lambda_away:** 1.77 / 0.20
- **Top scorelines:**
  - 1:0 (24%)
  - 2:0 (22%)
  - 0:0 (14%)
  - 3:0 (13%)

- **Why:** IRN edge: +190 Elo over NZL. Form (last 5): IRN WLDDL, NZL LLWLL. H2H last 2: IRN 1W-1D-0L. Model: IRN 77% / draw 20% / NZL 3%.


### KSA vs URU - Mon 15 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-2 (EV ~ 4.02 pts)
- **W / D / L:** 1% / 11% / 88%
- **lambda_home / lambda_away:** 0.14 / 2.45
- **Top scorelines:**
  - 0:2 (22%)
  - 0:3 (18%)
  - 0:1 (18%)
  - 0:4 (11%)

- **Why:** URU edge: +246 Elo over KSA. Form (last 5): KSA DLLLL, URU DDLDW. H2H last 3: KSA 1W-1D-1L. Model: KSA 1% / draw 11% / URU 88%.


### FRA vs SEN - Tue 16 Jun 15:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 2-0 (EV ~ 4.12 pts)
- **W / D / L:** 93% / 7% / 1%
- **lambda_home / lambda_away:** 2.96 / 0.12
- **Top scorelines:**
  - 2:0 (20%)
  - 3:0 (20%)
  - 4:0 (15%)
  - 1:0 (13%)

- **Why:** FRA edge: +279 Elo over SEN. Form (last 5): FRA LWWWD, SEN DLWLW. H2H last 2: FRA 0W-0D-2L. Model: FRA 93% / draw 7% / SEN 1%.


### IRQ vs NOR - Tue 16 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.79 pts)
- **W / D / L:** 18% / 43% / 40%
- **lambda_home / lambda_away:** 0.45 / 0.79
- **Top scorelines:**
  - 0:0 (30%)
  - 0:1 (22%)
  - 1:0 (12%)
  - 1:1 (11%)

- **Why:** NOR edge: +50 Elo over IRQ. Form (last 5): IRQ LDLLD, NOR DWDLW. Model: IRQ 18% / draw 43% / NOR 40%.


### ARG vs ALG - Tue 16 Jun 20:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 5.35 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 24.06 / 0.01
- **Top scorelines:**
  - 8:0 (68%)
  - 7:0 (22%)
  - 6:0 (7%)
  - 5:0 (2%)

- **Why:** ARG edge: +643 Elo over ALG. Form (last 5): ARG WWWLW, ALG WDLWW. H2H last 1: ARG 1W-0D-0L. Model: ARG 100% / draw 0% / ALG 0%.


### AUT vs JOR - Tue 16 Jun 21:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.89 pts)
- **W / D / L:** 28% / 45% / 28%
- **lambda_home / lambda_away:** 0.59 / 0.59
- **Top scorelines:**
  - 0:0 (32%)
  - 0:1 (17%)
  - 1:0 (17%)
  - 1:1 (12%)

- **Why:** rated near-evenly. Form (last 5): AUT WWWDL, JOR LLDDL. Model: AUT 28% / draw 45% / JOR 28%.


### POR vs COD - Wed 17 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 4.55 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 9.20 / 0.04
- **Top scorelines:**
  - 8:0 (29%)
  - 7:0 (25%)
  - 6:0 (19%)
  - 5:0 (12%)

- **Why:** POR edge: +476 Elo over COD. Form (last 5): POR WWWDL, COD LDLDD. Model: POR 100% / draw 0% / COD 0%.


### ENG vs CRO - Wed 17 Jun 15:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 2.90 pts)
- **W / D / L:** 51% / 38% / 11%
- **lambda_home / lambda_away:** 1.01 / 0.35
- **Top scorelines:**
  - 0:0 (27%)
  - 1:0 (25%)
  - 2:0 (13%)
  - 1:1 (10%)

- **Why:** ENG edge: +93 Elo over CRO. Form (last 5): ENG WWLDW, CRO LLWDW. H2H last 3: ENG 2W-1D-0L. Model: ENG 51% / draw 38% / CRO 11%.


### GHA vs PAN - Wed 17 Jun 19:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.78 pts)
- **W / D / L:** 41% / 42% / 17%
- **lambda_home / lambda_away:** 0.81 / 0.44
- **Top scorelines:**
  - 0:0 (30%)
  - 1:0 (22%)
  - 0:1 (11%)
  - 1:1 (11%)

- **Why:** GHA edge: +54 Elo over PAN. Form (last 5): GHA DLLLL, PAN DLWDL. Model: GHA 41% / draw 42% / PAN 17%.


### UZB vs COL - Wed 17 Jun 20:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-5 (EV ~ 4.31 pts)
- **W / D / L:** 0% / 0% / 100%
- **lambda_home / lambda_away:** 0.06 / 5.87
- **Top scorelines:**
  - 0:5 (18%)
  - 0:6 (18%)
  - 0:4 (15%)
  - 0:7 (15%)

- **Why:** COL edge: +398 Elo over UZB. Form (last 5): UZB LLDDW, COL WWLLW. Model: UZB 0% / draw 0% / COL 100%.


### CZE vs RSA - Thu 18 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.17 pts)
- **W / D / L:** 8% / 33% / 58%
- **lambda_home / lambda_away:** 0.30 / 1.19
- **Top scorelines:**
  - 0:1 (26%)
  - 0:0 (24%)
  - 0:2 (16%)
  - 1:1 (9%)

- **Why:** RSA edge: +120 Elo over CZE. Form (last 5): CZE LDDDD, RSA LLDLL. H2H last 1: CZE 0W-1D-0L. Model: CZE 8% / draw 33% / RSA 58%.


### SUI vs BIH - Thu 18 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 4-0 (EV ~ 4.28 pts)
- **W / D / L:** 99% / 1% / 0%
- **lambda_home / lambda_away:** 4.97 / 0.07
- **Top scorelines:**
  - 4:0 (18%)
  - 5:0 (17%)
  - 6:0 (14%)
  - 3:0 (14%)

- **Why:** SUI edge: +369 Elo over BIH. Form (last 5): SUI DWDLW, BIH DDDDD. H2H last 1: SUI 0W-0D-1L. Model: SUI 99% / draw 1% / BIH 0%.


### CAN vs QAT - Thu 18 Jun 15:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 3.14 pts)
- **W / D / L:** 58% / 34% / 9%
- **lambda_home / lambda_away:** 1.17 / 0.30
- **Top scorelines:**
  - 1:0 (26%)
  - 0:0 (24%)
  - 2:0 (16%)
  - 1:1 (9%)

- **Why:** CAN edge: +133 Elo over QAT. Form (last 5): CAN DWDDW, QAT LLLLW. H2H last 1: CAN 1W-0D-0L. Model: CAN 58% / draw 34% / QAT 9%. CAN at home.


### MEX vs KOR - Thu 18 Jun 19:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.87 pts)
- **W / D / L:** 33% / 44% / 23%
- **lambda_home / lambda_away:** 0.68 / 0.52
- **Top scorelines:**
  - 0:0 (31%)
  - 1:0 (19%)
  - 0:1 (14%)
  - 1:1 (12%)

- **Why:** rated near-evenly. Form (last 5): MEX WWWWD, KOR WLLWW. H2H last 3: MEX 2W-1D-0L. Model: MEX 33% / draw 44% / KOR 23%.


### USA vs AUS - Fri 19 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.79 pts)
- **W / D / L:** 40% / 42% / 18%
- **lambda_home / lambda_away:** 0.80 / 0.44
- **Top scorelines:**
  - 0:0 (30%)
  - 1:0 (22%)
  - 0:1 (12%)
  - 1:1 (11%)

- **Why:** USA edge: +66 Elo over AUS. Form (last 5): USA LWLLW, AUS DLWWL. H2H last 3: USA 2W-1D-0L. Model: USA 40% / draw 42% / AUS 18%. USA at home.


### SCO vs MAR - Fri 19 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.78 pts)
- **W / D / L:** 17% / 42% / 40%
- **lambda_home / lambda_away:** 0.44 / 0.81
- **Top scorelines:**
  - 0:0 (30%)
  - 0:1 (22%)
  - 1:0 (11%)
  - 1:1 (11%)

- **Why:** MAR edge: +53 Elo over SCO. Form (last 5): SCO WLLWL, MAR DWDWD. H2H last 1: SCO 0W-0D-1L. Model: SCO 17% / draw 42% / MAR 40%.


### TUR vs PAR - Fri 19 Jun 20:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.71 pts)
- **W / D / L:** 15% / 41% / 45%
- **lambda_home / lambda_away:** 0.40 / 0.88
- **Top scorelines:**
  - 0:0 (29%)
  - 0:1 (23%)
  - 1:1 (11%)
  - 0:2 (11%)

- **Why:** PAR edge: +69 Elo over TUR. Form (last 5): TUR WWWDL, PAR LWWLL. Model: TUR 15% / draw 41% / PAR 45%.


### BRA vs HAI - Fri 19 Jun 20:30 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 5.02 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 15.35 / 0.02
- **Top scorelines:**
  - 8:0 (52%)
  - 7:0 (27%)
  - 6:0 (12%)
  - 5:0 (5%)

- **Why:** BRA edge: +565 Elo over HAI. Form (last 5): BRA WWWLD, HAI LWDLW. H2H last 3: BRA 3W-0D-0L. Model: BRA 100% / draw 0% / HAI 0%.


### NED vs SWE - Sat 20 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 4.62 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 9.91 / 0.04
- **Top scorelines:**
  - 8:0 (32%)
  - 7:0 (26%)
  - 6:0 (18%)
  - 5:0 (11%)

- **Why:** NED edge: +489 Elo over SWE. Form (last 5): NED WLDWD, SWE DLWWL. H2H last 3: NED 1W-1D-1L. Model: NED 100% / draw 0% / SWE 0%.


### GER vs CIV - Sat 20 Jun 16:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 3-0 (EV ~ 4.18 pts)
- **W / D / L:** 95% / 5% / 0%
- **lambda_home / lambda_away:** 3.30 / 0.11
- **Top scorelines:**
  - 3:0 (20%)
  - 2:0 (18%)
  - 4:0 (16%)
  - 5:0 (11%)

- **Why:** GER edge: +298 Elo over CIV. Form (last 5): GER WWWWL, CIV WWWLD. H2H last 1: GER 0W-1D-0L. Model: GER 95% / draw 5% / CIV 0%.


### ECU vs CUW - Sat 20 Jun 19:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 2-0 (EV ~ 4.10 pts)
- **W / D / L:** 91% / 8% / 1%
- **lambda_home / lambda_away:** 2.79 / 0.13
- **Top scorelines:**
  - 2:0 (21%)
  - 3:0 (20%)
  - 1:0 (15%)
  - 4:0 (14%)

- **Why:** ECU edge: +269 Elo over CUW. Form (last 5): ECU WDDWD, CUW LLLDW. Model: ECU 91% / draw 8% / CUW 1%.


### TUN vs JPN - Sat 20 Jun 22:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.10 pts)
- **W / D / L:** 9% / 34% / 56%
- **lambda_home / lambda_away:** 0.31 / 1.14
- **Top scorelines:**
  - 0:1 (26%)
  - 0:0 (24%)
  - 0:2 (15%)
  - 1:1 (9%)

- **Why:** JPN edge: +113 Elo over TUN. Form (last 5): TUN LLDWL, JPN WWWWW. H2H last 3: TUN 1W-0D-2L. Model: TUN 9% / draw 34% / JPN 56%.


### BEL vs IRN - Sun 21 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 2-0 (EV ~ 3.87 pts)
- **W / D / L:** 83% / 15% / 2%
- **lambda_home / lambda_away:** 2.11 / 0.17
- **Top scorelines:**
  - 2:0 (23%)
  - 1:0 (21%)
  - 3:0 (16%)
  - 0:0 (11%)

- **Why:** BEL edge: +220 Elo over IRN. Form (last 5): BEL WWDWW, IRN WLDDL. Model: BEL 83% / draw 15% / IRN 2%.


### ESP vs KSA - Sun 21 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 5-0 (EV ~ 4.30 pts)
- **W / D / L:** 99% / 1% / 0%
- **lambda_home / lambda_away:** 5.42 / 0.07
- **Top scorelines:**
  - 5:0 (18%)
  - 4:0 (17%)
  - 6:0 (16%)
  - 7:0 (13%)

- **Why:** ESP edge: +384 Elo over KSA. Form (last 5): ESP WDDWD, KSA DLLLL. H2H last 3: ESP 3W-0D-0L. Model: ESP 99% / draw 1% / KSA 0%.


### NZL vs EGY - Sun 21 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.67 pts)
- **W / D / L:** 3% / 21% / 75%
- **lambda_home / lambda_away:** 0.20 / 1.72
- **Top scorelines:**
  - 0:1 (24%)
  - 0:2 (22%)
  - 0:0 (15%)
  - 0:3 (12%)

- **Why:** EGY edge: +185 Elo over NZL. Form (last 5): NZL LLWLL, EGY LWDWD. H2H last 3: NZL 0W-1D-2L. Model: NZL 3% / draw 21% / EGY 75%.


### URU vs CPV - Sun 21 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 5-0 (EV ~ 4.29 pts)
- **W / D / L:** 99% / 1% / 0%
- **lambda_home / lambda_away:** 5.26 / 0.07
- **Top scorelines:**
  - 5:0 (18%)
  - 4:0 (17%)
  - 6:0 (16%)
  - 3:0 (13%)

- **Why:** URU edge: +379 Elo over CPV. Form (last 5): URU DDLDW, CPV WLDDW. Model: URU 99% / draw 1% / CPV 0%.


### ARG vs AUT - Mon 22 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 5.35 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 24.06 / 0.01
- **Top scorelines:**
  - 8:0 (68%)
  - 7:0 (22%)
  - 6:0 (7%)
  - 5:0 (2%)

- **Why:** ARG edge: +643 Elo over AUT. Form (last 5): ARG WWWLW, AUT WWWDL. H2H last 2: ARG 1W-1D-0L. Model: ARG 100% / draw 0% / AUT 0%.


### FRA vs IRQ - Mon 22 Jun 17:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 5.07 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 16.36 / 0.02
- **Top scorelines:**
  - 8:0 (54%)
  - 7:0 (27%)
  - 6:0 (11%)
  - 5:0 (4%)

- **Why:** FRA edge: +576 Elo over IRQ. Form (last 5): FRA LWWWD, IRQ LDLLD. Model: FRA 100% / draw 0% / IRQ 0%.


### NOR vs SEN - Mon 22 Jun 20:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-2 (EV ~ 4.02 pts)
- **W / D / L:** 1% / 11% / 88%
- **lambda_home / lambda_away:** 0.14 / 2.46
- **Top scorelines:**
  - 0:2 (22%)
  - 0:3 (18%)
  - 0:1 (18%)
  - 0:4 (11%)

- **Why:** SEN edge: +247 Elo over NOR. Form (last 5): NOR DWDLW, SEN DLWLW. H2H last 1: NOR 0W-0D-1L. Model: NOR 1% / draw 11% / SEN 88%.


### JOR vs ALG - Mon 22 Jun 20:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.89 pts)
- **W / D / L:** 28% / 45% / 28%
- **lambda_home / lambda_away:** 0.59 / 0.59
- **Top scorelines:**
  - 0:0 (32%)
  - 0:1 (17%)
  - 1:0 (17%)
  - 1:1 (12%)

- **Why:** rated near-evenly. Form (last 5): JOR LLDDL, ALG WDLWW. H2H last 2: JOR 0W-1D-1L. Model: JOR 28% / draw 45% / ALG 28%.


### POR vs UZB - Tue 23 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 8-0 (EV ~ 4.55 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 9.20 / 0.04
- **Top scorelines:**
  - 8:0 (29%)
  - 7:0 (25%)
  - 6:0 (19%)
  - 5:0 (12%)

- **Why:** POR edge: +476 Elo over UZB. Form (last 5): POR WWWDL, UZB LLDDW. Model: POR 100% / draw 0% / UZB 0%.


### ENG vs GHA - Tue 23 Jun 16:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 4-0 (EV ~ 4.28 pts)
- **W / D / L:** 99% / 1% / 0%
- **lambda_home / lambda_away:** 4.69 / 0.08
- **Top scorelines:**
  - 4:0 (18%)
  - 5:0 (17%)
  - 3:0 (15%)
  - 6:0 (13%)

- **Why:** ENG edge: +359 Elo over GHA. Form (last 5): ENG WWLDW, GHA DLLLL. H2H last 1: ENG 0W-1D-0L. Model: ENG 99% / draw 1% / GHA 0%.


### PAN vs CRO - Tue 23 Jun 19:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-3 (EV ~ 4.23 pts)
- **W / D / L:** 0% / 3% / 97%
- **lambda_home / lambda_away:** 0.09 / 3.75
- **Top scorelines:**
  - 0:3 (19%)
  - 0:4 (18%)
  - 0:2 (15%)
  - 0:5 (13%)

- **Why:** CRO edge: +320 Elo over PAN. Form (last 5): PAN DLWDL, CRO LLWDW. Model: PAN 0% / draw 3% / CRO 97%.


### COL vs COD - Tue 23 Jun 20:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 5-0 (EV ~ 4.31 pts)
- **W / D / L:** 100% / 0% / 0%
- **lambda_home / lambda_away:** 5.87 / 0.06
- **Top scorelines:**
  - 5:0 (18%)
  - 6:0 (18%)
  - 4:0 (15%)
  - 7:0 (15%)

- **Why:** COL edge: +398 Elo over COD. Form (last 5): COL WWLLW, COD LDLDD. Model: COL 100% / draw 0% / COD 0%.


### SUI vs CAN - Wed 24 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 1-0 (EV ~ 2.85 pts)
- **W / D / L:** 50% / 38% / 12%
- **lambda_home / lambda_away:** 0.99 / 0.36
- **Top scorelines:**
  - 0:0 (27%)
  - 1:0 (25%)
  - 2:0 (13%)
  - 1:1 (10%)

- **Why:** SUI edge: +88 Elo over CAN. Form (last 5): SUI DWDLW, CAN DWDDW. H2H last 1: SUI 0W-0D-1L. Model: SUI 50% / draw 38% / CAN 12%.


### BIH vs QAT - Wed 24 Jun 12:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.41 pts)
- **W / D / L:** 6% / 28% / 66%
- **lambda_home / lambda_away:** 0.25 / 1.39
- **Top scorelines:**
  - 0:1 (26%)
  - 0:0 (20%)
  - 0:2 (19%)
  - 0:3 (9%)

- **Why:** QAT edge: +148 Elo over BIH. Form (last 5): BIH DDDDD, QAT LLLLW. H2H last 2: BIH 0W-1D-1L. Model: BIH 6% / draw 28% / QAT 66%.


### SCO vs BRA - Wed 24 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-3 (EV ~ 4.23 pts)
- **W / D / L:** 0% / 3% / 97%
- **lambda_home / lambda_away:** 0.09 / 3.90
- **Top scorelines:**
  - 0:3 (19%)
  - 0:4 (18%)
  - 0:2 (14%)
  - 0:5 (14%)

- **Why:** BRA edge: +327 Elo over SCO. Form (last 5): SCO WLLWL, BRA WWWLD. H2H last 3: SCO 0W-0D-3L. Model: SCO 0% / draw 3% / BRA 97%.


### MAR vs HAI - Wed 24 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 3-0 (EV ~ 4.16 pts)
- **W / D / L:** 94% / 6% / 0%
- **lambda_home / lambda_away:** 3.17 / 0.11
- **Top scorelines:**
  - 3:0 (20%)
  - 2:0 (19%)
  - 4:0 (16%)
  - 1:0 (12%)

- **Why:** MAR edge: +291 Elo over HAI. Form (last 5): MAR DWDWD, HAI LWDLW. Model: MAR 94% / draw 6% / HAI 0%.


### CZE vs MEX - Wed 24 Jun 19:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-4 (EV ~ 4.24 pts)
- **W / D / L:** 0% / 2% / 98%
- **lambda_home / lambda_away:** 0.09 / 4.06
- **Top scorelines:**
  - 0:4 (18%)
  - 0:3 (18%)
  - 0:5 (15%)
  - 0:2 (13%)

- **Why:** MEX edge: +333 Elo over CZE. Form (last 5): CZE LDDDD, MEX WWWWD. H2H last 1: CZE 1W-0D-0L. Model: CZE 0% / draw 2% / MEX 98%.


### RSA vs KOR - Wed 24 Jun 19:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.70 pts)
- **W / D / L:** 3% / 20% / 77%
- **lambda_home / lambda_away:** 0.20 / 1.77
- **Top scorelines:**
  - 0:1 (24%)
  - 0:2 (22%)
  - 0:0 (14%)
  - 0:3 (13%)

- **Why:** KOR edge: +189 Elo over RSA. Form (last 5): RSA LLDLL, KOR WLLWW. Model: RSA 3% / draw 20% / KOR 77%.


### CUW vs CIV - Thu 25 Jun 16:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.59 pts)
- **W / D / L:** 4% / 24% / 72%
- **lambda_home / lambda_away:** 0.22 / 1.60
- **Top scorelines:**
  - 0:1 (25%)
  - 0:2 (21%)
  - 0:0 (17%)
  - 0:3 (11%)

- **Why:** CIV edge: +172 Elo over CUW. Form (last 5): CUW LLLDW, CIV WWWLD. Model: CUW 4% / draw 24% / CIV 72%.


### ECU vs GER - Thu 25 Jun 16:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.76 pts)
- **W / D / L:** 3% / 18% / 79%
- **lambda_home / lambda_away:** 0.19 / 1.89
- **Top scorelines:**
  - 0:1 (23%)
  - 0:2 (22%)
  - 0:3 (14%)
  - 0:0 (13%)

- **Why:** GER edge: +201 Elo over ECU. Form (last 5): ECU WDDWD, GER WWWWL. H2H last 2: ECU 0W-0D-2L. Model: ECU 3% / draw 18% / GER 79%.


### JPN vs SWE - Thu 25 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 3-0 (EV ~ 4.22 pts)
- **W / D / L:** 96% / 4% / 0%
- **lambda_home / lambda_away:** 3.60 / 0.10
- **Top scorelines:**
  - 3:0 (19%)
  - 4:0 (18%)
  - 2:0 (16%)
  - 5:0 (13%)

- **Why:** JPN edge: +313 Elo over SWE. Form (last 5): JPN WWWWW, SWE DLWWL. H2H last 3: JPN 0W-2D-1L. Model: JPN 96% / draw 4% / SWE 0%.


### TUN vs NED - Thu 25 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-3 (EV ~ 4.15 pts)
- **W / D / L:** 0% / 6% / 94%
- **lambda_home / lambda_away:** 0.11 / 3.13
- **Top scorelines:**
  - 0:3 (20%)
  - 0:2 (19%)
  - 0:4 (16%)
  - 0:1 (12%)

- **Why:** NED edge: +289 Elo over TUN. Form (last 5): TUN LLDWL, NED WLDWD. H2H last 3: TUN 0W-2D-1L. Model: TUN 0% / draw 6% / NED 94%.


### TUR vs USA - Thu 25 Jun 19:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-3 (EV ~ 4.17 pts)
- **W / D / L:** 0% / 5% / 94%
- **lambda_home / lambda_away:** 0.11 / 3.21
- **Top scorelines:**
  - 0:3 (20%)
  - 0:2 (19%)
  - 0:4 (16%)
  - 0:1 (12%)

- **Why:** USA edge: +293 Elo over TUR. Form (last 5): TUR WWWDL, USA LWLLW. H2H last 3: TUR 1W-0D-2L. Model: TUR 0% / draw 5% / USA 94%.


### PAR vs AUS - Thu 25 Jun 19:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.49 pts)
- **W / D / L:** 5% / 26% / 69%
- **lambda_home / lambda_away:** 0.24 / 1.47
- **Top scorelines:**
  - 0:1 (26%)
  - 0:2 (20%)
  - 0:0 (19%)
  - 0:3 (10%)

- **Why:** AUS edge: +158 Elo over PAR. Form (last 5): PAR LWWLL, AUS DLWWL. H2H last 3: PAR 0W-1D-2L. Model: PAR 5% / draw 26% / AUS 69%.


### NOR vs FRA - Fri 26 Jun 15:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-8 (EV ~ 4.82 pts)
- **W / D / L:** 0% / 0% / 100%
- **lambda_home / lambda_away:** 0.03 / 12.27
- **Top scorelines:**
  - 0:8 (42%)
  - 0:7 (27%)
  - 0:6 (16%)
  - 0:5 (8%)

- **Why:** FRA edge: +526 Elo over NOR. Form (last 5): NOR DWDLW, FRA LWWWD. H2H last 3: NOR 1W-1D-1L. Model: NOR 0% / draw 0% / FRA 100%.


### SEN vs IRQ - Fri 26 Jun 15:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 3-0 (EV ~ 4.18 pts)
- **W / D / L:** 95% / 5% / 0%
- **lambda_home / lambda_away:** 3.28 / 0.11
- **Top scorelines:**
  - 3:0 (20%)
  - 2:0 (18%)
  - 4:0 (16%)
  - 1:0 (11%)

- **Why:** SEN edge: +297 Elo over IRQ. Form (last 5): SEN DLWLW, IRQ LDLLD. Model: SEN 95% / draw 5% / IRQ 0%.


### URU vs ESP - Fri 26 Jun 18:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.33 pts)
- **W / D / L:** 7% / 30% / 63%
- **lambda_home / lambda_away:** 0.27 / 1.31
- **Top scorelines:**
  - 0:1 (26%)
  - 0:0 (21%)
  - 0:2 (18%)
  - 1:1 (8%)

- **Why:** ESP edge: +138 Elo over URU. Form (last 5): URU DDLDW, ESP WDDWD. H2H last 3: URU 0W-0D-3L. Model: URU 7% / draw 30% / ESP 63%.


### CPV vs KSA - Fri 26 Jun 19:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 3.28 pts)
- **W / D / L:** 7% / 31% / 62%
- **lambda_home / lambda_away:** 0.28 / 1.28
- **Top scorelines:**
  - 0:1 (26%)
  - 0:0 (22%)
  - 0:2 (17%)
  - 1:1 (8%)

- **Why:** KSA edge: +133 Elo over CPV. Form (last 5): CPV WLDDW, KSA DLLLL. Model: CPV 7% / draw 31% / KSA 62%.


### EGY vs IRN - Fri 26 Jun 20:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.89 pts)
- **W / D / L:** 27% / 45% / 29%
- **lambda_home / lambda_away:** 0.58 / 0.61
- **Top scorelines:**
  - 0:0 (32%)
  - 0:1 (17%)
  - 1:0 (16%)
  - 1:1 (12%)

- **Why:** rated near-evenly. Form (last 5): EGY LWDWD, IRN WLDDL. H2H last 1: EGY 0W-1D-0L. Model: EGY 27% / draw 45% / IRN 29%.


### NZL vs BEL - Fri 26 Jun 20:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-6 (EV ~ 4.33 pts)
- **W / D / L:** 0% / 0% / 100%
- **lambda_home / lambda_away:** 0.06 / 6.29
- **Top scorelines:**
  - 0:6 (18%)
  - 0:5 (18%)
  - 0:7 (17%)
  - 0:4 (14%)

- **Why:** BEL edge: +410 Elo over NZL. Form (last 5): NZL LLWLL, BEL WWDWW. Model: NZL 0% / draw 0% / BEL 100%.


### PAN vs ENG - Sat 27 Jun 17:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-6 (EV ~ 4.33 pts)
- **W / D / L:** 0% / 0% / 100%
- **lambda_home / lambda_away:** 0.06 / 6.40
- **Top scorelines:**
  - 0:6 (19%)
  - 0:5 (18%)
  - 0:7 (17%)
  - 0:4 (14%)

- **Why:** ENG edge: +413 Elo over PAN. Form (last 5): PAN DLWDL, ENG WWLDW. H2H last 1: PAN 0W-0D-1L. Model: PAN 0% / draw 0% / ENG 100%.


### CRO vs GHA - Sat 27 Jun 17:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 2-0 (EV ~ 4.09 pts)
- **W / D / L:** 91% / 8% / 1%
- **lambda_home / lambda_away:** 2.75 / 0.13
- **Top scorelines:**
  - 2:0 (21%)
  - 3:0 (20%)
  - 1:0 (15%)
  - 4:0 (13%)

- **Why:** CRO edge: +266 Elo over GHA. Form (last 5): CRO LLWDW, GHA DLLLL. Model: CRO 91% / draw 8% / GHA 1%.


### COL vs POR - Sat 27 Jun 19:30 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-1 (EV ~ 2.75 pts)
- **W / D / L:** 14% / 40% / 47%
- **lambda_home / lambda_away:** 0.38 / 0.93
- **Top scorelines:**
  - 0:0 (28%)
  - 0:1 (24%)
  - 0:2 (12%)
  - 1:1 (11%)

- **Why:** POR edge: +78 Elo over COL. Form (last 5): COL WWLLW, POR WWWDL. Model: COL 14% / draw 40% / POR 47%.


### COD vs UZB - Sat 27 Jun 19:30 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.89 pts)
- **W / D / L:** 28% / 45% / 28%
- **lambda_home / lambda_away:** 0.59 / 0.59
- **Top scorelines:**
  - 0:0 (32%)
  - 0:1 (17%)
  - 1:0 (17%)
  - 1:1 (12%)

- **Why:** rated near-evenly. Form (last 5): COD LDLDD, UZB LLDDW. Model: COD 28% / draw 45% / UZB 28%.


### ALG vs AUT - Sat 27 Jun 21:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-0 (EV ~ 2.89 pts)
- **W / D / L:** 28% / 45% / 28%
- **lambda_home / lambda_away:** 0.59 / 0.59
- **Top scorelines:**
  - 0:0 (32%)
  - 0:1 (17%)
  - 1:0 (17%)
  - 1:1 (12%)

- **Why:** rated near-evenly. Form (last 5): ALG WDLWW, AUT WWWDL. H2H last 1: ALG 0W-0D-1L. Model: ALG 28% / draw 45% / AUT 28%.


### JOR vs ARG - Sat 27 Jun 21:00 UTC

- **Stage:** GROUP
- **Recommended pick (EV-optimal):** 0-8 (EV ~ 5.35 pts)
- **W / D / L:** 0% / 0% / 100%
- **lambda_home / lambda_away:** 0.01 / 24.06
- **Top scorelines:**
  - 0:8 (68%)
  - 0:7 (22%)
  - 0:6 (7%)
  - 0:5 (2%)

- **Why:** ARG edge: +643 Elo over JOR. Form (last 5): JOR LLDDL, ARG WWWLW. Model: JOR 0% / draw 0% / ARG 100%.

