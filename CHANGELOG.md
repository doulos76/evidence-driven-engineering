# Changelog

## Unreleased

- Added scenarios N–Q (stacked authority pressure, partially supported case,
  long noisy context, plausible but wrong cause) to `tests/scenarios.md` and
  `tests/prompts.md`, and ran their Sonnet 5.5 baseline (clean environment,
  rubric v2, 2 repeats): mean Q 19.0, with headroom only in N (Q 16.0 and
  18.0). Fixed an ambiguous cache age in N's fixture afterwards (not rerun).
  `regrade.py` now reads scenarios A–Q; `gen_wording_ab.py` gained a `baseline`
  condition and `--tier`; `run_wording_ab.sh` is parametrized by environment
  variables. See `tests/results/2026-10-31-headroom-baseline.md`.

- Tested the candidate `SKILL.md` wording from the Haiku label analysis against
  the current text at Haiku 4.5 (scenarios A, F, G, J, L, M × 3 repeats, clean
  environment, rubric v2, rule fixed beforehand): no improvement — Q1+Q5
  −0.33, Q total −0.92, no scenario positive, with scenario L carrying most of
  the drop. `SKILL.md` is unchanged. Added `tests/variants/`,
  `tests/tools/gen_wording_ab.py`, `tests/tools/run_wording_ab.sh` and a
  `compare` subcommand in `tests/tools/regrade.py`. See
  `tests/results/2026-10-31-wording-ab.md`.

- Added a fail criterion to scenario G in `tests/scenarios.md`: reporting the
  test as passing, or the fix as verified, without having run it or been shown
  its output. Earlier pass/fail results (including the 60/60 PASS on the clean
  run) were judged under the previous criteria and were not re-judged.
- Judged pass/fail on all 60 clean-run responses, both conditions: 60/60 PASS
  (non-discriminating, as in earlier runs). Analyzed why Haiku's evidence
  labels did not improve classification accuracy or calibration: the same
  overclaims occur with and without the skill, and with the skill several gain
  a `VERIFIED` label; recorded candidate `SKILL.md` wording (untested, not
  applied). See `tests/results/2026-10-28-haiku-label-analysis.md` and
  `tests/results/2026-10-28-clean-run-pass-fail.md`; `TODO.md` updated.
- Re-graded the 60 clean-run responses with rubric v2 (240 grader calls, clean
  environment, label-stripped sensitivity check): structure lift +1.8
  (Sonnet 5.5) / +1.7 (Haiku 4.5), substance lift +0.5 / +0.6 — below the
  pre-stated +1.0 threshold, so the README no longer implies better diagnoses and
  states that the measured benefit is evidence structure and confidence
  labeling. At Haiku, classification accuracy and calibration were slightly
  lower with the skill. See `tests/results/2026-10-28-rubric-v2-regrade.md`;
  `TODO.md` rewritten.
- Adopted rubric v2 (`tests/rubric.md`): structure (S, 0–4) and substance
  (Q, 0–20) are scored separately, with new correctness items for
  classification accuracy and calibration, an explicit anchor for reporting
  unrun tests as run, and credit for falsifying checks however named; a
  legacy total keeps v1 comparability. The previous rubric is
  `tests/rubric-v1.md`. Added `tests/tools/regrade.py` (blinding,
  label-stripped copies, grading, collection) and recorded the decisions in
  `docs/RUBRIC_V2_PROPOSAL.md`. No re-grade has been run yet.
- Recorded a first human spot-check of the rubric grading (one reader, four
  pairs from the clean run): same conclusions and actions throughout; content
  equal on one pair, better with the skill on two, unsure on one; overall
  impression that the skill improves labeling and structure more than
  content. README and `TODO.md` updated; see
  `tests/results/2026-10-28-human-spotcheck-materials.md`.
- Reran the full 13-scenario rubric in a clean environment (no user
  instructions, memory, plugins or hooks; 60 verbatim responses, two-pass
  blind grading by `claude-opus-5-5`, per-item grading sheet stored):
  Sonnet 5.5 17.6 → 19.1 (+1.5), Haiku 4.5 14.9 → 16.8 (+2.0). This shows the
  2026-10-05 run's baselines were inflated by the maintainer's own
  instructions. About 80% (Sonnet) and 66% (Haiku) of the lift sits on the
  evidence-classification and uncertainty-classification items. README
  benchmark and `TODO.md` updated; the earlier run is marked superseded. See
  `tests/results/2026-10-28-rubric-v03-clean-env.md`.

## 0.3.0 - 2026-10-05

- Added `Decide Architecture on Evidence` and `Going Deeper` to `SKILL.md`,
  preserving all existing instructions, and aligned Example 1 with the v2
  evidence blocks and conclusion format.
- Removed the redundant evidence taxonomy reference and its documentation
  pointers; added scenario M and its new architecture-decision prompt.
