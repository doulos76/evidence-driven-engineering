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
| [2026-08-21-rubric-v2-full-verbatim.md](./2026-08-21-rubric-v2-full-verbatim.md) | Rubric, verbatim two-pass, both tiers, SKILL v2 | **Current authoritative** |

Recommended reading order: the `run*` pass/fail records (non-discrimination),
then `rubric-haiku` (negative result), verbatim regrading, format hardening,
and finally the v2 full evaluation.

## Response Storage Convention

For WP2 and future evaluations, preserve original response text as follows:

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
