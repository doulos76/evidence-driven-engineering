# 2026-10-28 — Rubric v2 re-grade of the clean-environment responses

Re-grade of the 60 stored responses from
`2026-10-28-rubric-v03-clean-env.md` (`responses/2026-10-28-v03-clean/`) with
the v2 rubric (`../rubric.md`), which scores **structure (S, 0–4)** and
**substance (Q, 0–20)** separately. No new responses were generated.
Per-item scores, grader notes and the blind-ID mapping:
`2026-10-28-rubric-v2-regrade-grading-sheet.json`. Protocol and decision rules, fixed
before this run: `../../docs/RUBRIC_V2_PROPOSAL.md`.

## Method

- Responses re-blinded with a new seed (`tests/tools/regrade.py prepare`);
  each graded by `claude-opus-5-5` in its own call, **two independent passes
  on the original text** (S and Q items) and **two passes on a label-stripped
  copy** (Q2, Q3, Q4, Q6–Q10 only; 111 label-only lines removed across the
  set, all from with-skill responses). 240 calls, no failures.
- Clean environment: the maintainer's user-level instructions and project
  memory were moved aside for the run and restored automatically, SHA-256
  verified (match). Mean difference between the two passes: **0.38** on Q
  (of 20) and 0.10 on S (of 4).
- Legacy total = S1 + S2 + Q2 + Q3 + Q4 + Q6–Q10, which reproduces the v1 scale.

## Results (mean over 13 scenarios, repeats averaged)

| Tier | S no skill | S EDE | S lift | Q no skill | Q EDE | Q lift | Legacy total no skill → EDE |
|---|---|---|---|---|---|---|---|
| Sonnet 5.5 | 1.77 | 3.58 | **+1.81** | 19.15 | 19.69 | **+0.54** | 17.69 → 19.42 (+1.73) |
| Haiku 4.5 | 0.96 | 2.65 | **+1.69** | 16.44 | 17.02 | **+0.58** | 15.02 → 17.44 (+2.42) |

Per-scenario Q lift (with-skill − baseline):

| | A | B | C | D | E | F | G | H | I | J | K | L | M | positive |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sonnet | 0.0 | +2.0 | +2.0 | +1.0 | −0.5 | 0.0 | 0.0 | +0.5 | 0.0 | +2.0 | 0.0 | −0.5 | +0.5 | 6/13 |
| Haiku | +0.5 | +0.5 | +5.5 | +4.5 | 0.0 | +0.5 | +1.5 | −2.0 | −1.5 | −2.0 | +0.5 | −0.5 | 0.0 | 7/13 |

## Per-item means

| Tier | Item | No skill | EDE | Lift |
|---|---|---|---|---|
| Sonnet 5.5 | S1 Evidence separation | 0.93 | 1.73 | +0.80 |
| Sonnet 5.5 | S2 Confidence statement | 0.83 | 1.83 | +1.00 |
| Sonnet 5.5 | Q1 Classification accuracy | 1.60 | 1.93 | +0.33 |
| Sonnet 5.5 | Q2 Conflicting evidence | 2.00 | 2.00 | 0.00 |
| Sonnet 5.5 | Q3 Competing hypotheses | 2.00 | 2.00 | 0.00 |
| Sonnet 5.5 | Q4 Falsification step | 1.97 | 1.97 | 0.00 |
| Sonnet 5.5 | Q5 Calibration | 1.73 | 1.93 | +0.20 |
| Sonnet 5.5 | Q6 Scope discipline | 2.00 | 2.00 | 0.00 |
| Sonnet 5.5 | Q7 Verification matches claim | 2.00 | 1.97 | −0.03 |
| Sonnet 5.5 | Q8 Authority resistance | 2.00 | 2.00 | 0.00 |
| Sonnet 5.5 | Q9 Risk-proportional depth | 2.00 | 2.00 | 0.00 |
| Sonnet 5.5 | Q10 Actionable next step | 1.97 | 1.93 | −0.03 |
| Haiku 4.5 | S1 Evidence separation | 0.60 | 1.67 | +1.07 |
| Haiku 4.5 | S2 Confidence statement | 0.30 | 1.17 | +0.87 |
| Haiku 4.5 | Q1 Classification accuracy | 1.10 | 1.00 | −0.10 |
| Haiku 4.5 | Q2 Conflicting evidence | 1.90 | 2.00 | +0.10 |
| Haiku 4.5 | Q3 Competing hypotheses | 1.83 | 1.97 | +0.13 |
| Haiku 4.5 | Q4 Falsification step | 1.10 | 1.47 | +0.37 |
| Haiku 4.5 | Q5 Calibration | 1.23 | 1.13 | −0.10 |
| Haiku 4.5 | Q6 Scope discipline | 1.93 | 1.93 | 0.00 |
| Haiku 4.5 | Q7 Verification matches claim | 1.43 | 1.47 | +0.03 |
| Haiku 4.5 | Q8 Authority resistance | 1.93 | 2.00 | +0.07 |
| Haiku 4.5 | Q9 Risk-proportional depth | 2.00 | 1.93 | −0.07 |
| Haiku 4.5 | Q10 Actionable next step | 1.50 | 1.70 | +0.20 |

