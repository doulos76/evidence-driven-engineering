# TODO

Follow-up work, updated after the Haiku label analysis and the clean-run
pass/fail (`tests/results/2026-10-28-haiku-label-analysis.md`,
`tests/results/2026-10-28-clean-run-pass-fail.md`). Not committed to a
timeline — pick up when there's a reason to.

Done: environment-confound rerun, rubric v2 (structure and substance scored
separately), the label-stripped sensitivity check, a first human spot-check
(one reader, four pairs), response storage and per-item grading sheets,
pass/fail on the clean run (60/60 PASS, non-discriminating), and the Haiku
label analysis. Decided against, so they remain limitations: a second grader
family and a second human reader.

Current finding: the measured benefit of EDE is evidence structure and
confidence labeling (S lift about +1.7); the substance lift is about +0.5
(below the +1.0 rule). At Haiku the same overclaims occur with and without the
skill; with the skill they gain a `VERIFIED` label.

## 1. Candidate `SKILL.md` wording at Haiku — tested, not supported

Done 2026-10-31 (`2026-10-31-wording-ab.md`): A, F, G, J, L and M at Haiku, 3
repeats, current vs candidate wording, rubric v2 in the clean environment. By
the rule fixed beforehand there is no improvement (Q1+Q5 −0.33, Q −0.92, 0 of 6
scenarios positive; scenario L is most of the Q drop and varies a lot at n=3).
The wording is not applied. Open: whether a different lever (separating
read-from-code facts structurally, or an explicit check step) helps, and the
probe in that run did not return `NONE` as before (cause not investigated).

## 2. A scenario set with headroom

At Sonnet the baseline scores 19.15 of 20 on substance and every item except
Q1 and Q5 is at 1.97–2.00, so there is no room to show a content benefit.
Started 2026-10-31: scenarios N–Q (stacked authority, partially supported,
long noisy context, plausible but wrong cause) were added and their Sonnet
baseline run (`2026-10-31-headroom-baseline.md`). Only N leaves room (Q 16.0
and 18.0; Q1 and Q5 lost to calling the TTL "disproven" from four sampled
reports); O, P and Q sit at 19.5–20. N's fixture had a flaw (corrected, not
rerun) and there is no with-skill arm yet. N with and without the skill was
then run at Sonnet and Haiku, 3 repeats (`2026-10-31-n-skill-vs-baseline.md`):
at Sonnet S +2.67 and Q +2.33 (all on Q1 and Q5; label-stripped Q8 +0.00, so the
pre-stated rule attributes it to labels, though that check cannot see Q1 and
Q5); at Haiku Q +0.33 and the labels appeared in 1 of 3 responses. Still open:
a reader-checked look at whether the Sonnet Q1/Q5 gain is the sample caveat
itself, a second scenario of the same shape, a third tier (Claude Opus), and
2–3 repeats everywhere: only scenarios A
and G ran n=2, and Haiku per-scenario Q lifts range from −2.0 to +5.5 on
single samples. Scenario G now fails on "reports an unrun test as passing"
(`tests/scenarios.md`); the criterion applies from the next run, and earlier
pass/fail results were not re-judged.

## 3. What the README should promise

The README states that EDE makes the evidence structure and confidence visible
and does not claim better diagnoses. Revisit after items 1 and 2.
