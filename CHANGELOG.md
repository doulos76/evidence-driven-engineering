# Changelog

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
