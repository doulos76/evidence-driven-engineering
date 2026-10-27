# TODO

Follow-up work, updated after the rubric v2 re-grade
(`tests/results/2026-10-28-rubric-v2-regrade.md`). Not committed to a timeline —
pick up when there's a reason to.

Done: environment-confound rerun, rubric v2 (structure and substance scored
separately), the label-stripped sensitivity check, a first human spot-check
(one reader, four pairs), response storage and per-item grading sheets.
Decided against, so they remain limitations: a second grader family and a
second human reader.

Current finding: the measured benefit of EDE is evidence structure and
confidence labeling (S lift about +1.7); the substance lift is about +0.5
(below the +1.0 rule), and at Haiku classification accuracy and calibration
are slightly lower with the skill.

## 1. Pass/fail on the clean run

The clean-run and v2 re-grade graded the rubric only. Judge the 30 with-skill
responses against `tests/scenarios.md` as well.

## 2. A scenario set with headroom

At Sonnet the baseline scores 19.15 of 20 on substance and every item except
Q1 and Q5 is at 1.97–2.00, so there is no room to show a content benefit.
Add adversarial variants (stacked authority pressure, partially supported
cases, longer noisy context, tasks where a plausible cause is wrong), consider
a third tier (Claude Opus), and run 2–3 repeats everywhere: only scenarios A
and G ran n=2, and Haiku per-scenario Q lifts range from −2.0 to +5.5 on
single samples.

## 3. Why Haiku's labels do not improve classification or calibration

Haiku's Q1 (classification accuracy) and Q5 (calibration) are 0.10 *lower*
with the skill. Read the with-skill responses where those items lose points
(for example a `VERIFIED` conclusion without direct demonstration, or
`UNKNOWNS: None` when information is missing). If the goal is substance, the
`SKILL.md` instruction may need to say what each label must be backed by; any
such change needs the CONTRIBUTING evaluation bar and a rerun with the v2
rubric.

## 4. What the README should promise

The README now states that EDE makes the evidence structure and confidence
visible and does not claim better diagnoses. Revisit after items 2 and 3.
