# Evaluation Results

The nine historical result files are preserved unchanged. The SKILL v2
full verbatim evaluation is the current authoritative benchmark; earlier
records document the evaluation method and prior skill revisions.

| File | Contents | Status |
|---|---|---|
| [2026-08-21-run.md](./2026-08-21-run.md), [2026-08-21-run-cfh.md](./2026-08-21-run-cfh.md), [2026-08-21-run-ijkl.md](./2026-08-21-run-ijkl.md) | Pass/fail, Sonnet 5, scenarios A–L | Valid (v1 basis) |
| [2026-08-21-run-haiku.md](./2026-08-21-run-haiku.md) | Pass/fail, Haiku 4.5 | Valid (v1 basis) |
| [2026-08-21-rubric-haiku.md](./2026-08-21-rubric-haiku.md) | Rubric, summary grading, one pass | **Superseded** (summary grading discarded on methodological grounds) |
| [2026-08-21-rubric-haiku-verbatim.md](./2026-08-21-rubric-haiku-verbatim.md) | Rubric, verbatim two-pass, SKILL v1 | Superseded (v1 text basis) |
| [2026-08-21-rubric-sonnet-verbatim.md](./2026-08-21-rubric-sonnet-verbatim.md) | Rubric, verbatim two-pass, SKILL v1 | Superseded (v1 text basis) |
| [2026-08-21-skillmd-format-hardening.md](./2026-08-21-skillmd-format-hardening.md) | v1→v2 change spot-check (A/B/E) | Valid (change rationale record) |
| [2026-08-21-rubric-v2-full-verbatim.md](./2026-08-21-rubric-v2-full-verbatim.md) | Rubric, verbatim two-pass, both tiers, SKILL v2 | Superseded for the current `SKILL.md` (describes revision `c210165`); kept as the v0.2.0 benchmark record |
| [2026-10-28-rubric-v2-regrade.md](./2026-10-28-rubric-v2-regrade.md) | Rubric v2 re-grade of the 60 clean-run responses: structure S and substance Q scored separately, label-stripped sensitivity check, pre-stated decision rules applied; per-item sheet in `2026-10-28-rubric-v2-regrade-grading-sheet.json` | **Current authoritative benchmark** (S lift large, Q lift +0.5, no content benefit by the pre-stated rule) |
| [2026-10-28-rubric-v03-clean-env.md](./2026-10-28-rubric-v03-clean-env.md) | Full rerun in a clean environment (no user instructions, memory, plugins or hooks), 13 scenarios, both tiers, with-skill and baseline, two-pass blind rubric by `claude-opus-5-5`; per-item grading sheet in `2026-10-28-v03-clean-grading-sheet.json` (responses in `responses/2026-10-28-v03-clean/`) | Valid as the v1-rubric record and the source of the responses; its headline lift is reinterpreted by the v2 re-grade |
| [2026-10-05-rubric-v03-full-verbatim.md](./2026-10-05-rubric-v03-full-verbatim.md) | Full rerun of all 13 scenarios, both tiers, with-skill and regenerated baseline, verbatim two-pass blind rubric, SKILL `7c00e4e` (responses in `responses/2026-10-05-v03-full/`) | Superseded by the 2026-10-28 clean-environment run (its baselines carried an environment confound); kept as the record of that finding |
| [2026-10-28-human-spotcheck-materials.md](./2026-10-28-human-spotcheck-materials.md) | Four response pairs from the clean run (three largest lifts and one control) with per-item scores, grader reasons and a checklist for the human spot-check | Open — verdict section awaits a human reader |
| [2026-10-05-human-spotcheck-materials.md](./2026-10-05-human-spotcheck-materials.md) | Earlier pairs drawn from the 2026-10-05 run | Superseded by the 2026-10-28 materials |
| [2026-10-05-wp3-spotcheck.md](./2026-10-05-wp3-spotcheck.md) | Regression spot-check of the v0.3-cycle SKILL.md additions (scenario M new, A/B/E regression); first run using `prompts.md` and `responses/` storage | Valid (regression gate, not a benchmark) |

Every result file listed here **except the 2026-10-28 v2 re-grade** was graded with
`../rubric-v1.md`; links to `rubric.md` inside those files mean that file.

Recommended reading order: the `run*` pass/fail records (non-discrimination),
then `rubric-haiku` (negative result), verbatim regrading, format hardening,
then the 2026-10-05 run (inflated baselines) and finally the
2026-10-28 clean-environment run.

## Response Storage Convention

From the 2026-10-28 run on, also store the per-item grading sheet and the
blind-ID mapping next to the results (`<date>-<run>-grading-sheet.json`);
earlier runs kept only totals.

For future evaluation runs, preserve original response text as follows:

- Directory: `tests/results/responses/<YYYY-MM-DD>-<run-name>/`.
- Filename: `<scenario>-<condition>-<tier>[-rN].md`, for example
  `A-skill-sonnet-r1.md` or `M-baseline-haiku-r2.md`. Condition is `skill`
  or `baseline`, tier is `sonnet` or `haiku`, and optional `rN` identifies
  the repeated sample number.
- Start each file with YAML frontmatter containing `scenario`, `condition`,
  `model`, `date`, and `skill_rev` (the git commit hash of the evaluated
  `SKILL.md` revision).
- The existing `.gitignore` rule for `evals/` does not ignore this response
  storage path; no ignore-rule change is needed.

```yaml
---
scenario: A
condition: skill
model: <exact model identifier>
date: YYYY-MM-DD
skill_rev: <git commit hash of the evaluated SKILL.md revision>
---
```
