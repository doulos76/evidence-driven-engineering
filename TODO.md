# TODO

Follow-up work, updated after the v0.3-cycle full rerun
(`tests/results/2026-10-05-rubric-v03-full-verbatim.md`). Not committed to
a timeline — pick up when there's a reason to.

Done in this cycle and removed from the list: pass/fail rerun against the
current `SKILL.md` (with-skill 30/30 PASS), `tests/results/README.md`
index, the updated CONTRIBUTING.md evaluation bar, scenario prompts in
`tests/prompts.md`, and n=2 on scenarios A and G.

## 1. Human spot-check of LLM rubric grading

Still open, and now the most important item. The rubric benchmark is
entirely LLM-graded (two independent passes by one grader model family);
no human has read the responses. Materials are prepared in
`tests/results/2026-10-05-human-spotcheck-materials.md` (Haiku scenario A,
+7.8, and scenario G, +3.5, side by side). A human needs to read them and
fill in the verdict section — if the spot-check does not confirm the
grading, that outranks the benchmark itself.

## 2. Clean rerun without environment confound

The v0.3 run's baselines show the evidence structure unprompted, very
likely because the generation environment carries user-level instructions
asking for exactly that. Rerun the baseline (and with-skill) generation in
an environment without such instructions, ideally in English to match the
2026-08-21 runs, before reading the Sonnet-tier "no lift" result (+0.12,
12 of 13 scenarios at the 20/20 ceiling) as "no benefit."

## 3. A harder scenario set for the stronger tier

At Sonnet the rubric saturates. Add adversarial variants (stacked
authority pressure, partially supported cases, longer noisy context) —
scenario M in particular needs a harder version, since baseline already
refuses an evidence-free migration — and consider a third tier (Claude
Opus) to check whether the larger-benefit-at-smaller-models trend holds.

## 4. More repeats

Only scenarios A and G ran n=2. Haiku with-skill G scored 18.0 and 15.5
across repeats, so single-sample cells are noisy; 2–3 repeats everywhere
would give a variance estimate for every scenario.
