---
scenario: K
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Engineering Status

**Do not close the ticket.** Deploy the comparator fix immediately, but continue investigation into the customer's intermittent symptom.

### Established Facts

FACTS:
- The old comparator logic returns `a.timestamp - b.timestamp`, which sorts ascending (oldest first)
- The contract requires newest first
- The comparator bug is deterministically wrong: it fails on every execution with mixed timestamps
- The customer reports intermittent behavior (once per ~20 refreshes)
- No reproduction case with real customer data was provided

ASSUMPTIONS:
- The patch fixes all ordering issues caused by this specific bug
- The customer's feed includes both local and remote entries

INFERENCES:
- The comparator's wrong ordering would appear consistently, not intermittently, if it were the sole cause of the customer's issue
- The intermittent pattern suggests either: timing/race behavior during load, data variation between refreshes, or a separate code path

UNKNOWNS:
- What timestamps or data patterns did the customer actually see when the issue occurred?
- Are there other code paths that sort or filter the feed?
- Does the customer always have both local and remote data, or does one sometimes return empty?
- Does a race condition exist where partial results are displayed before both sources complete?

CONFLICTING EVIDENCE:
- A deterministic bug should produce consistent incorrect ordering, not intermittent issues
- The unit test confirms the bug exists, but doesn't execute the full `loadFeed` flow, concurrent I/O, or varying payloads

CLAIMS:
- Manager claim: "We found a genuine bug and the test is green" — TRUE for the comparator, but insufficient evidence that this bug caused the specific customer symptom

Conclusion: **STRONGLY SUPPORTED** that the comparator is buggy and should be fixed. **INFERRED** that it is the root cause of the customer's intermittent issue.

---

## Recommended Action

**Tier 1: Deploy immediately**
- Apply the comparator patch
- Merge the unit test
- Ship in next release

**Tier 2: Monitor & investigate**
- Ask the customer: "Can you capture the exact timestamps or entry order in your feed when you see the issue? Does it always happen with both cached and fresh data, or sometimes with only one?"
- Add telemetry to log feed payload sizes and final sort order at load time
- Monitor for follow-up reports after the patch ships

**Tier 3: If issue persists**
- Inspect for race conditions in Promise.all sequencing (local could update while remote is still fetching)
- Check whether overlapping refreshes could cause partial/stale data
- Review other sort or filter operations on the feed

---

## Customer Reply

Subject: Activity Feed Sorting — Fix in Progress

Thanks for reporting this. We found a real sorting bug in our feed code where oldest entries could appear first instead of newest. We're shipping a fix in our next release.

The bug we found is deterministic (wrong every time with certain data), but your report of *intermittent* issues suggests we may have additional causes to rule out — timing or data overlap during load.

Once you upgrade, please let us know if the issue persists. If it does, we'd like to capture the exact timestamps you see so we can dig deeper.

We appreciate you catching this.
