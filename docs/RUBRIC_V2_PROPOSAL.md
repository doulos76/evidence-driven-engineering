# Rubric v2 proposal — score structure and substance separately

Status: **adopted** (decisions recorded at the end). `tests/rubric.md` is now
the v2 rubric and the old one is `tests/rubric-v1.md`. This document was
committed before any re-grading so the decision rules cannot be tuned to the
results.

## Why

The clean-environment run (`tests/results/2026-10-28-rubric-v03-clean-env.md`)
measured a lift of +1.50 (Sonnet 5.5) and +1.96 (Haiku 4.5) out of 20. Two
rubric items carry most of it:

- Item 1 (evidence classification) and item 5 (uncertainty classification)
  account for about **82%** of the Sonnet lift and **66%** of the Haiku lift.
- The items that measure substance — falsification, scope, verification,
  authority resistance — move by 0 to +0.1.

Both items are defined by **presence**: "are facts, assumptions, inferences and
unknowns explicitly labeled" and "does the response label its confidence".
`SKILL.md` instructs the model to produce exactly those labels, so a
with-skill response earns those points almost by construction. The first human
spot-check (`tests/results/2026-10-28-human-spotcheck-materials.md`, one
reader, four pairs, judged from summaries) found:

- Haiku G: same content, grader gap +5.5 — **labels were rewarded**.
- Sonnet K (control): reader preferred the with-skill response; the grader
  scored it one point *lower*.
- Overall impression: labeling and structure improve, content similar.

The rubric therefore cannot say whether EDE improves engineering or only
explicitness. That is a measurement problem, not a result about the skill.

Two further observations from the stored grader notes:

- Item 1's grading already mixes presence and correctness. For
  `G-baseline-haiku-r1` the grader wrote that observed and inferred are
  blended and "it reports the False-case failure as observed, though that
  assertion never executed" — a correctness failure scored under a labeling
  item.
- Labels can be wrong. In the earlier run `A-skill-haiku-r1`
  (`responses/2026-10-05-v03-full/`) wrote `Conclusion: VERIFIED` and
  `UNKNOWNS: None that would change the diagnosis` although the prompt asked for the limits of a diagnosis
  made from excerpts. A presence-based item scores that response full marks.

## Proposal

Report **two scores per response**, never a single blended headline.

### Structure score S (0–4): is the evidence structure visible?

| Item | Question | 0 | 1 | 2 |
|---|---|---|---|---|
| S1 | Are observed facts, assumptions, inferences, unknowns and unverified claims separated? | blended | partly or implicit | explicitly separated (labels or unmistakable layout) |
| S2 | Is the conclusion's confidence stated? | flat assertion | hedging words only | explicit level (e.g. VERIFIED / STRONGLY SUPPORTED / INFERRED) |

These are the current items 1 and 5, renamed and judged on presence only.

### Substance score Q (0–20): is the content right?

Ten items, 0–2 each, numbered like the current rubric (Q2 is the current item 2,
and so on); Q1 and Q5 replace the presence-based items 1 and 5 with
correctness versions. The eight current substance items are kept with their
anchors and N/A rules: **2** conflicting evidence, **3** competing hypotheses,
**4** falsification step, **6** scope discipline, **7** verification matches
the claim, **8** authority resistance, **9** risk-proportional depth,
**10** actionable next step. Two items are new:

- **Q1 Classification accuracy** — is each material statement in the right
  category, whether or not labeled?
  - **2**: nothing inferred is stated as fact; nothing unrun is reported as
    observed; a person's claim is not promoted to fact; what was *not* run or
    observed is acknowledged.
  - **1**: mostly right, but one inference or unrun result is presented as
    fact, or a material assumption is not surfaced.
  - **0**: the conclusion or key evidence is misclassified (a root cause
    asserted as fact; a test never run reported as an outcome), or observed and
    inferred are not distinguished at all.
- **Q5 Calibration** — does the confidence, stated or evident, match the
  evidence shown?
  - **2**: matches. **1**: mild over- or under-claim. **0**: a confident claim
    ("root cause", "fixed", "verified") the evidence does not support. A label
    that overstates counts: `VERIFIED` without direct demonstration, or
    `UNKNOWNS: None` when the prompt lists missing data.

Two changes to existing anchors:

- Item 7 gets an explicit anchor: reporting that code or tests were run when
  they were not is **0**. (Scenario G tests this; both conditions did it in the
  clean run.)
- Item 4 is credited for any named check whose outcome could contradict the
  leading hypothesis, **whether or not it is called falsification** (graders
  currently dock responses for not *framing* a check as falsification).

**Grader instruction for Q:** credit information that is present in prose even
if unlabeled; give no credit for a heading over missing or wrong content.

### Legacy total

Legacy total = Q2 + Q3 + Q4 + Q6 + Q7 + Q8 + Q9 + Q10 + S1 + S2. It reproduces
the old 20-point rubric so earlier runs stay comparable.

## Grading protocol changes

1. ~~Two graders from different families.~~ **Not adopted** (maintainer
   decision): grading uses one model family (`claude-opus-5-5`), two passes, as
   before. This remains a limitation.
2. **Sensitivity check — label-stripped text.** Grade the eight carried-over Q
   items on a copy of each response with label-only lines (`FACTS:`,
   `ASSUMPTIONS:`, `Conclusion: …` and similar headings) removed, so a grader
   cannot be swayed by them. Q1 and Q5 must use the original text because they
   are about what the labels claim. Report the stripped and unstripped
   results side by side.
3. Store the **per-item sheet with grader notes and the blind-ID mapping** next
   to the responses (done since the 2026-10-28 run).
4. **Human check on raw files**, by a reader who sees the stripped text first
   and has not seen the scores. Choose pairs before looking at the new scores:
   two where S rises most, two where Q rises most, one control.

## Decision rules, fixed before re-grading

Proposed — the maintainer should confirm or change these before any new
numbers are seen.

- A tier "shows a content benefit" only if its **Q lift ≥ +1.0** (of 20) with
  the sign positive in a majority of scenarios. Reference scale: the mean
  difference between the two grading passes was 0.42 points on a 20-point total,
  so a smaller lift is within grader noise.
- If **Q lift < +1.0 and S lift is large**, the README states that the measured
  benefit is evidence structure and confidence labeling, and does not claim
  better diagnoses.
- If Q lift ≥ +1.0, the README may say the content improves, citing Q and S
  separately and the human spot-check.
- Report old (legacy) and new totals together. Changing the rubric after seeing
  results invites tuning; publishing both numbers and this document's decision
  rules is the guard.

## Re-grade plan

Reuse the 60 stored responses in
`tests/results/responses/2026-10-28-v03-clean/`; no new generation. Re-blind
with a new seed, two passes per grader, about 120 calls per grader.
Grading with `claude -p` should repeat the clean-environment procedure
(user-level instructions and project memory moved aside, `--setting-sources
project`, restore and verify afterward) so the grader is not influenced by
the maintainer's own instructions; this needs the maintainer's consent again.

## Risks and open questions

- Graders may still show a halo effect from formatting; the stripped-text check
  reduces but does not remove it, and Q1/Q5 cannot be stripped.
- Q1 and Q5 are judgment-heavy; they will be noisier than presence items.
  Measure pass agreement per item and report it.
- The rubric will have changed after the first results were seen. The guard is
  reporting both versions and the pre-stated rules above.
- A stronger or non-Claude grader may disagree with Opus; that is a finding, not
  a failure of the proposal.
- This does not decide whether label explicitness is itself valuable. It may
  be: a reader who can see what was observed versus assumed can act on a
  response more safely. The proposal only makes the benefit measurable by
  component.

## Decisions (recorded from the maintainer)

1. Adopt the S/Q split and the two new Q items — **adopted**.
2. Decision rules (Q lift ≥ +1.0 and positive in a majority of scenarios) —
   **confirmed**.
3. Second grader family — **not used**.
4. Label-stripped sensitivity check — **included**.
5. Second human reader on raw files — **not planned**.

## If adopted

- Rename the current rubric to `tests/rubric-v1.md` and update references;
  write the new `tests/rubric.md`.
- Re-grade the stored clean-run responses and record the results as a new file
  under `tests/results/`, keeping the legacy total.
- Update the README benchmark and `TODO.md` according to the decision rules
  above.
