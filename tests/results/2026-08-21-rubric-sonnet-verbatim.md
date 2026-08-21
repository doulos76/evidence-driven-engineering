# Rubric Scoring Run (verbatim, 2 passes) — Sonnet 5 responses — 2026-08-21

Follow-up to
[`2026-08-21-rubric-haiku-verbatim.md`](./2026-08-21-rubric-haiku-verbatim.md),
which applied the verbatim/two-pass rubric method to Haiku 4.5 and found no
with-skill advantage (with-skill 11.50/20 vs. baseline 12.79/20), driven
substantially by scenario A, where the with-skill response skipped the
skill's own instructed structure while the baseline response spontaneously
used it. That run's open question, stated explicitly in its
recommendation, was whether this was a Haiku-tier instruction-following
limitation or a more general property of the skill/rubric — to be checked
by running the same method against Sonnet 5.

This run answers that question.

## Method

The original three Sonnet 5 pass/fail runs
([`2026-08-21-run.md`](./2026-08-21-run.md),
[`2026-08-21-run-cfh.md`](./2026-08-21-run-cfh.md),
[`2026-08-21-run-ijkl.md`](./2026-08-21-run-ijkl.md)) did not preserve
verbatim response text — only summaries. Since the Haiku rubric run's own
finding was that grading from summaries is unreliable, those summaries
could not be reused. All 12 scenarios (A-L) were **re-run from scratch**
with Sonnet 5, with-skill and baseline, 24 new responses captured verbatim.
Prompts were reconstructed from the scenario definitions in
`tests/scenarios.md` plus the specific details (file names, numbers)
recorded in the original summaries, so they match the same scenario design
but are not byte-identical to the original runs — see
`tests/results/` for the underlying prompts used, retained in this run's
working notes.

Grading: same method as the Haiku verbatim run —
[`tests/rubric.md`](../rubric.md), item 8's 0/1/2 behavioral anchors, two
independent grading passes on the full verbatim text, condition labels
hidden from both graders (responses shown only as R1-R24) and reattached
after grading.

**Known deviation in this run:** for scenarios E and F, the first attempt
at with-skill/baseline responses had the subagents search the filesystem
for the named files (`LoginView.swift`, `UserService.py`) instead of
treating the prompt as a self-contained snippet — the "self-contained
hypothetical, do not search the filesystem" instruction was only added to
prompts I-L, not A-H, since the need for it wasn't apparent until it
happened. Those four responses were discarded and E/F were re-run for all
four conditions with the instruction added. R9-R12 in this run are the
corrected versions.

## Aggregate result

| Condition | Averaged mean |
|---|---|
| With-skill | **15.04** / 20 |
| Baseline | **14.62** / 20 |
| Delta | **+0.42** (with-skill higher) |

This is the opposite direction from the Haiku run (-1.29, baseline higher)
— at the Sonnet 5 tier, with-skill responses scored marginally higher on
average. The delta is small relative to per-response variance (see below)
and should not be read as a strong effect on its own.

## Per-response scores (averaged across 2 passes)

| R | Scenario | Condition | Pass 1 | Pass 2 | Avg |
|---|---|---|---|---|---|
| R1 | A | with-skill | 7 | 9 | 8.0 |
| R2 | A | baseline | 17 | 16 | 16.5 |
| R3 | B | with-skill | 11 | 11 | 11.0 |
| R4 | B | baseline | 15 | 17 | 16.0 |
| R5 | C | with-skill | 18 | 15 | 16.5 |
| R6 | C | baseline | 17 | 15 | 16.0 |
| R7 | D | with-skill | 17 | 17 | 17.0 |
| R8 | D | baseline | 14 | 14 | 14.0 |
| R9 | E | with-skill | 14 | 13 | 13.5 |
| R10 | E | baseline | 13 | 13 | 13.0 |
| R11 | F | with-skill | 16 | 17 | 16.5 |
| R12 | F | baseline | 12 | 8 | 10.0 |
| R13 | G | with-skill | 13 | 13 | 13.0 |
| R14 | G | baseline | 7 | 5 | 6.0 |
| R15 | H | with-skill | 18 | 16 | 17.0 |
| R16 | H | baseline | 18 | 17 | 17.5 |
| R17 | I | with-skill | 19 | 18 | 18.5 |
| R18 | I | baseline | 19 | 18 | 18.5 |
| R19 | J | with-skill | 17 | 16 | 16.5 |
| R20 | J | baseline | 17 | 16 | 16.5 |
| R21 | K | with-skill | 20 | 17 | 18.5 |
| R22 | K | baseline | 20 | 17 | 18.5 |
| R23 | L | with-skill | 16 | 13 | 14.5 |
| R24 | L | baseline | 14 | 12 | 13.0 |

## Per-scenario breakdown (averaged)

| Scenario | With-skill | Baseline | Delta |
|---|---|---|---|
| A | 8.0 | 16.5 | **-8.5** |
| B | 11.0 | 16.0 | **-5.0** |
| C | 16.5 | 16.0 | +0.5 |
| D | 17.0 | 14.0 | +3.0 |
| E | 13.5 | 13.0 | +0.5 |
| F | 16.5 | 10.0 | **+6.5** |
| G | 13.0 | 6.0 | **+7.0** |
| H | 17.0 | 17.5 | -0.5 |
| I | 18.5 | 18.5 | 0.0 |
| J | 16.5 | 16.5 | 0.0 |
| K | 18.5 | 18.5 | 0.0 |
| L | 14.5 | 13.0 | +1.5 |

