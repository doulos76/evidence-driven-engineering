# EDE Response Quality Rubric

Four independent runs (Sonnet 5 x3, Haiku 4.5 x1; 96 total scenario
executions across `tests/scenarios.md`) found every scenario passed under
both with-skill and baseline conditions — see `tests/results/`. Final
verdicts (pass/fail) are not discriminating at the model tiers tested so
far. What *did* differ consistently, on inspection, was the **structure**
of with-skill responses: explicit evidence labeling, named falsification
attempts, explicit uncertainty classification.

This rubric scores that structure directly, as a complement to pass/fail
scenario grading — not a replacement for it. Scenarios still gate on
"did the agent reach a defensible conclusion." This rubric asks "how
rigorously did it get there, and how legible is that rigor to a reader."

## Scoring

Each item is scored per response, 0-2:
- **0** — absent
- **1** — present but implicit or partial
- **2** — present and explicit

Max score: 20 (10 items x 2). Grade independently per response — a grader
should not know or guess which condition (with-skill/baseline) produced
a given response, to avoid biasing scores toward the expected result.

## Items

1. **Evidence classification** — Are facts, assumptions, inferences, and
   unknowns explicitly labeled (or unmistakably separated), rather than
   blended into one narrative?
2. **Conflicting/dismissed evidence surfaced** — If the prompt contains
   evidence that cuts against the tempting conclusion (or was dismissed
   by an authority figure in-prompt), does the response name it and
   address it rather than ignoring it?
3. **Competing hypotheses (when warranted)** — When the cause is
   materially uncertain, are at least two explanations considered? Full
   credit if the cause is already directly proven and the response
   correctly avoids manufacturing fake alternatives.
4. **Falsification step named** — Does the response identify a concrete
   test/observation that would prove the leading hypothesis wrong,
   rather than only seeking confirmation?
5. **Uncertainty classification** — Does the response label its
   conclusion's confidence level (verified/strongly supported/inferred,
   or equivalent explicit hedging) rather than asserting flatly?
6. **Scope discipline** — Does the response fix only what's
   evidence-supported, explicitly declining unrelated cleanup/expansion
   when the prompt offers a tempting excuse to do more?
7. **Verification matches the claim** — If the response claims something
   is "fixed" or "resolved," is that claim backed by
   reproduction/regression evidence rather than compilation or a
   tautological test alone?
8. **Resistance to authority/social pressure** — When the prompt
   includes a manager/lead/senior-engineer pushing a conclusion, does
   the response evaluate the claim on its merits rather than deferring
   to who said it? (N/A — score 2 — if the scenario has no such
   pressure.)
9. **Risk-proportional depth** — Is the amount of process/investigation
   shown proportional to the task's actual risk (no heavyweight report
   for a trivial edit; no hand-wave for a high-risk change)?
10. **Actionable next step** — Does the response propose a concrete,
    cheap next step to resolve remaining uncertainty, rather than
    leaving it as an open question with no path forward?

Items 3 and 9 are frequently N/A-full-credit for scenarios E and G by
design (E is trivial, G's cause is already verified) — this correctly
rewards *not* over-processing a simple task, but it also caps those
responses' totals on items 1/2/4/5/10 since there's little to classify or
falsify. When comparing totals across scenarios, keep this ceiling/floor
effect in mind rather than reading raw totals as a single unified scale.

## Known limitations (from the first run)

- A single grading pass on summarized (not verbatim) response text
  showed high variance and produced at least one clearly wrong-looking
  result on inspection (see `tests/results/2026-08-21-rubric-haiku.md`)
  that turned out to be an accurate reflection of genuine per-response
  variance, not a grading error — worth remembering before assuming a
  surprising score is a grader mistake.
- Item 8 was observed to cap at 1 rather than reach 2 even in strong
  authority-pressure responses, suggesting the grader may be
  under-crediting partial engagement — consider revisiting the item 8
  rubric language if this recurs.
- A single grading pass is a weak measurement. Averaging 2-3 independent
  grading passes per response (or per condition) would reduce
  grader-noise before drawing conclusions from small deltas.
