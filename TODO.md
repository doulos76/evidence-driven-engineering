# TODO

Follow-up work identified after v0.2.0. Not committed to a timeline —
pick up when there's a reason to.

## 1. Human spot-check of LLM rubric grading

The rubric benchmark in the README (Sonnet +2.83, Haiku +5.38 on the
20-point scale) is entirely LLM-graded: a grader subagent scored 96
verbatim responses blind to condition, two independent passes averaged.
No human has read the underlying responses and independently checked
whether the point gaps reflect real quality differences or the grader
reacting to surface patterns (e.g. presence of `FACTS:`/`ASSUMPTIONS:`
headers) rather than substance.

- Pick a handful of the largest-delta response pairs (scenario A is a
  good start — comparison already prepared) and read them side by side.
- Check whether the grader's point allocation matches independent
  judgment, especially on items 1 (evidence classification) and 5
  (uncertainty classification), which are the items most likely to
  reward formatting over content.
- Record findings in `tests/results/` regardless of outcome — if spot-check
  confirms the grading, say so; if it doesn't, that's a more important
  finding than the benchmark itself.

## 2. Re-run pass/fail scenario suite against SKILL.md v2

Pass/fail testing (`tests/scenarios.md`) was last run against the v1
(prose-guidance) `SKILL.md`. The v2 format-hardening change has only been
validated via the rubric — pass/fail hasn't been re-checked since. Given
pass/fail has been non-discriminating across all 4 prior runs, regression
risk is low, but it hasn't actually been confirmed for v2.

- Re-run all 12 scenarios, with-skill only (baseline unaffected by a
  skill-text change), against `SKILL.md` v2, both Sonnet 5 and Haiku 4.5.
- Confirm no scenario flips to FAIL under the new format requirement
  (most likely failure mode: over-processing a trivial task like
  scenario E because of the tightened "non-trivial by default" framing).

## 3. Larger sample size / additional model tier

Current rubric numbers are n=1 response per condition per scenario per
tier. Individual-scenario swings (e.g. scenario G showed +7.0 on the
20-point scale) dominate the tier average at this sample size.

- Consider 2-3 responses per condition per scenario to get a variance
  estimate, not just a point estimate.
- Consider adding a third tier (e.g. Claude Opus) to check whether the
  effect size trend (larger benefit at smaller/weaker models) holds or
  plateaus.

## 4. Clean up `tests/results/`

Nine files have accumulated there, mixing v1/v2 SKILL.md, summarized/
verbatim grading, and single/two-pass methodology, run across multiple
sessions. Useful as a raw history, but there's no single place that says
"here's the current state of the evidence, here's what's superseded."

- Consider a short `tests/results/README.md` index: which files are
  current/authoritative, which are superseded and why, in what order to
  read them if someone wants the full history.

## 5. Re-check CONTRIBUTING.md's "what to re-run" guidance

`CONTRIBUTING.md` tells contributors what to re-run and record when they
change `SKILL.md`. That guidance was written before this release's
multi-round evaluation (pass/fail → rubric → verbatim → two-pass → format
fix → full re-grade). Confirm it still reflects a reasonable minimum bar
for a `SKILL.md` change, rather than either the full v0.2.0 evaluation
cycle (too heavy for a small change) or the original lighter bar (now
known to be insufficient — see item 1).
