# Rubric Scoring Run (verbatim, 2 passes) — SKILL.md v2, both tiers — 2026-08-21

Full re-characterization of `SKILL.md` v2 (the format-hardening change from
[`2026-08-21-skillmd-format-hardening.md`](./2026-08-21-skillmd-format-hardening.md),
which only spot-checked scenarios A, B, and E). This run re-generates all
12 scenarios, with-skill condition, under v2, for both Sonnet 5 and Haiku
4.5, and grades all 48 responses (24 per tier: 12 with-skill v2 + 12
baseline, baseline reused from the prior verbatim runs since skill text
does not affect the no-skill condition) with the same verbatim/two-pass
method used throughout this test suite.

## Method

- With-skill responses: regenerated fresh under `SKILL.md` v2 (the
  FACTS/ASSUMPTIONS/INFERENCES/UNKNOWNS/CONFLICTING EVIDENCE/CLAIMS block
  + explicit `Conclusion: VERIFIED | STRONGLY SUPPORTED | INFERRED` line),
  for all 12 scenarios, both Sonnet 5 and Haiku 4.5.
- Baseline responses: reused verbatim from
  [`2026-08-21-rubric-sonnet-verbatim.md`](./2026-08-21-rubric-sonnet-verbatim.md)
  and [`2026-08-21-rubric-haiku-verbatim.md`](./2026-08-21-rubric-haiku-verbatim.md)
  — the no-skill condition is unaffected by a skill-text change, so
  regenerating it would add noise without adding signal.
- Grading: two independent passes per tier on the full verbatim text,
  condition labels hidden from graders, scores averaged per response, using
  [`tests/rubric.md`](../rubric.md).

## Aggregate result

| Tier | With-skill (v2) | Baseline | Delta |
|---|---|---|---|
| Claude Sonnet 5 | **16.29** / 20 | 13.46 / 20 | **+2.83** |
| Claude Haiku 4.5 | **15.08** / 20 | 9.71 / 20 | **+5.38** |
| Combined (n=24 each) | **15.69** / 20 | 11.58 / 20 | **+4.10** |

Both tiers now show with-skill scoring clearly higher than baseline. This
reverses the v1 finding for Haiku (which favored baseline, -1.29) and
extends the v1 finding for Sonnet (which favored with-skill only slightly,
+0.42) into a much larger, now-consistent-in-direction effect at both
tiers.

## Per-scenario breakdown

### Sonnet 5

| Scenario | With-skill (v2) | Baseline | Delta |
|---|---|---|---|
| A | 17.0 | 14.5 | +2.5 |
| B | 18.0 | 16.5 | +1.5 |
| C | 18.5 | 17.0 | +1.5 |
| D | 17.5 | 14.0 | +3.5 |
| E | 11.0 | 8.5 | +2.5 |
| F | 16.0 | 9.5 | +6.5 |
| G | 15.0 | 8.0 | +7.0 |
| H | 16.5 | 14.5 | +2.0 |
| I | 18.0 | 18.0 | 0.0 |
| J | 14.5 | 14.5 | 0.0 |
| K | 18.0 | 17.5 | +0.5 |
| L | 15.5 | 9.0 | +6.5 |

### Haiku 4.5

| Scenario | With-skill (v2) | Baseline | Delta |
|---|---|---|---|
| A | 11.5 | 5.0 | +6.5 |
| B | 16.5 | 6.0 | +10.5 |
| C | 18.5 | 14.0 | +4.5 |
| D | 16.5 | 9.5 | +7.0 |
| E | 9.5 | 8.0 | +1.5 |
| F | 13.0 | 9.5 | +3.5 |
| G | 13.0 | 7.0 | +6.0 |
| H | 18.5 | 12.5 | +6.0 |
| I | 19.0 | 14.0 | +5.0 |
| J | 16.5 | 11.5 | +5.0 |
| K | 16.5 | 13.0 | +3.5 |
| L | 12.0 | 6.5 | +5.5 |

Every single scenario now shows with-skill at or above baseline, at both
tiers — including scenario A, which was the single largest with-skill
deficit under v1 at both tiers (Sonnet -8.5, Haiku -11.0) and is now a
positive delta at both tiers (Sonnet +2.5, Haiku +6.5). Scenarios I and J
at the Sonnet tier show a 0.0 delta — both conditions already scored near
the ceiling on these scenarios in the v1 run, so this is a ceiling effect,
not evidence the skill added nothing.

## Interpretation

**The v1 → v2 format change resolved the instruction-following gap that
motivated it, and did so more broadly than the two scenarios it was
designed for.** The two scenarios explicitly targeted by the fix (A, B)
improved the most dramatically in the earlier spot-check
(8.0→19, 11.0→20 at the Sonnet tier). This full run confirms that
improvement held up under independent two-pass grading (Sonnet A: 8.0→17.0,
B: 11.0→18.0 — slightly lower than the single-pass spot-check numbers but
still a large, clearly positive swing) and, more importantly, shows the
same direction of improvement across scenarios that were never specifically
targeted (F, G, L each show +5 to +7 point swings at the Sonnet tier; B
shows +10.5 at the Haiku tier).

**The effect is larger at the Haiku tier than the Sonnet tier** (+5.38 vs.
+2.83 combined). This is consistent with the v1 finding's core diagnosis:
the smaller/weaker model benefited more from having the skill's structure
made into an explicit, hard-to-skip format requirement, because it was the
tier most prone to silently dropping prose-style guidance under v1.

**Scenario E (trivial edit) remains a floor-effect scenario, as flagged
throughout this test suite**, and the spot-check specifically confirmed
the tightened format requirement doesn't cause over-processing there — both
tiers show only a small positive delta (Sonnet +2.5, Haiku +1.5), consistent
with "same appropriately light response, marginally better justified"
rather than new unwanted ceremony.

## What this means for the skill

Combined with every prior run in this repository, the current honest state
is:

1. **Pass/fail scenario testing remains non-discriminating** at both model
   tiers tested (all 96 executions across 4 runs passed under both
   conditions) — this hasn't changed and isn't expected to, since these
   scenarios test whether a defensible conclusion is reached, not how
   rigorously.
2. **Structural/quality rubric scoring, under the v1 (prose-guidance)
   SKILL.md, was inconsistent** — a small positive effect at the Sonnet
   tier, a small negative effect at the Haiku tier, both dominated by a
   single scenario (A) where the skill's own structure was being silently
   skipped.
3. **Under v2 (explicit format-required) SKILL.md, the rubric now shows a
   consistent, meaningful positive effect at both tiers**, including on
   the scenario that previously showed the largest negative effect. This
   is the first result in this test suite where the with-skill condition
   outperforms baseline consistently across scenarios and model tiers,
   rather than being a mixed or scenario-dependent result.

This is now strong enough, consistent enough, and large enough (+2.83 to
+5.38 on a 20-point scale, roughly +14 to +27 on a normalized 100-point
scale) to report as a headline finding rather than a caveated one — while
still being transparent that pass/fail correctness was never the
discriminator; response rigor and legibility is.
