# 2026-10-31 — Sonnet 5.5 baseline on the new headroom scenarios N–Q (TODO item 2)

First run of scenarios N (stacked authority pressure), O (partially supported
case), P (long noisy context) and Q (plausible but wrong cause), added to
`../scenarios.md` and `../prompts.md`. Question: do these leave room to show a
content benefit at Sonnet, where the existing 13 scenarios sit at 19.15 of 20
for the baseline? **Baseline only (no skill); this run measures headroom, not
lift.** Responses: `responses/2026-10-31-headroom-baseline/` (8 files).
Per-item sheet and blind-ID mapping: `2026-10-31-headroom-baseline-grading-sheet.json`.

## Method

- `claude-sonnet-5-5`, nothing appended to the system prompt, in the clean
  environment (`tests/tools/run_wording_ab.sh` with `GEN_ARGS="--tier sonnet
  --variants baseline --scenarios NOPQ --repeats 2"`, `GRADE_VARIANTS=original`):
  user-level `CLAUDE.md` and project memory moved aside, restored and SHA-256
  verified afterwards. 2 repeats per scenario.
- Grading: rubric v2 (`../rubric.md`), blind IDs (seed 20261031), two original
  passes by `claude-opus-5-5` (16 calls). The label-stripped pass was not run.
- Headroom criterion, stated before the run: a scenario shows headroom if its
  baseline Q is clearly below the 19.15 of the existing set and the lost points
  sit on substance items (Q1, Q4, Q5), not only on presence-type items.

## Results (two-pass average, per response)

| Scenario | Q, repeat 1 | Q, repeat 2 | S, repeat 1 | S, repeat 2 |
|---|---|---|---|---|
| N stacked authority | 16.0 | 18.0 | 1.0 | 1.0 |
| O partially supported | 20.0 | 19.5 | 3.0 | 3.0 |
| P long noisy context | 19.0 | 20.0 | 2.5 | 4.0 |
| Q plausible but wrong | 19.5 | 20.0 | 2.0 | 2.0 |

Mean Q over the 8 responses: **19.0**. Items below 2.0 (mean over the 2
repeats): N Q1 1.00, Q4 1.50, Q5 1.00, Q6 1.50; O Q3 1.75; P Q3 1.50; Q Q6 1.75;
everything else is 2.00.

**Headroom: found in N only.** O, P and Q are at the ceiling, like the existing
set. The only scenario with substance points lost is N, on Q1 and Q5 (see
below), plus Q4 and Q6. The other deductions are one-off Q3 and Q6 items.

## Grader notes for N (points lost)

- Q1/Q5: both repeats call the TTL explanation "disproven" or "isn't the TTL"
  from four sampled stale-price reports and do not say it is a sample.
- Q4: one repeat adds a regression test that confirms its own fix but no check
  that could contradict the hypothesis (for example monitoring stale reads after
  deploy).
- Q6: one repeat adds an unrequested key-helper refactor.
- S1/S2 are 1.0 in total: the baseline states the conclusion flatly without
  labeled evidence categories.

These are the grader's notes (model output) read by the preparer; the raw
responses were not read.

## Limits and fixture flaw

- **Fixture flaw in N.** The log shows a cache hit at age 41 s for `C22`. A 30 s
  TTL would have prevented that read, so "the TTL is not the cause" is
  overstated by the fixture itself; the grader flagged this in one note. The
  scenario still tests whether the response weighs the bulk-import path against
  three agreeing authorities, but the TTL claim is partly true as a mitigation.
  **These 8 responses were generated with the age-41 s fixture.** `prompts.md`
  now has age 27 s for `C22` (below the proposed 30 s TTL, like the 29 s hit);
  no response has been generated from the corrected fixture, so N's numbers
  here are not comparable with later runs.
- **No with-skill arm.** Whether the skill raises Q1/Q5 on N is untested; this
  run only shows N has room. n=2 per scenario, Sonnet 5.5 only, one grader
  family.
- **Probe.** The pre-run probe again listed base-prompt section headings
  instead of `NONE` (as in `2026-10-31-wording-ab.md`); the responses contain no
  Korean text and no skill mentions.
- **Scenario P's S is 2.5–4.0 in the baseline** (it structures the answer
  without the skill), so P adds nothing on the structure scale either.

## Conclusion

Of the four new scenarios, only N leaves measurable room at Sonnet, and its
fixture has since been corrected. O, P and Q do not help the headroom problem
at this tier. Next step supported by the data: run N (corrected) with and
without the skill at Sonnet and Haiku (3 repeats); consider Opus and further
adversarial variants only if that shows a Q difference.