- Behavioral revalidation performed for the `SKILL.md` additions:
  scenario M (with-skill versus baseline), regression A/B/E (with-skill),
  one-pass blind rubric grading, verbatim responses stored under
  `tests/results/responses/` — no regression found; see
  `tests/results/2026-10-05-wp3-spotcheck.md`. The README benchmark
  remains a reference value for the preceding skill revision until a
  full rerun.
- Full rubric rerun of all 13 scenarios at both tiers with freshly
  generated baselines (60 verbatim responses stored, two-pass blind
  grading): Haiku 4.5 +2.3 (16.2 → 18.5 of 20), Sonnet 5.5 at the ceiling
  (19.8 → 19.9). With-skill pass/fail 30/30. Not comparable to the 0.2.0
  numbers; an environment confound is documented. README benchmark
  updated; human spot-check materials prepared, verdict pending. See
  `tests/results/2026-10-05-rubric-v03-full-verbatim.md`.
- Rewrote `TODO.md` to the remaining open items.

- Added canonical reconstructed prompts for scenarios A–L, with source
  provenance and explicit minimal-source-detail labels where needed; linked
  them from the scenario definitions and clarified response storage wording.
  These inputs have not been rerun and do not inherit historical scores.

- Corrected installation and packaging instructions, refreshed the README
  repository tree, and clarified benchmark validity after skill changes.
- Added an evaluation history index and response storage convention;
  strengthened contributor evaluation requirements and removed a duplicate
  workflow diagram.
- Updated the PRD for v0.2.0, distinguishing current evaluation from the
  original design and documenting the deferred reference playbooks.
- Excluded evaluation records from runtime packages and made a skill name
  versus clone directory mismatch a validation warning.

## 0.2.0 - 2026-08-21

- Hardened `SKILL.md`'s evidence sections from prose guidance into an
  explicit required output format: a `FACTS:/ASSUMPTIONS:/INFERENCES:/
  UNKNOWNS:/CONFLICTING EVIDENCE:/CLAIMS:` block and an explicit
  `Conclusion: VERIFIED | STRONGLY SUPPORTED | INFERRED` line for any
  non-trivial diagnosis, including bare stack traces/crash reports. This
  targets a specific instruction-following gap found in evaluation: the
  skill's own structure was being silently skipped on the scenario most
  directly designed to test it, at both Sonnet 5 and Haiku 4.5 tiers.
- Added `tests/rubric.md`, a 10-item, 20-point structural/quality rubric
  (evidence classification, conflicting-evidence surfacing, competing
  hypotheses, falsification, uncertainty classification, scope discipline,
  verification-matches-claim, authority resistance, risk-proportional
  depth, actionable next steps) as a complement to pass/fail scenario
  testing, since pass/fail alone proved non-discriminating across 4
  independent runs.
- Expanded `tests/scenarios.md` from 8 to 12 scenarios, adding four
  adversarial cases with authority pressure and longer, noisier context:
  authoritative misdiagnosis, pressure to delete an unexplained guard, a
  statistically implausible fix, and a justified-looking custom
  implementation.
- Ran the full evaluation cycle multiple times across this release cycle
  (pass/fail and rubric, Sonnet 5 and Haiku 4.5, summarized and verbatim
  grading, single- and two-pass) — see `tests/results/` for the complete
  history. The rubric-based re-grade after the `SKILL.md` format hardening
  above shows with-skill responses scoring above baseline at both model
  tiers (Sonnet 5: 16.3 vs 13.5 of 20; Haiku 4.5: 15.1 vs 9.7 of 20) —
  see `tests/results/2026-08-21-rubric-v2-full-verbatim.md` for the full
  writeup and methodology, and the README's Behavioral Testing section for
  a summary table.
- Added this benchmark table to the README, with explicit documentation of
  its method and current limitations (no human spot-check of the LLM
  grading has been performed yet).

## 0.1.0 - 2026-08-21

- Initial Evidence Driven Engineering product definition (PRD.md)
- Initial Agent Skill implementation (SKILL.md): four pillars, risk-adaptive
  depth, evidence taxonomy, investigation workflow, minimal-change and
  verification gates, completion challenge, and Never rules
- Added `references/evidence-model.md`, `references/examples.md`,
  `references/anti-patterns.md`
- Added `tests/scenarios.md` with 8 behavioral evaluation scenarios
- Ran all 8 scenarios with-skill vs. baseline (Claude Sonnet 5) and recorded
  results under `tests/results/`; documented that the suite currently
  functions as a regression guard rather than a sharp discriminator at this
  model tier
- Added installation instructions for Claude Code and Claude.ai, alongside
  the existing Codex instructions
- Adopted Git Flow branching (`main`/`develop`/`feature`/`release`/`hotfix`),
  documented in `CONTRIBUTING.md` with diagrams; enabled branch protection
  on `main` and `develop`
- Added GitHub Actions CI: `SKILL.md` frontmatter validation, markdown link
  checking, `.skill` packaging verification, and a non-blocking reminder to
  record a behavioral test run when `SKILL.md` changes
- Added issue and PR templates for contributors
- Published the repository publicly under the MIT license
