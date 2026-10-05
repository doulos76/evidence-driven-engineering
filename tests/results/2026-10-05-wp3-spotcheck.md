# 2026-10-05 — WP3 spot-check: SKILL.md additions (architecture section + references pointer)

## What changed and why this run exists

`SKILL.md` revision `7c00e4e` inserted two sections into the v2 text,
changing nothing else: `Decide Architecture on Evidence` (between
Reconstruct Context and Classify the Conclusion) and `Going Deeper`
(a two-line pointer to `references/` at the end). Under
CONTRIBUTING.md's minimum bar for a non-trivial `SKILL.md` change, the
affected scenarios were rerun with-skill and rubric spot-checked.

This is also the **first run to use the reconstructed canonical prompts
in `tests/prompts.md`** (added this cycle) rather than ad-hoc prompts,
and the first to store verbatim responses under
`tests/results/responses/` per the storage convention.

## Method

- Scenarios: **M** (new, directly tests the added architecture section;
  with-skill *and* baseline) and regression **A, B, E** (with-skill
  only; E additionally at the Haiku tier, since over-processing a
  trivial task was the named regression risk of tightening the skill).
- Generation: one response per cell. With-skill = the generating agent
  loads `SKILL.md`@`7c00e4e` and nothing else; baseline = no skill.
  Prompts verbatim from `tests/prompts.md`.
- Grading: one pass per response, blind to condition, from verbatim
  text, against `tests/rubric.md` (10 items, 0–2). Grader was a
  stronger model tier than the generators.
- Verbatim responses: `responses/2026-10-05-wp3-spotcheck/`.

## Results

| Scenario | Condition | Generator | Pass/fail | Rubric (1-pass) |
|---|---|---|---|---|
| M | skill | claude-sonnet-5-5 | PASS | 20/20 |
| M | baseline | claude-sonnet-5-5 | PASS | 20/20 |
| A | skill | claude-sonnet-5-5 | PASS | 20/20 |
| B | skill | claude-sonnet-5-5 | PASS | 20/20 |
| E | skill | claude-sonnet-5-5 | PASS | 19/20 |
| E | skill | claude-haiku-4-5-20251001 | PASS | 13/20 |

Pass/fail judged against `tests/scenarios.md` criteria:

- **M (skill):** declined to commit to the migration on assumed scale,
  separated measured constraints from anticipated needs in the FACTS
  block, compared four options including staying on the monolith, and
  resisted the product lead's framing with specific counter-evidence.
  The new section's required behaviors are all visibly present. PASS.
- **M (baseline):** also refused to commit and demanded measurement
  first — pass/fail remains non-discriminating on M at this tier,
  consistent with every prior run of the suite.
- **A (skill):** did not anchor on the top frame; identified
  `apply_patch`'s omitted-field overwrite via the full v2 FACTS block,
  attempted falsification, `Conclusion: STRONGLY SUPPORTED`. No
  regression of the v2 format-hardening behavior.
- **B (skill):** treated deletion as unproven (H1/H2 undecidable on
  supplied evidence), named the decisive API 21–22 device test,
  `Conclusion: INFERRED`. No regression.
- **E (skill, both tiers):** concise edit with no hypothesis
  manufacturing or risk report — the named regression risk
  (over-processing a trivial task after the insertions) did **not**
  materialize at either tier. The Sonnet response added a short
  unverified-areas note and a grep suggestion; the Haiku response was
  minimal. Both within intended Scenario E behavior.

## Interpretation

1. **No regression from the WP3 insertions.** All with-skill responses
   kept the v2 structure, and E stayed lightweight at both tiers.
2. **Scenario M does not discriminate at this tier/environment** — both
   conditions hit the rubric ceiling (20/20). The with-skill response
   shows the added section's exact vocabulary (irreversible commitment,
   keep-the-current-design option, UNKNOWNS in the decision record), so
   the section *is* being applied; but a strong baseline already
   refuses evidence-free migrations. A harder M variant (e.g. pressure
   plus a partially supported migration case) would be needed for a
   discriminating signal.

## Limitations (read before citing these numbers)

- n=1 per cell, single grading pass — weaker than the two-pass method
  used for the v0.2.0 benchmark; this run is a regression gate, not a
  benchmark update. The README benchmark table still describes
  revision `c210165` (v2) and awaits a full rerun.
- Generator tiers are claude-sonnet-5-5 / claude-haiku-4-5 — a newer
  Sonnet than the "Sonnet 5" used in the 2026-08-21 runs. Scores are
  not comparable across runs.
- The generation environment carries user-level global agent
  instructions that themselves demand fact/assumption separation; this
  plausibly inflates baseline structure scores (M baseline 20/20) and
  is a standing confound for every run from this environment. Noted
  for the planned human spot-check (TODO item 1).
- Responses were generated in Korean (environment default); the rubric
  is language-agnostic and grading was done on substance, but this
  differs from the English responses of prior runs.
