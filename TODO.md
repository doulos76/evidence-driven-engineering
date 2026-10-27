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

## 1. Test the candidate `SKILL.md` wording at Haiku

`2026-10-28-haiku-label-analysis.md` proposes wording that ties FACTS and
VERIFIED to what was actually observed or supplied, forbids showing results
that were not run, and asks for UNKNOWNS when the user limits the material. It
is untested and not applied. To test: generate A, F, G, J, L and M at Haiku
with current and candidate wording (2–3 repeats), grade with rubric v2 in the
clean environment (needs the maintainer's consent to move the user-level
instructions), and look for Q1 and Q5 rising without S falling. Applying the
wording to `SKILL.md` needs the CONTRIBUTING evaluation bar.

## 2. A scenario set with headroom

At Sonnet the baseline scores 19.15 of 20 on substance and every item except
Q1 and Q5 is at 1.97–2.00, so there is no room to show a content benefit.
Add adversarial variants (stacked authority pressure, partially supported
cases, longer noisy context, tasks where a plausible cause is wrong), consider
a third tier (Claude Opus), and run 2–3 repeats everywhere: only scenarios A
and G ran n=2, and Haiku per-scenario Q lifts range from −2.0 to +5.5 on
single samples. Also consider pass/fail criteria that cover "reports an unrun
test as passing" (scenario G currently cannot fail on it).

## 3. What the README should promise

The README states that EDE makes the evidence structure and confidence visible
and does not claim better diagnoses. Revisit after items 1 and 2.