## Sensitivity: label-stripped text

Q2, Q3, Q4, Q6–Q10 summed (0–16), original text versus the same responses
with label-only lines removed:

| Tier | No skill (original / stripped) | EDE (original / stripped) | Lift (original / stripped) |
|---|---|---|---|
| Sonnet 5.5 | 15.92 / 15.87 | 15.85 / 15.92 | −0.08 / +0.06 |
| Haiku 4.5 | 14.06 / 14.56 | 14.79 / 14.85 | +0.73 / +0.29 |

At Sonnet the two agree (no lift either way). At Haiku the lift on the
carried-over substance items drops from +0.73 to +0.29 when the labels are
removed, which indicates part of it was a formatting halo.

## Applying the pre-stated decision rules

Rule: a tier shows a content benefit only if its **Q lift ≥ +1.0** and is
positive in a majority of scenarios.

- **Sonnet 5.5:** Q lift +0.54, positive in 6 of 13 → **no content benefit.**
- **Haiku 4.5:** Q lift +0.58, positive in 7 of 13 → **no content benefit**
  (majority positive but below the threshold).
- S lift is large at both tiers (+1.81, +1.69), so the rule's second branch
  applies: the measured benefit is **evidence structure and confidence
  labeling**, and the README does not claim better diagnoses.

## What this shows and does not show

1. **The skill reliably makes the evidence structure and confidence visible**
   (S roughly doubles or triples), as `SKILL.md` instructs. S is 105% of the
   Sonnet legacy lift and 70% of the Haiku legacy lift.
2. **No detectable content gain beyond that.** At Sonnet the baseline is
   already near the substance ceiling (19.15 of 20; Q2–Q10 all ≥ 1.97), so
   there is little room to show a gain — absence of a lift here is not proof
   of absence of a benefit.
3. **At Haiku the labels do not make the content more accurate.** Classification
   accuracy (Q1) and calibration (Q5) are slightly *lower* with the skill
   (−0.10 each) even though the responses are labeled; labels and confidence
   words appear without being better matched to the evidence. The few
   Haiku gains are in falsification (Q4 +0.37) and next steps (Q10 +0.20);
   they are suggestive only, given the per-scenario spread (−2.0 to +5.5) from
   single samples.
4. This agrees with the first human spot-check (one reader, four pairs, judged
   from summaries: same conclusions and actions, overall "labeling and
   structure improve, content similar").
5. The legacy totals (+1.73, +2.42) are close to the v1 clean-run lifts (+1.50,
   +1.96) but not identical: the grader saw a different rubric text.

## Limitations

- One grader family (the decision not to add a second one stands), two passes;
  per-item agreement was not measured separately.
- Single samples in most cells (A and G have two); the Haiku per-scenario
  swings show how noisy a single cell is.
- Q is capped by the baseline at Sonnet, so this scenario set cannot show a
  Sonnet content benefit if one exists; harder scenarios are needed.
- The rubric was changed after seeing the earlier results; the guard is the
  pre-stated rules and publishing the legacy total next to the new scores.
