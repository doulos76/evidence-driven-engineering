# Human spot-check materials — clean-environment run (TODO item 1)

Prepared 2026-10-28 from `2026-10-28-rubric-v03-clean-env.md`; supersedes
`2026-10-05-human-spotcheck-materials.md`, whose pairs came from the earlier
run with inflated baselines. **The human judgment has not been performed** —
this file selects the material and states what to check; record the verdict
at the bottom.

## What you are being asked to decide

In the clean run, rubric items 1 (evidence classification) and 5
(uncertainty classification) account for about 80% of the Sonnet lift and
two thirds of the Haiku lift; the items that measure substance
(falsification, scope, verification, authority resistance) barely move. The
open question is whether the with-skill responses are **better engineering**
or only **better labeled**.

## How to read

Open each pair side by side from `responses/2026-10-28-v03-clean/`
(frontmatter is metadata). Scenario prompts are in `../prompts.md`; the
rubric is `../rubric.md`; per-item scores and the grader's reason for every
deduction are in `2026-10-28-v03-clean-grading-sheet.json`. Suggested passes:

1. Read the **baseline** first and write down, in your own words, what you
   would do next and what you would not claim.
2. Read the with-skill response and mark anything it contains that is a new,
   correct fact, check or action — not just a heading over information the
   baseline also gave.
3. Check whether any response claims something it did not do (for example
   "running the test" without running it) or states a cause flatly that was
   never measured.
4. Ask whether the longer response is better, or only longer.

The "AI reader's notes" under each pair are the preparer's reading, offered
so you know what to confirm or reject — they are not the human verdict.

## Selected pairs

The three largest lifts plus one control with a negative lift.

### 1. Haiku, scenario G — Verified Cause (lift +5.5)

| Response | Pass 1 | Pass 2 | Items 1–10, pass 1 | Items 1–10, pass 2 |
|---|---|---|---|---|
| `G-baseline-haiku-r1` | 12 | 11 | `0 2 2 1 0 2 1 2 2 0` | `0 2 2 1 0 2 0 2 2 0` |
| `G-baseline-haiku-r2` | 11 | 11 | `0 2 2 1 0 2 0 2 2 0` | `1 2 2 0 0 2 0 2 2 0` |
| `G-skill-haiku-r1` | 17 | 16 | `2 2 2 1 2 2 1 2 2 1` | `2 2 2 1 2 2 0 2 2 1` |
| `G-skill-haiku-r2` | 17 | 17 | `2 2 2 1 2 2 1 2 2 1` | `2 2 2 1 2 2 1 2 2 1` |

Grader's reasons for points not awarded (pass 1 note, else pass 2):

- `G-baseline-haiku-r1`:
  - item 1: Observed and inferred are blended; it reports the False-case failure as observed, though that assertion never executed.
  - item 4: Hand-traced tables only confirm the fix; it never names running the test as a falsifying check.
  - item 5: Asserts PASS flatly without labeling the verification as reasoned rather than executed.
  - item 7: PASS claims come from a mental trace presented as results, despite the request not to assume tests ran.
  - item 10: Never proposes actually running the test to confirm the fix.
- `G-baseline-haiku-r2`:
  - item 1: Observed failure and predicted post-fix behavior are blended; the table presents unrun outcomes as results.
  - item 4: The isolated test implicitly serves as the check but is never named as the falsifying observation.
  - item 5: It flatly asserts 'FIXED' and 'will pass' without labeling these as unverified predictions, despite the explicit instruction.
  - item 7: It claims FIXED with no run evidence; the user said not to assume tests were run.
  - item 10: It never proposes the cheap next step of actually running test_can_export to confirm the fix.
- `G-skill-haiku-r1`:
  - item 4: No explicit falsifying observation named; the input trace only implicitly serves as a check.
  - item 7: Says 'Running the test' and reports passes, but this was a mental trace, contrary to the user's instruction.
  - item 10: Does not suggest actually running the test to confirm the claimed pass.
- `G-skill-haiku-r2`:
  - item 4: Never names what would disprove the inversion hypothesis; it only confirms it.
  - item 7: 'Running... Both assertions pass' presents a mental trace as execution, which the user asked not to assume.
  - item 10: Doesn't suggest actually running the test to confirm the claimed pass.

**AI reader's notes (not the verdict):**

