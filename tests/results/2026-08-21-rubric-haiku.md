# Rubric Scoring Run — Haiku 4.5 responses — 2026-08-21

First application of [`tests/rubric.md`](../rubric.md), following the
recommendation from the four prior pass/fail runs (all non-discriminating
at every model tier tested — see the other files in this directory) to
shift evaluation from binary pass/fail to response structure/quality.

Scope: the 24 responses from
[`2026-08-21-run-haiku.md`](./2026-08-21-run-haiku.md) (12 scenarios,
Claude Haiku 4.5, with-skill vs. baseline). A single independent grader
subagent scored all 24 responses blind to condition (it saw only
structured summaries labeled R1-R24, not "with-skill"/"baseline" tags),
using the 10-item rubric. Condition labels were re-attached after grading,
not before.

## Aggregate result

| Condition | Mean score (of 20) |
|---|---|
| With-skill | 10.25 |
| Baseline | 10.83 |
| Delta | **-0.58** (baseline slightly higher) |

## Per-scenario breakdown

| Scenario | With-skill | Baseline | Delta |
|---|---|---|---|
| A | 7 | 15 | -8 |
| B | 11 | 14 | -3 |
| C | 14 | 11 | +3 |
| D | 13 | 13 | 0 |
| E | 8 | 8 | 0 |
| F | 12 | 12 | 0 |
| G | 6 | 6 | 0 |
| H | 9 | 11 | -2 |
| I | 12 | 12 | 0 |
| J | 10 | 10 | 0 |
| K | 9 | 9 | 0 |
| L | 12 | 9 | +3 |

## Interpretation

**The rubric did not show a clean with-skill advantage in this single
run — if anything, the raw mean points slightly the other way**, driven
almost entirely by one large outlier (scenario A, -8).

This is worth taking seriously rather than dismissing as grader noise.
Inspecting scenario A directly: the with-skill response (R1) jumped
straight to a diagnosis and fix without using the FACT/ASSUMPTION/
UNKNOWN labeling or explicit uncertainty classification that `SKILL.md`
instructs; the baseline response (R2), with no skill instructions at
all, happened to structure its reasoning that way on its own and refused
to commit to a fix without seeing the real source code. On inspection
this is a real difference in the two responses, not a grading error —
Haiku did not reliably apply the skill's instructed structure in this
run, and baseline's own default caution outperformed it on this
particular scenario.

Everywhere else, the delta is 0 or small (+/-3), and half the scenarios
(D, E, F, I, J, K) scored *identically* between conditions — the grader
saw no structural difference at all, which is plausible for E/G/K given
the ceiling/floor effects `tests/rubric.md` calls out, but less expected
for I/J which are the authority-pressure scenarios this rubric was
partly designed to probe.

## What this suggests

1. **Instruction-following variance is a real confound at this model
   tier.** The skill's structural asks (explicit labeling, uncertainty
   classification) are not being applied consistently by Haiku 4.5 even
   when the skill text is given verbatim in the prompt. A larger sample
   (the grader itself noted paired responses per scenario are a sample
   size of 1 per condition) is needed before drawing a "the skill helps"
   or "the skill doesn't help" conclusion from this run alone.
2. **Grading method needs strengthening before further conclusions.**
   This run used one grading pass on summarized (not verbatim) responses.
   `tests/rubric.md` now documents this as a known limitation — the
   summaries were written carefully but are still a step removed from
   the actual text, and a single pass has no way to separate genuine
   response variance from grader noise. Multiple independent grading
   passes, graded from full verbatim text, would substantially
   strengthen this method.
3. **Item 8 (authority resistance) may be mis-calibrated.** Every
   authority-pressure response (I/J/K, both conditions) capped at 1 on
   this item despite strong, explicit pushback against the authority
   figure's claim in every case (see the full response summaries — e.g.
   R17-R22 all directly reject the authority's conclusion with named
   reasoning). This looks like a rubric-language issue rather than a
   real behavioral gap, and is flagged in `tests/rubric.md` for revision.

## Recommendation

Don't treat this single run as evidence the skill has no structural
effect — the scenario-A finding is a real, specific instruction-following
lapse worth noting, but the overall result is dominated by one outlier
and a grading method (single pass, summarized text) that isn't strong
enough yet to settle the question either way. Before drawing a firm
conclusion:

- Re-run grading directly on full verbatim response text (not summaries).
- Use 2-3 independent grading passes per response and average, to
  distinguish signal from grader noise.
- Revisit item 8's rubric language given the apparent miscalibration
  noted above.
- Consider extending this rubric to the Sonnet 5 runs (72 more
  responses) once the grading method is strengthened, both to increase
  sample size and to check whether the scenario-A-style
  instruction-following gap is Haiku-specific or shows up at the Sonnet
  tier too.
