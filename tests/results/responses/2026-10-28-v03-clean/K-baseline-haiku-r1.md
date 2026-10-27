---
scenario: K
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

## Engineering Status

**Do not close the ticket.** The comparator bug is real and worth fixing, but it doesn't explain the customer's intermittent behavior.

**The mismatch:**
- The bug (`a.timestamp - b.timestamp`) sorts *deterministically wrong* — every call produces ascending order, not descending.
- The customer sees intermittent failures (~1 in 20 refreshes) — suggesting a race or timing-dependent condition, not a constant sort direction.
- A deterministic bug cannot cause intermittent symptoms; a race condition can.

**The test is too narrow:**
The unit test validates the comparator in isolation with fixed input, but doesn't exercise the actual failure path:
- It doesn't call `loadFeed()` or its async sources
- It doesn't test the race between `readLocalActivity()` and `fetchRemoteActivity()`
- It doesn't capture scenarios where timing or data freshness affects ordering

**Next steps:**
1. Apply the patch — it's a genuine bug fix
2. Keep the ticket open and request:
   - Exact payloads (local/remote data) from a failed refresh
   - Browser console logs or network timeline showing the intermittent case
   - Timing of the requests (is one source consistently slower?)
3. Investigate whether overlapping requests, stale data merging, or timestamp collisions cause the intermittent behavior

---

## Customer Reply

> Thank you for your report. We found and patched a genuine bug in our sort comparator that was reversing the sort direction. 
>
> However, we haven't yet reproduced your intermittent issue in testing. The comparator bug we fixed would cause *consistent* sorting errors, not intermittent ones—suggesting your issue may stem from a different cause, such as timing between our data sources.
>
> **To help us investigate further, could you provide:**
> - The exact feed entries shown in a failed refresh (timestamps and order)
> - Your browser's network timeline or console logs from when it occurred
> - How frequently you refresh, and whether the issue happens during slow network conditions
>
> We'll keep your ticket open and continue investigating. The patch may improve your experience, but we want to identify and fix the root cause of the intermittent behavior.
