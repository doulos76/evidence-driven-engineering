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

## 1. Act on the human spot-check

A first spot-check is recorded in
`tests/results/2026-10-28-human-spotcheck-materials.md` (one reader, four
pairs, judged from condensed summaries): same conclusions and actions in every
pair; content judged equal on one pair, better with the skill on two, unsure
on one; overall impression "labeling and structure improve, content similar".
It also showed the grader over-rewarding labels (Haiku G) and under-rewarding
an addition (Sonnet K). Still open:

- A second reader, reading the raw response files rather than summaries, on
  more pairs (including pairs with small lifts).
- Decide whether to revise the rubric so label presence and substance are
  scored separately (items 1 and 5 carry about 80% of the Sonnet lift), then
  re-grade before citing a headline number again.
- Decide what the README should claim about EDE given that the measured gain
  is mostly explicitness and confidence labeling.

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
