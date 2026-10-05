# Human spot-check materials — LLM rubric grading (TODO item 1)

Prepared 2026-10-05, from the v0.3-cycle full run
(`2026-10-05-rubric-v03-full-verbatim.md`). **The human judgment itself
has not been performed yet** — this file selects the material and states
what to check; record the verdict in the section at the bottom.

## Why these pairs

TODO item 1 asks a human to read the largest-delta response pairs side
by side and check whether the LLM grader's point allocation reflects
real quality differences, or rewards surface patterns (presence of
`FACTS:`/`ASSUMPTIONS:` headers) over substance. The largest deltas in
the current run are at the Haiku tier:

| Pair | with-skill (2-pass avg) | baseline (2-pass avg) | Delta |
|---|---|---|---|
| Scenario A, Haiku | `A-skill-haiku-r1` 16.0 / `A-skill-haiku-r2` 19.0 | `A-baseline-haiku-r1` 9.5 / `A-baseline-haiku-r2` 10.0 | **+7.8** |
| Scenario G, Haiku | `G-skill-haiku-r1` 18.0 / `G-skill-haiku-r2` 15.5 | `G-baseline-haiku-r1` 15.5 / `G-baseline-haiku-r2` 11.0 | **+3.5** |

All files are under `responses/2026-10-05-v03-full/`. The scenario
prompts are in `../prompts.md` (Scenario A — Stack Trace Anchoring;
Scenario G — Verified Cause).

## What to check (from TODO item 1)

1. Read each pair side by side, **ignoring the evidence-block headers**
   on a second pass: is the with-skill response actually more rigorous
   (correct cause, falsification attempt, honest limits), or does it
   mainly differ in formatting?
2. Items 1 (evidence classification) and 5 (uncertainty classification)
   are the items most likely to reward formatting over content — check
   whether the baseline responses genuinely lack the *substance* of
   those items or only the labels.
3. Scenario G is a verified-cause scenario: check whether the grader
   correctly rewarded *not* manufacturing fake alternatives (rubric
   item 3) rather than rewarding length.
4. Note: the scores above were produced by a single stronger-tier
   grader model in two independent passes; per-pass scores are in
   `2026-10-05-rubric-v03-full-verbatim.md`.

## Human verdict (to be filled in by a human reader)

- Scenario A pair — grading matches independent judgment? (yes/no + notes):
- Scenario G pair — grading matches independent judgment? (yes/no + notes):
- Overall: does the Haiku-tier lift (+2.29/20) look real on inspection?:
