# 2026-10-28 — Why Haiku's labels did not improve classification accuracy or calibration

Analysis of the rubric v2 re-grade (`2026-10-28-rubric-v2-regrade.md`). It reads the
grader's notes and the underlying responses; **it changes nothing in
`SKILL.md`** and the candidate wording at the end is untested.

## The puzzle

At Haiku 4.5 the skill raised the structure score (S +1.69) but not the
substance score (Q +0.58), and two substance items went *down* slightly:
Q1 classification accuracy (1.10 → 1.00) and Q5 calibration (1.23 → 1.13).
Responses with the evidence labels were not better classified or better
calibrated than responses without them.

## What the data show

- Responses losing at least one point on Q1 or Q5 (two-pass average below 2):
  **{cnt['skill'][0]} of {cnt['skill'][1]} with-skill Haiku responses** versus
  **{cnt['baseline'][0]} of {cnt['baseline'][1]} baseline Haiku responses**.
- The failure modes are **the same in both conditions at similar frequency.**
  Counts below are the preparer's manual reading of the grader's notes
  (not an automated classification; the notes themselves are model output):

| Failure mode | With-skill (15) | Baseline (15) |
|---|---|---|
| A result the response did not produce is shown as an outcome (before/after tables, "running the test … passes", fabricated output) | 5 (F, G ×2, J, L) | 5 (A, F, G ×2, L) |
| An inference or assumption is stated as fact | 5 (B, C, D, I, J) | 6 (B, C, D, J, K, M) |
| A strong flat claim ("actual root cause", "FIXED", "the actual fix") | — | 3 (C, G, J) |
| A `VERIFIED` / "Verified" label on something not demonstrated | 5 (A, F, G ×2, M) | not applicable (no labels) |
| User-stated limits of the material not acknowledged (excerpts only; prompt asked for limits) | 2 (A ×2) | 0 |

So the skill does not remove the overclaims. It puts a label on them: in five
with-skill responses a `VERIFIED` (or "Verified") label sits on a claim that the
baseline version states flatly, and the label lends it authority.

## Confirmed in the raw responses

- `F-skill-haiku-r1`: lists the fix as `Conclusion: VERIFIED` and shows
  before/after cases ending in ✓ although nothing was run.
- `J-skill-haiku-r1`: puts "the logic is inverted" under FACTS although it is
  read from a code comment, and calls the one-line patch a fix that "resolves
  the failed assertion" without running it.
- `M-skill-haiku-r1`: a claims table marks the user's report "Verified but
  cause unknown" with "no measurement".
- `G-skill-haiku-r1` and `-r2`: "Running the fixed function … both assertions
  pass" although the prompt said not to assume tests were run.

## Why the instruction may not prevent it

`SKILL.md` defines the labels as: FACT — "directly observed or verified";
VERIFIED — "directly demonstrated"; and warns that "a fix that compiles or a
plausible-looking cause is not, by itself, grounds for VERIFIED." It does not
say that **reading or tracing code is not running it**, that a **before/after
result must not be shown unless it was observed**, or what to do when the user
**limits the material** (excerpts only). A small model that follows the label
format literally can therefore place a code-reading conclusion under FACTS and
mark a fix VERIFIED. This is a hypothesis about the cause; it has not been
tested.

## Candidate wording (not applied)

For `SKILL.md`, under *Establish What Is Known* and *Classify the Conclusion*:

- FACTS holds only what was supplied to you or what you observed. What you
  conclude by reading or tracing code goes under INFERENCES, however certain it
  feels.
- VERIFIED means a test, reproduction or output was actually run or supplied
  and shows it. Reading code is INFERRED. Never show a before/after result you
  did not run; say it was not run.
- If the user limits the material (excerpts, a partial log), list what you
  could not see under UNKNOWNS; do not write "None".

## How to test it

This needs the CONTRIBUTING evaluation bar and the maintainer's consent:
generate the affected scenarios (A, F, G, J, L, M) at Haiku with the current
wording and with the candidate wording, grade with rubric v2 (Q1 and Q5 first,
then the legacy total and stripped check), in the clean environment. Success
would be Q1 and Q5 rising without S falling; a longer or more rigid skill text
is a cost to watch. With single samples per cell, use 2–3 repeats.

## Limitations

Haiku only; single samples; counts are a manual reading of model-written
notes; the raw responses were spot-checked (four) rather than all read; and a
Sonnet-tier baseline is already near ceiling on Q1/Q5, so Sonnet cannot show
whether such wording helps.