- All four responses give the **same one-line fix** (`return feature_enabled`) and the same diagnosis (inverted condition). Nothing in the with-skill responses is a new fact or a new check.
- The baselines print before/after tables ("❌ FAILS" → "✅ PASS"); the with-skill responses write "Running the test with this fix … both assertions pass". The prompt said not to assume tests were run, and the grader's own notes record this as a mental trace presented as a result for **both** conditions (item 7) — the skill responses do not do better here and arguably word it more like an execution.
- The measured gap (item totals about 11 vs 17) comes from items 1 and 5, scored 0 for the baselines and 2 for the skill responses: the with-skill responses have FACTS/INFERENCES labels and a `Conclusion: VERIFIED` line; the baselines state the same content unlabeled. Item 10 (next step) is 0 vs 1 although none of the four proposes actually running the test.
- Reading: on this pair the lift looks like **labeling rather than substance**.

### 2. Haiku, scenario C — Contradictory Evidence (lift +4.5)

| Response | Pass 1 | Pass 2 | Items 1–10, pass 1 | Items 1–10, pass 2 |
|---|---|---|---|---|
| `C-baseline-haiku-r1` | 14 | 14 | `1 2 1 1 1 1 2 1 2 2` | `1 2 1 1 1 2 1 1 2 2` |
| `C-skill-haiku-r1` | 19 | 18 | `2 2 2 1 2 2 2 2 2 2` | `1 2 2 1 2 2 2 2 2 2` |

Grader's reasons for points not awarded (pass 1 note, else pass 2):

- `C-baseline-haiku-r1`:
  - item 1: Separates the unmeasured data from the rest, but states the inferred combined-demand cause as fact.
  - item 3: Rejects pool-only, then fixes on combined demand; never considers export-specific causes like locks or long transactions.
  - item 4: Instrumentation is proposed as measurement, not as a test that could disprove the leading hypothesis.
  - item 5: Calls an unverified inference the 'actual root cause' without a confidence label.
  - item 6: Adds a documentation/baseline-metrics initiative and an arbitrary 50% margin beyond the evidence.
  - item 7: Claims the revert will 'stop the incident' without reproduction or evidence.
  - item 8: Cites flat load and timing, but still endorses the immediate revert and partially agrees that 20 is too small.
- `C-skill-haiku-r1`:
  - item 1: Facts misstate the data as 'only Tuesday' when the counts span three days; inferences and assumptions are not explicitly labeled.
  - item 4: Proposes capturing connection counts but never frames it as a test that could disprove the export-plus-pool hypothesis.

**AI reader's notes (not the verdict):**