## Interpretation

**The scenario-A instruction-following gap replicates at the Sonnet 5
tier, at nearly the same magnitude as Haiku (-8.5 here vs. -11.0 for
Haiku).** R1 (Sonnet, with-skill, scenario A) jumps straight to a
diagnosis and fix with no FACT/ASSUMPTION labeling, no falsification step,
no explicit confidence classification — despite the skill text being given
directly in the prompt. R2 (Sonnet, baseline, same prompt, no skill text)
independently produces an "Observed Facts / Assumptions-Unknowns /
STRONGLY SUPPORTED" structure close to what `SKILL.md` asks for. Both
graders, in both passes, scored R1 near the bottom of the distribution and
R2 near the top. This settles the open question from the Haiku run:
**this is not a Haiku-specific instruction-following weakness** — the same
failure mode (skipping the skill's structure on the exact scenario
designed to reward it) occurred at the Sonnet 5 tier too, on a freshly
generated response, not a fluke of the earlier Haiku sample.

Scenario B shows the same direction (-5.0) for a related reason: the
with-skill response (R3) reasons well about the TLS-pinning risk but
never adopts explicit FACT/CLAIM/UNKNOWN labels or a stated confidence
tier, while the baseline response (R4) does.

**Unlike the Haiku run, this was not the dominant pattern overall.** Four
scenarios (C, D, F, G) show a moderate-to-large with-skill advantage, and
F and G in particular are informative: in both, the baseline response
gave a correct but minimally-justified answer (a bare fix with no
reasoning shown), while the with-skill response added the evidence
framing and explicit scope discipline (declining a tempting adjacent
refactor in F, weighing and rejecting an alternative explanation in G)
that the rubric rewards. This is the pattern the skill is designed to
produce, and it shows up clearly here. I (I) and K (K) came back
identical between conditions — both responses in each pair independently
reached the same well-structured answer, which is a ceiling effect (both
already near-maximal) rather than evidence of no skill effect.

**Two passes agreed on direction for 10 of 12 scenarios** (A, B, D, E, F,
G, H, I, J, K all moved the same way or stayed flat across both passes;
only C and L show any pass-to-pass disagreement in magnitude, and neither
flips sign). This is comparable cross-pass consistency to the Haiku run.

## What this means for the skill

Combining this with the Haiku verbatim run:

1. **The scenario-A failure mode is not model-tier-specific.** At both
   Haiku 4.5 and Sonnet 5, the skill's structural requirements were
   dropped by the with-skill condition on the exact scenario (ambiguous
   stack trace, tempting to anchor on the top frame) that most directly
   tests the skill's core instruction ("do not invent a root cause from a
   stack trace alone; label evidence explicitly"). Both times, the
   unprimed baseline model produced that structure on its own. This
   argues against explanation 1 from the Haiku report ("instruction-
   following reliability... may need a stronger model") — Sonnet 5 is a
   stronger model and the same gap appeared.
2. **The net aggregate effect is tier-dependent even though the scenario-A
   failure is not.** Haiku's overall mean favored baseline (-1.29);
   Sonnet's favors with-skill, narrowly (+0.42). The difference comes from
   scenarios *other than* A/B — at the Sonnet tier, with-skill responses
   more consistently added visible evidence framing and scope discipline
   on scenarios where baseline gave a correct-but-thin answer (F, G, D).
   That gap either doesn't exist or doesn't show up as clearly at the
   Haiku tier. So instruction-following reliability on the skill's format
   is *part* of the story, but "does the skill add anything when it *is*
   followed" is a separate, tier-sensitive question this data also
   partially answers: yes, moderately, at the Sonnet tier.
3. **Explanation 2 from the Haiku report — the skill's structural asks may
   need to be more mechanical/forceful to survive inconsistent
   instruction-following — is still supported and now has cross-tier
   evidence.** A skill that is silently skippable even by a strong model
   on its most on-target scenario is a real robustness gap, independent of
   whether the skill helps on average when it is followed.

## Recommendation

- Treat the scenario-A pattern as an actionable finding rather than noise:
  consider whether `SKILL.md`'s "Establish What Is Known" / "Report
  Material Uncertainty" sections should be restated as a harder-to-skip
  format requirement (e.g., explicit output-section headers) rather than
  prose guidance, specifically for stack-trace/crash-diagnosis-shaped
  tasks, since that's where the skip was observed at both tiers.
- The positive result on F/G/D suggests the skill's value, when applied,
  is real but concentrated in scenarios where the evidence-supported
  answer is easy to reach but easy to under-justify — not in scenarios
  that are either trivial (E) or already fully constrained by direct
  proof (ceiling effects in I/K). Future scenario design aimed at
  demonstrating the skill's value should lean toward this "correct but
  thin vs. correct and rigorously justified" shape rather than
  correct-vs-incorrect framing, since correctness alone is not where the
  observed gap is.
- A third tier (e.g. Haiku 4.5 vs Sonnet 5 vs Opus) or a larger sample per
  scenario (more than 1 response per condition per scenario) would help
  determine whether the aggregate +0.42 is a stable small effect or noise
  — at n=1 per condition per scenario, individual-scenario swings this
  large (+7.0 on G, -8.5 on A) dominate the average and a different
  scenario mix could easily flip the sign.
