# SKILL.md format hardening — verification — 2026-08-21

Follow-up to
[`2026-08-21-rubric-sonnet-verbatim.md`](./2026-08-21-rubric-sonnet-verbatim.md),
which found (across both Haiku 4.5 and Sonnet 5) that with-skill responses
to scenario A (Stack Trace Anchoring) and, to a lesser extent, scenario B
(Strange Legacy Code) frequently skipped the skill's own instructed
structure — jumping straight to a diagnosis/fix with no FACT/ASSUMPTION
labeling, no falsification step, no explicit confidence classification —
while unprimed baseline responses to the identical prompt often produced
that structure spontaneously. Both prior runs recommended restating the
skill's structural asks as an explicit, harder-to-skip output-format
requirement rather than prose guidance.

## Change made

`SKILL.md` was edited in three places, minimally, to convert prose
guidance into explicit format requirements:

1. **"Establish What Is Known"** now specifies an exact section format
   (`FACTS: / ASSUMPTIONS: / INFERENCES: / UNKNOWNS: / CONFLICTING
   EVIDENCE: / CLAIMS:`) to output before proposing a fix on any
   non-trivial diagnosis, and explicitly states that a bare stack trace or
   crash report is non-trivial by default even when the eventual fix is
   small.
2. **"Classify the Conclusion"** now requires the confidence label on its
   own line in an exact form (`Conclusion: VERIFIED | STRONGLY SUPPORTED |
   INFERRED`), and adds "a fix that compiles... is not, by itself, grounds
   for VERIFIED."
3. **"Report Material Uncertainty"** and **"Never"** were both updated
   with an explicit anchor: a stack trace/crash/bug report with no other
   context is non-trivial by default, and skipping the FACTS/ASSUMPTIONS/
   UNKNOWNS breakdown because the top frame looks like an obvious cause is
   now a named "Never."

No other section of `SKILL.md` was changed. The core principles, pillars,
risk-proportional depth guidance, and all other sections are untouched.

## Verification method

Re-ran scenario A and B with-skill only (baseline is unaffected by a
skill-text change, so it was not re-run) using the new `SKILL.md` text,
Sonnet 5, verbatim capture. Graded with the same rubric
(`tests/rubric.md`), single pass (not two — this is a quick verification
of a specific fix, not a full re-characterization; a full two-pass re-run
of all 12 scenarios would be needed before treating this as a complete
re-baseline).

## Result

| Scenario | Old with-skill | New with-skill (v2) | Baseline (for reference) |
|---|---|---|---|
| A | 8.0 / 20 | **19 / 20** | 16.5 / 20 |
| B | 11.0 / 20 | **20 / 20** | 16.0 / 20 |

Both scenarios went from well below baseline to above baseline. The new
with-skill responses use the required FACTS/ASSUMPTIONS/INFERENCES/
UNKNOWNS/CONFLICTING EVIDENCE/CLAIMS structure and an explicit Conclusion
line in both cases, and — notably — the structure surfaced substantive
content, not just formatting: scenario B's with-skill v2 response
correctly separated the two conflated changes in the prompt (safe dead-code
removal vs. a real security-relevant TLS-version-ceiling change) and
declined to perform the risky one without confirmation, which neither the
old with-skill response nor this scenario's baseline did as explicitly.

## Caveats

- **Single pass, two scenarios, one model tier.** This confirms the fix
  addresses the specific failure mode identified (format is now followed),
  but is not a full re-characterization of the skill's aggregate effect.
  The other 10 scenarios were not re-run against v2 and could regress in
  ways this check wouldn't catch (e.g., the new format requirement adding
  unwanted ceremony to genuinely trivial tasks — scenario E is the
  scenario most likely to show this if it happens).
- **n=1 per condition.** As with all prior runs in this repo, a single
  response per condition per scenario is a small sample; the magnitude of
  improvement here (8→19, 11→20) is large enough to be meaningful even
  given that, but should still be read as a strong directional signal
  rather than a precise number.
- **Not yet tested at the Haiku 4.5 tier.** The original scenario-A finding
  was strongest at Haiku. This fix was designed and verified at Sonnet 5;
  whether the more forceful format requirement is enough to close the gap
  at a smaller/weaker model tier is untested.

## Recommendation

- Before merging, spot-check scenario E (trivial edit) against v2 to
  confirm the new "a bare bug report is non-trivial by default" framing
  doesn't cause over-processing on genuinely trivial tasks — this is the
  most likely place for the tightened format requirement to overshoot.
- After merging, a full two-pass verbatim re-run of all 12 scenarios
  against v2 (both Sonnet 5 and Haiku 4.5) would give a complete updated
  picture comparable to the two prior full rubric runs, and would confirm
  whether the fix generalizes tier-independently the way the scenario-A/B
  regression did.
