# 2026-10-28 — Pass/fail on the clean-run responses

Pass/fail judgment, against `../scenarios.md`, of all 60 responses from
`2026-10-28-rubric-v03-clean-env.md` (`responses/2026-10-28-v03-clean/`),
**both conditions**. Earlier runs judged with-skill responses only.

## Method

- Responses blinded with the random IDs R01–R60 from the v2 re-grade
  (frontmatter stripped); judges saw only the scenario letter, the scenario's
  Pass/Fail criteria, the scenario prompt and the response.
- Four judge agents (`sonnet`), 15 responses each, deciding PASS/FAIL strictly
  by the scenario's stated Fail criterion rather than general quality.

## Result

**60 of 60 PASS** — 15 of 15 in each of the four cells (Sonnet and Haiku ×
with-skill and baseline). No response met a scenario's Fail criterion.

## Reading

- Pass/fail is again **non-discriminating**, as in every earlier run: baseline
  responses already avoid the specific failure modes the scenarios test. It
  works as a regression guard, not as a measure of the skill's benefit.
- Pass/fail also does not capture the failures the v2 rubric found. For
  example, the Haiku `G` responses in both conditions show an unrun test as
  passing although the prompt said not to assume tests were run; scenario G's
  Pass/Fail criteria do not cover that, so they pass.
- No with-skill response was borderline in this run (one was in the earlier
  2026-10-05 run).

## Limitations

One judge family (Sonnet), single judgments, no second reading of any case;
the judges ran with the maintainer's global instructions loaded (judging
against explicit criteria is less sensitive to them than generation, but it is
a difference from the clean generation run).
