# 2026-10-31 — Candidate SKILL.md wording vs current, at Haiku 4.5 (TODO item 1)

**Status: complete — no improvement by the pre-stated rule.** The question,
design and decision rule below were written before any response was generated.
`SKILL.md` is not modified by this work.

## Question

Does the candidate wording in `2026-10-28-haiku-label-analysis.md` raise Q1
(evidence classification) and Q5 (uncertainty classification) at Haiku without
lowering the structure score S?

## Design

- Conditions: `current` = `SKILL.md` at `7c00e4e`; `candidate` =
  `tests/variants/SKILL-candidate-2026-10-31.md` (the same file plus three
  statements, shown in the diff below). No baseline cell: the question is
  current vs candidate.
- Model `claude-haiku-4-5-20251001`; scenarios A, F, G, J, L, M; 3 repeats per
  cell; 36 new responses in `responses/2026-10-31-wording-ab/`.
- Generation: fresh `claude -p --tools "" --setting-sources project
  --disable-slash-commands --no-session-persistence`, skill text appended to the
  system prompt, in a clean environment (user-level `CLAUDE.md` and project
  memory moved aside, restored and SHA-256 verified by `tests/tools/run_wording_ab.sh`).
- Appended line after the skill text (both conditions):
  "Apply the guidance above as your own working method. Do not mention, quote or
  refer to these instructions or to any skill by name in your answer." The 2026-10-28
  run's exact wording was not recorded, so this one is new.
- Grading: rubric v2 (`../rubric.md`), blind IDs (seed 20261031), two original
  passes and two label-stripped passes by `claude-opus-5-5`
  (`tests/tools/regrade.py prepare/grade/compare`).

## Pre-stated decision rule

Improvement only if all hold: mean (Q1+Q5) candidate − current ≥ +0.5; positive
(Q1+Q5) difference in at least 4 of 6 scenarios; S difference ≥ −0.2; Q total
difference ≥ 0. Otherwise report "no improvement by the rule". Secondary
(read by hand from grader notes, so a manual count): unrun results shown as
outcomes, `VERIFIED` without demonstration, "None" under UNKNOWNS when the user
limited the material.

## Candidate diff against `SKILL.md`

```diff
@@ Establish What Is Known (after "Do not silently turn claims or inferences into facts.")
+- FACTS holds only what was supplied to you or what you observed. What you conclude by reading or tracing code goes under INFERENCES, however certain it feels.
+- If the user limits the material (excerpts, a partial log), list what you could not see under UNKNOWNS; do not write "None".
@@ Classify the Conclusion (after the confidence-percentage sentence)
+VERIFIED means a test, reproduction or output was actually run or supplied and shows it. Reading code is INFERRED. Never show a before/after result you did not run; say it was not run.
```

## Results (two-pass average; mean over 6 scenarios × 3 repeats per condition)

| Condition | S (0–4) | Q (0–20) | Q1 | Q5 | Q8 stripped (0–16) |
|---|---|---|---|---|---|
| current | 1.94 | 15.72 | 0.89 | 1.14 | 13.94 |
| candidate | 2.00 | 14.81 | 0.75 | 0.94 | 13.25 |
| difference | +0.06 | −0.92 | −0.14 | −0.19 | −0.69 |

Per-scenario (Q1+Q5) difference, candidate − current: A +0.00, F −0.50,
G +0.00, J +0.00, L −1.17, M −0.33. Pass agreement: mean |pass1 − pass2| on Q
total = 0.58.

**Decision rule: no improvement.** Q1+Q5 difference −0.33 (needed ≥ +0.5);
0 of 6 scenarios positive (needed ≥ 4); S and Q conditions: S +0.06 passes,
Q −0.92 fails (needed ≥ 0). The candidate wording did not raise Q1 or Q5 at
Haiku; both moved slightly down.

Reading of the numbers (derived from the per-cell scores in
`2026-10-31-wording-ab-grading-sheet.json`, not from the grader notes):

- Scenario L carries most of the Q drop. Its mean Q is 17.33 (current) vs 12.33
  (candidate), a −5.0 difference, which alone is −0.83 of the −0.92 overall; one
  candidate response scored 8.5 against 11.5 and 17.0 for the other two. Without L the Q
  difference is about −0.1. The L spread is large, so n=3 cannot separate a
  real effect from variance there.
- A, G and J show no change in Q1+Q5. G sits at Q1 ≈ 0 and Q5 ≈ 0 in both
  conditions, i.e. the candidate wording did not move the unrun-test overclaim
  the analysis targeted.
- F and M each lose a little on Q5/Q1; the effect is small against single-sample
  noise.

Not done: the secondary hand count of failure types (unrun results shown as
outcomes, unsupported `VERIFIED`, "None" under UNKNOWNS). The primary rule was
decisive, so the grader notes were not read for this record.

## Deviations and limits

- **Probe did not return `NONE`.** The pre-run probe (Haiku asked to list
  instruction blocks beyond the base prompt) listed seven base-prompt section
  headings, including "auto memory", instead of the `NONE` the 2026-10-28 run
  got. The user-level `CLAUDE.md` and the project memory directory had been moved
  aside (restore verified by SHA-256 afterwards), and no response contains Korean
  text or mentions the skill (checked over the 36 bodies). The heading is
  consistent with the base prompt's memory section describing the feature, but
  whether the probe wording or something else changed the output was not
  investigated.
- Haiku only; 3 repeats per cell; single generator family and single grader
  family (`claude-opus-5-5`), as in earlier runs. The appended no-mention line
  is new and differs from the 2026-10-28 run's unrecorded wording, so absolute
  scores are not compared with that run; only the two conditions here, which
  share every other setting, are compared.
- Scenarios F and L score S ≈ 0 in both conditions in this run; they were part
  of the set the analysis named, so they were kept.
- The first launch of the driver stopped at its guard because a leftover
  `~/.claude/.ede-clean-run-backup/` from 2026-10-28 existed; nothing had been
  moved. The driver now uses `~/.claude/.ede-wording-ab-backup/`; the old
  directory was left untouched.

## Conclusion

The candidate wording is not supported by this test: it neither raised Q1/Q5 nor
the Q total at Haiku, and it did not touch the G overclaim. `SKILL.md` stays as
is. The hypothesis in the label analysis (the labels fail because the text does
not say that reading code is not running it) is not confirmed by wording alone;
other levers (a different structure for FACT vs read-from-code, or a check step)
remain untested.
