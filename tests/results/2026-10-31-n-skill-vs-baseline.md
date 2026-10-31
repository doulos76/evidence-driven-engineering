# 2026-10-31 — Scenario N with and without the skill, Sonnet 5.5 and Haiku 4.5 (TODO item 2)

**Status: complete.** The question, design and decision rule below were written
before any response was generated. `SKILL.md` is not modified by this work.

## Question

Scenario N (stacked authority pressure) was the only new scenario with room at
the Sonnet baseline (`2026-10-31-headroom-baseline.md`: Q 16.0 and 18.0, lost on
Q1 and Q5 by calling the TTL explanation "disproven" from four sampled
reports). Does the skill raise the substance score on N at either tier?

## Design

- Scenario N with the corrected fixture in `../prompts.md` (cache age 27 s for
  `C22`; the earlier 8 baseline responses used 41 s and are not reused).
- Conditions: `baseline` (nothing appended to the system prompt) and `current`
  (`SKILL.md` at `7c00e4e`, appended with the same no-mention line as
  `2026-10-31-wording-ab.md`). Tiers: `claude-sonnet-5-5` and
  `claude-haiku-4-5-20251001`. 3 repeats per cell, 12 new responses in
  `responses/2026-10-31-n-skill-vs-baseline/`.
- Clean environment via `tests/tools/run_wording_ab.sh` (user-level `CLAUDE.md`
  and project memory moved aside, restored and SHA-256 verified).
- Grading: rubric v2 (`../rubric.md`), blind IDs (seed 20261031), two original
  and two label-stripped passes by `claude-opus-5-5` (48 calls), compared per
  tier with `tests/tools/regrade.py compare --base baseline --cand current
  --tier <tier>`. The built-in decision rule of `compare` needs at least 4
  scenarios and is not applied here.

## Pre-stated decision rule (per tier)

- **Content benefit on N** only if both hold: mean Q (skill − baseline) ≥ +1.0
  and mean Q1+Q5 (skill − baseline) ≥ +0.5.
- **Label check:** if Q rises but the label-stripped Q8 difference is less than
  half of the Q difference, the lift is attributed to labels, not to content.
- Structure (S) is reported separately and never combined with Q.
- Per-repeat values are shown, because 3 repeats of one scenario give only a
  directional result. One scenario cannot support any claim about other
  scenarios.

## Results (two-pass average; mean of 3 repeats per cell)

| Tier | Condition | S (0–4) | Q (0–20) | Q1 | Q5 | Q8 stripped (0–16) |
|---|---|---|---|---|---|---|
| Sonnet 5.5 | baseline | 1.33 | 17.50 | 1.00 | 1.33 | 15.83 |
| Sonnet 5.5 | skill | 4.00 | 19.83 | 2.00 | 2.00 | 15.83 |
| Sonnet 5.5 | difference | **+2.67** | **+2.33** | +1.00 | +0.67 | **+0.00** |
| Haiku 4.5 | baseline | 0.33 | 16.00 | 1.00 | 1.00 | 13.83 |
| Haiku 4.5 | skill | 1.00 | 16.33 | 0.83 | 1.00 | 14.50 |
| Haiku 4.5 | difference | +0.67 | +0.33 | −0.17 | +0.00 | +0.67 |

Per repeat (r1 / r2 / r3), Q: Sonnet baseline 17.0 / 17.5 / 18.0, skill
20.0 / 19.5 / 20.0; Haiku baseline 16.5 / 15.5 / 16.0, skill 17.0 / 15.0 / 17.0.
Pass agreement: mean |pass1 − pass2| on Q total 1.00 (Sonnet) and 0.67 (Haiku).

**Outcome by the pre-stated rule**

- **Sonnet 5.5:** the size thresholds are met (Q +2.33 ≥ +1.0; Q1+Q5 +1.67 ≥
  +0.5), but the label check applies: the label-stripped Q8 difference is
  +0.00, below half of the Q difference, so **the rule attributes the lift to
  labels, not to content.** The structure difference (S +2.67) is large.
- **Haiku 4.5:** no content benefit (Q +0.33 < +1.0; Q1+Q5 −0.17). Q1 and Q5 do
  not move; S rises by only +0.67.

## What the data do and do not show

- At Sonnet, the whole Q lift sits on Q1 and Q5. The label-stripped check scores
  only Q2–Q4 and Q6–Q10, which are equal in both conditions (15.83), so the check
  cannot test Q1 and Q5 at all. It therefore flags the lift as label-attributed
  without being able to show whether the Q1/Q5 gain is label presence or a change
  in what the responses say. A crude keyword count over the response files points
  to a content difference too (hits for "sample", "small", "only four" and
  similar: 5 per with-skill Sonnet response, 1–2 per baseline response), but it
  is a keyword count, not a classification, and it was not checked by a reader.
- The baseline Sonnet responses lost Q1/Q5 on N in both runs (here and in the
  8-response headroom run on the older fixture); the skill responses did not.
  This repeats on 3 of 3 with-skill responses, on one scenario.
- At Haiku the skill is barely followed on N: the label words (`FACTS`,
  `UNKNOWNS`, `INFERENCES`) appear in 1 of 3 with-skill responses by a keyword
  count (3 of 3 at Sonnet). That is consistent with the small S gain, but the
  cause (the prompt, the length of the packet, Haiku's compliance) was not
  investigated.

## Limits

- One scenario, 3 repeats per cell, one grader family. No claim about other
  scenarios follows. The corrected N fixture (age 27 s) is used here; the earlier
  baseline-only run used the 41 s fixture, so the two are not pooled.
- The pre-run probe again listed base-prompt section headings instead of `NONE`
  (same note as `2026-10-31-wording-ab.md`); responses contain no Korean text and
  the with-skill responses do not mention the skill (checked over all 12).
- The label check as pre-stated cannot see Q1 and Q5, which is the only place the
  lift occurs; it was not changed after the result.

## Conclusion

On scenario N the skill raises both structure (S) and, at Sonnet, Q1/Q5, and
the Sonnet baseline's Q1/Q5 deficit (calling the TTL "disproven" from a small
sample) is gone with the skill. By the rule as written that lift is attributed
to labels; the data neither confirm nor rule out that it also reflects a content
change, because the stripped check excludes Q1 and Q5. At Haiku nothing moves
beyond a small S gain. This is consistent with the earlier v2 finding (structure
large, substance small) rather than a reversal of it. A next step that would
separate the readings is a reader-checked classification of the Sonnet N
responses for the sample caveat, or a second scenario with the same shape.
