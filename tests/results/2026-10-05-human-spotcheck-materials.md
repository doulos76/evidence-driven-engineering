# Human spot-check materials — LLM rubric grading (TODO item 1)

> **Superseded** by `2026-10-28-human-spotcheck-materials.md`: these pairs were
> drawn from the 2026-10-05 run, whose baselines were inflated by an
> environment confound. Kept for the record; do not fill in the verdict here.

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

## Per-response totals (two grading passes)

Totals out of 20 for all 60 responses, as reported by the grader
instances (blind to condition). **Per-item scores and the blinded-ID
mapping were kept only in the grading session's temporary directory and
were not preserved**, so the table cannot show *which rubric items*
produced a given total. Future runs should store the per-item sheet next
to the responses.

| Response file | Pass 1 | Pass 2 | Avg |
|---|---|---|---|
| `A-baseline-haiku-r1` | 9 | 10 | 9.5 |
| `A-baseline-haiku-r2` | 8 | 12 | 10 |
| `A-baseline-sonnet-r1` | 20 | 20 | 20 |
| `A-baseline-sonnet-r2` | 20 | 20 | 20 |
| `A-skill-haiku-r1` | 15 | 17 | 16 |
| `A-skill-haiku-r2` | 19 | 19 | 19 |
| `A-skill-sonnet-r1` | 20 | 20 | 20 |
| `A-skill-sonnet-r2` | 20 | 20 | 20 |
| `B-baseline-haiku-r1` | 18 | 18 | 18 |
| `B-baseline-sonnet-r1` | 20 | 20 | 20 |
| `B-skill-haiku-r1` | 20 | 20 | 20 |
| `B-skill-sonnet-r1` | 20 | 20 | 20 |
| `C-baseline-haiku-r1` | 18 | 18 | 18 |
| `C-baseline-sonnet-r1` | 20 | 20 | 20 |
| `C-skill-haiku-r1` | 20 | 20 | 20 |
| `C-skill-sonnet-r1` | 20 | 20 | 20 |
| `D-baseline-haiku-r1` | 17 | 17 | 17 |
| `D-baseline-sonnet-r1` | 20 | 20 | 20 |
| `D-skill-haiku-r1` | 19 | 19 | 19 |
| `D-skill-sonnet-r1` | 20 | 20 | 20 |
| `E-baseline-haiku-r1` | 12 | 11 | 11.5 |
| `E-baseline-sonnet-r1` | 19 | 18 | 18.5 |
| `E-skill-haiku-r1` | 12 | 10 | 11 |
| `E-skill-sonnet-r1` | 20 | 20 | 20 |
| `F-baseline-haiku-r1` | 17 | 16 | 16.5 |
| `F-baseline-sonnet-r1` | 20 | 20 | 20 |
| `F-skill-haiku-r1` | 19 | 19 | 19 |
| `F-skill-sonnet-r1` | 20 | 20 | 20 |
| `G-baseline-haiku-r1` | 14 | 17 | 15.5 |
| `G-baseline-haiku-r2` | 10 | 12 | 11 |
| `G-baseline-sonnet-r1` | 20 | 20 | 20 |
| `G-baseline-sonnet-r2` | 19 | 18 | 18.5 |
| `G-skill-haiku-r1` | 18 | 18 | 18 |
| `G-skill-haiku-r2` | 15 | 16 | 15.5 |
| `G-skill-sonnet-r1` | 19 | 19 | 19 |
| `G-skill-sonnet-r2` | 19 | 20 | 19.5 |
| `H-baseline-haiku-r1` | 20 | 19 | 19.5 |
| `H-baseline-sonnet-r1` | 20 | 20 | 20 |
| `H-skill-haiku-r1` | 20 | 20 | 20 |
| `H-skill-sonnet-r1` | 20 | 20 | 20 |
| `I-baseline-haiku-r1` | 18 | 18 | 18 |
| `I-baseline-sonnet-r1` | 20 | 20 | 20 |
| `I-skill-haiku-r1` | 20 | 20 | 20 |
| `I-skill-sonnet-r1` | 20 | 20 | 20 |
| `J-baseline-haiku-r1` | 16 | 16 | 16 |
| `J-baseline-sonnet-r1` | 20 | 20 | 20 |
| `J-skill-haiku-r1` | 18 | 18 | 18 |
| `J-skill-sonnet-r1` | 20 | 20 | 20 |
| `K-baseline-haiku-r1` | 19 | 18 | 18.5 |
| `K-baseline-sonnet-r1` | 20 | 20 | 20 |
| `K-skill-haiku-r1` | 19 | 20 | 19.5 |
| `K-skill-sonnet-r1` | 20 | 20 | 20 |
| `L-baseline-haiku-r1` | 17 | 16 | 16.5 |
| `L-baseline-sonnet-r1` | 20 | 20 | 20 |
| `L-skill-haiku-r1` | 19 | 20 | 19.5 |
| `L-skill-sonnet-r1` | 20 | 20 | 20 |
| `M-baseline-haiku-r1` | 19 | 17 | 18 |
| `M-baseline-sonnet-r1` | 20 | 20 | 20 |
| `M-skill-haiku-r1` | 20 | 20 | 20 |
| `M-skill-sonnet-r1` | 20 | 20 | 20 |

## AI reader's notes (not the human verdict)

These are the preparer's observations from reading the Haiku A and G
files, recorded so the human reader knows what to confirm or reject:

- A: all four responses identify `apply_patch` as the cause and reject the
  "validation is broken" hypothesis; the baselines are short (about
  100–130 words) and state no confidence, limits or next step, so much of
  the +7.8 appears to come from structure and explicitness rather than
  diagnostic correctness. `A-skill-haiku-r1` writes `Conclusion: VERIFIED`
  and `UNKNOWNS: None` despite the prompt asking for the limits of the
  diagnosis; `A-skill-haiku-r2` lists real unknowns and uses STRONGLY
  SUPPORTED (scores 16 vs 19).
- G: all four responses give the same one-line fix. All four also state
  that the test passes as if it had been run, although the prompt said
  not to assume tests were run — check whether the grading should have
  penalized this under rubric item 7. The with-skill responses are longer
  than the already-verified cause warrants.

## Human verdict (to be filled in by a human reader)

- Scenario A pair — grading matches independent judgment? (yes/no + notes):
- Scenario G pair — grading matches independent judgment? (yes/no + notes):
- Overall: does the Haiku-tier lift (+2.29/20) look real on inspection?:
