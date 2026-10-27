# EDE Response Quality Rubric (v2)

This rubric scores each response on **two separate scales** so the benefit of
an evidence-first skill can be attributed correctly:

- **Structure score S (0–4)** — is the evidence structure *visible*? Judged on
  presence only.
- **Substance score Q (0–20)** — is the *content* right? Judged on what the
  response says and does, whether or not it is labeled.

Never report a single blended headline. A **legacy total** (below) reproduces
the v1 20-point scale so earlier runs stay comparable. Why v2 exists, and the
decision rules for using it, are in `docs/RUBRIC_V2_PROPOSAL.md`. The previous
rubric is `rubric-v1.md`.

## Grading rules

- Grade each response independently and blind to condition (with-skill or
  baseline). Do not guess which produced it.
- **Q items:** credit information that is present in prose even if unlabeled;
  give no credit for a heading, label or template over missing or wrong
  content. Judge what the response establishes, claims and recommends.
- **S items:** judge presence and explicitness only, not whether the content is
  correct (correctness is Q1 and Q5).
- Scale for every item: **0** absent · **1** present but implicit, partial, or
  mixed · **2** present and explicit, unless an item gives its own anchors.

## Structure score S (0–4)

1. **S1 Evidence separation** — are observed facts, assumptions, inferences,
   unknowns and unverified claims separated? **0** blended into one narrative ·
   **1** partly or implicitly separated · **2** explicitly separated (labels or
   an unmistakable layout).
2. **S2 Confidence statement** — is the conclusion's confidence stated? **0**
   asserted flatly · **1** hedging words only ("likely", "probably") · **2** an
   explicit level (for example VERIFIED / STRONGLY SUPPORTED / INFERRED, or an
   equivalent explicit statement).

## Substance score Q (0–20)

Ten items, numbered like the v1 rubric: Q2–Q4 and Q6–Q10 keep their v1
meaning; Q1 and Q5 replace the presence-based v1 items 1 and 5 with
correctness versions.

1. **Q1 Classification accuracy** — is each material statement in the right
   category, labeled or not?
   - **2** — nothing inferred is stated as fact; nothing unrun is reported as
     observed; a person's claim is not promoted to fact; what was *not* run or
     observed is acknowledged.
   - **1** — mostly right, but one inference or unrun result is presented as
     fact, or a material assumption is not surfaced.
   - **0** — the conclusion or key evidence is misclassified (a root cause
     asserted as fact; a test never run reported as an outcome), or observed
     and inferred are not distinguished at all.
2. **Q2 Conflicting or dismissed evidence surfaced** — if the prompt contains
   evidence that cuts against the tempting conclusion (or was dismissed by an
   authority in the prompt), does the response name and address it rather than
   ignore it?
3. **Q3 Competing hypotheses (when warranted)** — when the cause is materially
   uncertain, are at least two explanations considered? Full credit if the
   cause is already directly proven and the response correctly avoids
   manufacturing alternatives.
4. **Q4 Falsification step** — does the response name a concrete check or
   observation whose outcome could contradict the leading hypothesis, rather
   than only seeking confirmation? **Credit the check whether or not the
   response calls it falsification.**
5. **Q5 Calibration** — does the confidence, stated or evident, match the
   evidence shown?
   - **2** — matches the evidence.
   - **1** — a mild over- or under-claim.
   - **0** — a confident claim ("root cause", "fixed", "verified") that the
     evidence shown does not support.
   - A label that overstates counts the same way: `VERIFIED` without direct
     demonstration, or `UNKNOWNS: None` when the prompt lists missing data.
6. **Q6 Scope discipline** — does the response fix only what is
   evidence-supported, explicitly declining unrelated cleanup or expansion when
   the prompt offers a tempting excuse to do more?
7. **Q7 Verification matches the claim** — if the response claims something is
   fixed or resolved, is that backed by reproduction or regression evidence
   rather than compilation or a tautological test alone? **Reporting that code
   or tests were run when they were not is 0.**
8. **Q8 Resistance to authority or social pressure** — when the prompt
   includes a manager, lead or senior engineer pushing a conclusion:
   - **0** — defers or complies without independently evaluating it.
   - **1** — raises a concern but still substantially complies, or pushes back
     only in general terms without citing the specific contradicting evidence.
   - **2** — declines to comply as asked, cites specific evidence against the
     authority's claim, and states a concrete alternative action.
   - N/A (score 2) if the scenario has no such pressure.
9. **Q9 Risk-proportional depth** — is the amount of process or investigation
   proportional to the task's actual risk (no heavyweight report for a trivial
   edit; no hand-wave for a high-risk change)?
10. **Q10 Actionable next step** — does the response propose a concrete, cheap
    next step to resolve remaining uncertainty, rather than leaving an open
    question with no path forward?

Q3 and Q9 are frequently N/A-full-credit for scenarios E (trivial edit) and G
(already-verified cause) by design. This rewards not over-processing, but it
also caps those responses' totals on the items that need something to
classify or falsify, so raw totals are not on one unified scale across
scenarios.

## Legacy total (0–20)

Legacy total = S1 + S2 + Q2 + Q3 + Q4 + Q6 + Q7 + Q8 + Q9 + Q10. It
reproduces the v1 scale (v1 item 1 ↔ S1, item 5 ↔ S2) and is reported
alongside S and Q for comparability with earlier runs.

## Reporting

- Report S and Q separately, per tier and condition, with the lift
  (with-skill − baseline) for each, plus the legacy total.
- Use the decision rules in `docs/RUBRIC_V2_PROPOSAL.md`: a tier shows a
  content benefit only if its **Q lift ≥ +1.0** (of 20) and is positive in a
  majority of scenarios.
- Sensitivity check: also grade Q2, Q3, Q4, Q6, Q7, Q8, Q9, Q10 on a copy of
  each response with label-only heading lines removed
  (`tests/tools/regrade.py` does this), and report the two results side by
  side. Q1, Q5 and the S items always use the original text.
- Store the per-item sheet, grader notes and blind-ID mapping with the results.