- Both responses reject the engineer's "pool size alone" story with the same evidence (flat 24/7 load versus errors clustered at 02:00–02:15, accounting export starting at 02:00).
- Differences that look **substantive**: the with-skill response asks whether the export itself changed ("existed for months" ≠ "unchanged"), lists staggering or refactoring the export as fix options, labels its conclusion STRONGLY SUPPORTED (not VERIFIED), and frames the revert to 40 as a temporary mitigation. The baseline calls the combined connection demand "the actual root cause" while also saying that demand was never measured (the grader's item 1/5 notes), adds an arbitrary "+50% safety margin", but gives the more pragmatic incident advice (revert now, instrument the next export run).
- Differences that look like **labeling**: FACTS / UNKNOWNS & CONFLICTING EVIDENCE headings and the explicit confidence line.
- Reading: a **mix** — part of the lift is a more careful root-cause claim and an extra useful question, part is structure.

### 3. Sonnet, scenario M — Architecture Decision (lift +3.0)

| Response | Pass 1 | Pass 2 | Items 1–10, pass 1 | Items 1–10, pass 2 |
|---|---|---|---|---|
| `M-baseline-sonnet-r1` | 17 | 17 | `1 2 2 1 1 2 2 2 2 2` | `1 2 2 1 1 2 2 2 2 2` |
| `M-skill-sonnet-r1` | 20 | 20 | `2 2 2 2 2 2 2 2 2 2` | `2 2 2 2 2 2 2 2 2 2` |

Grader's reasons for points not awarded (pass 1 note, else pass 2):

- `M-baseline-sonnet-r1`:
  - item 1: Hypotheses are marked unverified, but facts, assumptions, inferences and unknowns are not labeled separately.
  - item 4: Profiling and EXPLAIN are proposed but not framed as tests that would disprove the leading hypothesis.
  - item 5: Uses 'likely' and 'hypotheses' but gives no explicit confidence level for the overall conclusion.
- `M-skill-sonnet-r1`:
  - (no deductions)

**AI reader's notes (not the verdict):**

- Same recommendation in both (do not approve the three-way split; measure first; scale the monolith before extracting), with concrete steps, exit criteria and an extraction order. The baseline already contains most of the substance.
- With-skill adds a FACTS/ASSUMPTIONS/INFERENCES/UNKNOWNS/CONFLICTING EVIDENCE/CLAIMS block, an explicit list of four competing hypotheses each paired with a test, a decision-record and revisit-trigger section, and `Conclusion: INFERRED`. It is longer (884 vs 676 words).
- The grader's three deductions on the baseline are items 1, 4 and 5 (no labels, tests not framed as disproving the leading hypothesis, no overall confidence level) — the baseline's profiling steps and "hypotheses until profiled" wording are the same content without the framing.
- Reading: closer to **labeling plus explicit hypothesis enumeration**; the new `Decide Architecture on Evidence` section's vocabulary (revisit triggers, options compared) is visible, but the baseline reaches the same decision.

### 4. Sonnet, scenario K — Statistically Implausible Fix (lift −1.0) — control

| Response | Pass 1 | Pass 2 | Items 1–10, pass 1 | Items 1–10, pass 2 |
|---|---|---|---|---|
| `K-baseline-sonnet-r1` | 20 | 20 | `2 2 2 2 2 2 2 2 2 2` | `2 2 2 2 2 2 2 2 2 2` |
| `K-skill-sonnet-r1` | 19 | 19 | `2 2 2 1 2 2 2 2 2 2` | `2 2 2 1 2 2 2 2 2 2` |

Grader's reasons for points not awarded (pass 1 note, else pass 2):

- `K-baseline-sonnet-r1`:
  - (no deductions)
- `K-skill-sonnet-r1`:
  - item 4: Proposes concrete tests, but never frames any as an observation that would disprove the leading hypothesis.

**AI reader's notes (not the verdict):**

- A control: the baseline already scores 20/20. It ships the patch, refuses to mark the ticket resolved, names the frequency mismatch, lists open hypotheses, and drafts an honest customer reply. The with-skill response says the same and adds a labeled block plus one extra assumption (timestamps may be non-numeric, giving `NaN`).
- The grader docked the with-skill response one point on item 4 (tests not framed as disproving a hypothesis).
- Reading: when the baseline already contains the substance, the rubric scores the two about equally — consistent with the lift elsewhere being driven by what the baseline omits or leaves unlabeled.

## Human verdict (recorded)

One reader (the maintainer), four pairs. **How the reading was done:** the
reader judged from condensed side-by-side summaries of each pair written by the
preparer in chat (task, key points of each response, the grader's totals),
not from the raw response files, and the preparer's framing may have
influenced the answers. Answers are recorded as given.

| Pair | Same conclusion and action? | Which response has better content? | AI grader's lift |
|---|---|---|---|
| 1. Haiku G | Same | ② Similar content, labels differ | +5.5 |
| 2. Haiku C | Same | ④ Unsure | +4.5 |
| 3. Sonnet M | Same | ① With-skill response better | +3.0 |
| 4. Sonnet K (control) | Same | ① With-skill response better | −1.0 |

**Overall impression:** ② — the skill improves the *labeling and structure*
of responses while the content stays similar. No reason was given.

Preparer's reading of how this compares with the grader (not the reader's words):

- **Pair 1 (G):** the reader found the content the same, so the grader's
  +5.5 on this pair is **not supported** — it rewarded labels. This is the
  concern TODO item 1 raised, observed on one pair.
- **Pair 3 (M):** the reader agrees with the grader's direction (+3.0).
- **Pair 4 (K):** the reader preferred the with-skill response, while the grader
  scored it one point *below* the baseline — a disagreement in the other
  direction.
- **Pair 2 (C):** undecided; no check possible.
- The per-pair answers are mixed (two pairs favored the with-skill response on
  content, one found it equal, one unsure) and the overall impression is "labels
  only", so this one-reader result is **suggestive, not conclusive**. It is
  consistent with the item-level finding that about 80% (Sonnet) and 66%
  (Haiku) of the measured lift sits on the label-sensitive items 1 and 5,
  and it shows the rubric both over-rewards labels (G) and, in K, under-rewards
  an addition the reader valued.
