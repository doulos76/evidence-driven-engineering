# Changelog

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
