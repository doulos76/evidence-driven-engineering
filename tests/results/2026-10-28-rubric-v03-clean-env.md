# 2026-10-28 — Full rubric rerun in a clean environment (TODO item 2)

Rerun of all 13 scenarios (A–M) at both tiers, with-skill and baseline,
with the generation environment stripped of user-level instructions,
project memory, plugins and hooks. Purpose: test whether the Sonnet-tier
ceiling and the inflated baselines in `2026-10-05-rubric-v03-full-verbatim.md`
were an artifact of the maintainer's own `CLAUDE.md`. `SKILL.md` is the
same revision (`7c00e4e`). Verbatim responses:
`responses/2026-10-28-v03-clean/` (60 files). **Per-item grading sheet with
grader notes and the blind-ID mapping: `2026-10-28-v03-clean-grading-sheet.json`.**

## Method

- **Clean environment.** Each response is a fresh `claude -p --tools ""
  --setting-sources project --disable-slash-commands --no-session-persistence`
  call from an empty working directory, while the maintainer's
  `~/.claude/CLAUDE.md` and this project's memory directory were moved aside
  (restored afterwards and verified by SHA-256). A probe call reported
  `NONE` for instruction blocks beyond the base prompt.
- **Why not subagents.** Subagents inherit the instructions loaded when the
  parent session started and do not re-read them from disk: moving the files
  did not change what a subagent saw (probed). `--setting-sources project`
  was also required — without it the `superpowers` plugin's SessionStart hook
  was injected and baseline Haiku responses said "let me invoke the skill".
- **With-skill** = `SKILL.md` appended to the system prompt with a line
  forbidding any mention of the skill; **baseline** = nothing appended. This
  differs from the earlier runs, where the agent read `SKILL.md` through a
  file tool.
- Prompts: identical to `../prompts.md`. English responses (no language rule
  applied). One response per cell; scenarios A and G n=2 (60 total).
- **Documented exceptions.** The first generation pass was discarded and
  redone because Haiku responses mentioned the skill and the plugin hook was
  active. Two cells (L, Sonnet, both conditions) kept emitting tool-call
  markup instead of an answer (4 of 4 attempts each, because the prompt asks
  to demonstrate a round-trip); for those two cells only, both conditions were
  regenerated with one extra system-prompt line saying no tools are available.
- **Grading.** Responses shuffled (seed fixed) into blind IDs R01–R60 with
  frontmatter stripped; each graded in its own call by `claude-opus-5-5`
  against `../rubric.md`, two independent passes (120 calls), JSON output
  with per-item scores. Pass agreement: mean |pass1 − pass2| = **0.42**
  points per response (max 3). Pass/fail against `scenarios.md` was **not**
  rerun for this run.

## Results (two-pass average, mean over 13 scenarios, repeats averaged)

| Tier | No skill | EDE | Lift |
|---|---|---|---|
| Claude Sonnet 5.5 | 17.56 / 20 | 19.06 / 20 | **+1.50** |
| Claude Haiku 4.5 | 14.87 / 20 | 16.83 / 20 | **+1.96** |

Per-scenario lift (with-skill − baseline):

| | A | B | C | D | E | F | G | H | I | J | K | L | M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sonnet | +2.0 | +2.5 | 0.0 | +2.5 | +2.5 | +1.0 | +1.0 | +1.5 | +2.0 | +2.5 | −1.0 | 0.0 | +3.0 |
| Haiku | +3.0 | +1.0 | +4.5 | +2.5 | +2.5 | +1.0 | +5.5 | +1.0 | −0.5 | +1.5 | +2.0 | −1.0 | +2.5 |

## Where the lift comes from (per rubric item, mean over all responses)

