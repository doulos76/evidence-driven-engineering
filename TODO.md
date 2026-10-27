# TODO

Follow-up work, updated after the clean-environment rerun
(`tests/results/2026-10-28-rubric-v03-clean-env.md`). Not committed to a
timeline — pick up when there's a reason to.

Done and removed from the list: the environment-confound rerun (Sonnet
+1.50, Haiku +1.96 in a clean environment, versus +0.12 / +2.29 with the
maintainer's instructions present), pass/fail against the current
`SKILL.md` (30/30 in the 2026-10-05 run), the `tests/results/README.md`
index, the updated CONTRIBUTING.md evaluation bar, scenario prompts in
`tests/prompts.md`, and n=2 on scenarios A and G.

## 1. Human spot-check of LLM rubric grading

Still open, and now sharper. In the clean run, items 1 (evidence
classification) and 5 (uncertainty classification) account for about 80%
of the Sonnet lift and two thirds of the Haiku lift, while the
substance-measuring items (falsification, scope, verification, authority
resistance) barely move — so whether the lift reflects better engineering
or better labeling is exactly what a human has to judge. Materials are prepared in
`tests/results/2026-10-28-human-spotcheck-materials.md`: four pairs from the clean
run (Haiku G and C, Sonnet M, and Sonnet K as a control) with per-item scores,
the grader's reasons, and a checklist. The verdict section is blank and needs
a human reader.

## 2. Pass/fail on the clean run

The 2026-10-28 run graded the rubric only. Judge the 30 with-skill
responses against `tests/scenarios.md` as well.

## 3. A second grader family

Both grading passes used one model (`claude-opus-5-5`). Re-grade a sample
with a different grader (another model family, or a human) to check the
item-level pattern above is not a grader artifact.

## 4. A harder scenario set and more repeats

Add adversarial variants (stacked authority pressure, partially supported
cases, longer noisy context) — the baseline already scores 2.00 on
authority resistance, so scenarios I and J cannot show an effect — consider
a third tier (Claude Opus), and run 2–3 repeats everywhere: only scenarios A
and G ran n=2, and single-response cells swing by a point or more.
