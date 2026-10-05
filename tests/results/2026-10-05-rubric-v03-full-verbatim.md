# 2026-10-05 — Full rubric rerun, SKILL.md revision 7c00e4e (v0.3 cycle)

Full-suite rerun after the v0.3-cycle `SKILL.md` additions
(`Decide Architecture on Evidence`, `Going Deeper`), covering all 13
scenarios (A–M) at both model tiers, with-skill **and freshly generated
baseline**, graded verbatim, blind to condition, in two independent
passes. Verbatim responses: `responses/2026-10-05-v03-full/` (60 files).
Scenario inputs: `../prompts.md` (reconstructed canonical prompts).

## Method

- Generators: claude-sonnet-5-5 and claude-haiku-4-5-20251001, one
  response per cell; scenarios **A and G ran n=2** (the two scenarios
  with the largest swings in earlier runs) to get a variance signal.
  With-skill = generator loads `SKILL.md` at `7c00e4e`; baseline = no
  skill. Prompts verbatim from `../prompts.md`.
- Blinding: 60 responses shuffled (seeded) into random IDs R01–R60 with
  YAML frontmatter stripped; graders saw only the text and the scenario
  prompt.
- Grading: 8 grader instances, 2 independent passes × 4 batches of 15,
  against `../rubric.md` (10 items, 0–2). Grader tier is stronger than
  both generators. Pass agreement: mean |pass1 − pass2| = **0.45** points
  per response.
- Pass/fail (scenarios.md criteria) was judged for the **with-skill
  responses only** (30/30 PASS; `G-skill-sonnet-r2` borderline — it
  lists two alternative hypotheses but rejects each in one line and goes
  straight to the fix). Baseline pass/fail was not rerun; pass/fail has
  been non-discriminating in every earlier run.

## Results (two-pass average, mean over 13 scenarios, repeats averaged)

| Tier | No skill | EDE | Lift |
|---|---|---|---|
| Claude Sonnet 5.5 | 19.83 / 20 | 19.94 / 20 | **+0.12** |
| Claude Haiku 4.5 | 16.19 / 20 | 18.48 / 20 | **+2.29** |

Per-scenario lift (with-skill − baseline):

| | A | B | C | D | E | F | G | H | I | J | K | L | M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sonnet | 0.0 | 0.0 | 0.0 | 0.0 | +1.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Haiku | +7.8 | +2.0 | +2.0 | +2.0 | −0.5 | +2.5 | +3.5 | +0.5 | +2.0 | +2.0 | +1.0 | +3.0 | +2.0 |

## What this does and does not show

1. **Haiku: a consistent, real-looking lift** — with-skill is at or above
   baseline on 12 of 13 scenarios; the exception, E (trivial edit), is
   −0.5, i.e. no over-processing. Scenario A is the largest effect
   (+7.8): the Haiku baseline tends to anchor on the top frame and give
   a thin answer, while with-skill responses use the FACTS block. Scenario
   M (the new architecture section) shows +2.0 at Haiku.
2. **Sonnet: ceiling, no measurable lift.** 12 of 13 scenarios are
   20/20 in both conditions. The rubric cannot discriminate at this tier
   with these prompts; this run neither supports nor contradicts a
   Sonnet-tier benefit.
3. **The lift is smaller than the v0.2.0 benchmark (Sonnet +2.83, Haiku
   +5.38) and the two are not comparable** (see limitations): different
   generator versions, regenerated baselines, a different language, and
   an environment confound.
4. **Variance is visible where expected.** Scenario G at Haiku with-skill
   scored 18.0 and 15.5 across the two repeats, baseline 15.5 and 11.0;
   the largest per-response pass disagreements were on Haiku baselines
   (`A-baseline-haiku-r2` 8 vs 12, `G-baseline-haiku-r1` 14 vs 17). A
   single sample of any one cell should not be trusted.
5. **No regression from the v0.3 insertions** — E stayed lightweight at
   both tiers; every with-skill response passed.

## Limitations (read before citing these numbers)

- **Environment confound.** Generator agents ran in an environment that
  carries the maintainer's user-level instructions, which themselves
  require separating verified facts from inference and stating
  confidence. Baseline responses frequently show that structure
  unprompted (e.g. `[확인된 사실]` / `[추정/추론]` sections and a closing
  confidence line), so baselines are plausibly inflated, and the Sonnet
  ceiling is partly an artifact of it. A clean rerun in an environment
  without such instructions is needed before reading the Sonnet result as
  "no benefit."
- n=1 per cell (n=2 for A and G); two grading passes by one grader
  model family; no human has read the grading (see
  `2026-10-05-human-spotcheck-materials.md`).
- Responses were generated in Korean (environment default); earlier runs
  were English. The rubric is language-agnostic, but the runs differ.
- Generators are newer model versions than the "Sonnet 5" of the
  2026-08-21 runs, and baselines were regenerated rather than reused.
- Prompts are reconstructed (`../prompts.md`), not the lost originals.