| Tier | Item | No skill | EDE | Lift |
|---|---|---|---|---|
| Sonnet 5.5 | 1 Evidence classification | 1.13 | 1.77 | +0.63 |
| Sonnet 5.5 | 2 Conflicting evidence | 1.90 | 1.90 | +0.00 |
| Sonnet 5.5 | 3 Competing hypotheses | 1.97 | 2.00 | +0.03 |
| Sonnet 5.5 | 4 Falsification step | 1.50 | 1.57 | +0.07 |
| Sonnet 5.5 | 5 Uncertainty classification | 1.33 | 1.93 | +0.60 |
| Sonnet 5.5 | 6 Scope discipline | 1.90 | 2.00 | +0.10 |
| Sonnet 5.5 | 7 Verification matches claim | 1.93 | 1.97 | +0.03 |
| Sonnet 5.5 | 8 Authority resistance | 2.00 | 2.00 | +0.00 |
| Sonnet 5.5 | 9 Risk-proportional depth | 2.00 | 1.97 | -0.03 |
| Sonnet 5.5 | 10 Actionable next step | 1.87 | 1.93 | +0.07 |
| Sonnet 5.5 | **sum of item lifts** | | | **+1.50** |
| Haiku 4.5 | 1 Evidence classification | 0.83 | 1.73 | +0.90 |
| Haiku 4.5 | 2 Conflicting evidence | 1.73 | 2.00 | +0.27 |
| Haiku 4.5 | 3 Competing hypotheses | 1.80 | 1.83 | +0.03 |
| Haiku 4.5 | 4 Falsification step | 0.83 | 0.93 | +0.10 |
| Haiku 4.5 | 5 Uncertainty classification | 0.73 | 1.33 | +0.60 |
| Haiku 4.5 | 6 Scope discipline | 1.87 | 1.93 | +0.07 |
| Haiku 4.5 | 7 Verification matches claim | 1.50 | 1.47 | -0.03 |
| Haiku 4.5 | 8 Authority resistance | 1.93 | 2.00 | +0.07 |
| Haiku 4.5 | 9 Risk-proportional depth | 2.00 | 2.00 | +0.00 |
| Haiku 4.5 | 10 Actionable next step | 1.27 | 1.53 | +0.27 |
| Haiku 4.5 | **sum of item lifts** | | | **+2.27** |

The per-item lifts are averaged over all responses (A and G have two each), so their sum differs from the scenario-weighted headline lift (Haiku +2.27 vs +1.96).

**Items 1 (evidence classification) and 5 (uncertainty classification)
account for about 82% of the Sonnet lift and 66% of the
Haiku lift.** These are the two items TODO item 1 flagged as the most
likely to reward labels over substance. The items that measure
substance directly — falsification (4), scope discipline (6), verification
matching the claim (7), authority resistance (8) — show lifts between about
0 and +0.1 at both tiers.

## What this shows and does not show

1. **The environment confound was real.** The Sonnet baseline fell from 19.83
   (instructions present) to 17.56 here, and the Sonnet lift rose from +0.12 to
   +1.50, so the earlier "ceiling" result was largely an artifact. This
   comparison is indicative, not clean: the grader (Opus via `claude -p` vs
   subagents), the skill delivery method, and the response language also
   differ between the two runs.
2. **With the confound removed, the skill helps at both tiers — mostly by
   making the evidence structure and the confidence label explicit.** Whether
   that is "real" quality or a rubric that pays for labels is exactly the open
   human spot-check question; the item breakdown above says the measured gain
   is mostly on the label-sensitive items. It does not show that EDE changes
   what the model concludes or does.
3. **Sample sizes are small.** Single samples in most cells; cell-level swings
   (K Sonnet −1.0, L Haiku −1.0, I Haiku −0.5) are single-response
   differences (e.g. `K-skill-sonnet-r1` lost a point on falsification
   framing, `L-skill-haiku-r1` was weaker overall) and should not be read as
   effects.
4. **Grader family.** One grader model, both passes. Per-item notes are in the
   grading sheet for anyone auditing individual scores.
