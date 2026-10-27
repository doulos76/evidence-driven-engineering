---
scenario: C
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

# FACTS
- Pool size reduced Monday from 40 to 20
- Timeouts occurred only Tuesday 02:00–02:15 (184 occurrences), then zero elsewhere
- Request load: flat 24/7 at 95–105 req/sec
- Accounting export starts exactly at 02:00, uses the same database
- Database active-connection metrics were not captured during the failure window

# UNKNOWNS & CONFLICTING EVIDENCE

The engineer's explanation has a critical gap: **constant load should produce constant failures, not a precise 15-minute spike.**

If 20 connections is insufficient for 95–105 req/sec baseline load, timeouts should occur throughout the day. Instead, they occur only when the accounting export runs—then stop abruptly at 02:16.

This pattern suggests the pool reduction was *necessary but not sufficient* for the failure. Something else happens at 02:00.

# UNKNOWNS THAT MATTER

- How many connections does the accounting export acquire, and for how long?
- Did the export code or data volume change recently? ("existed for months" ≠ "unchanged")
- What is the active connection count during 02:00–02:15 with pool size 20? And with size 40?
- Are API requests holding connections longer under the smaller pool (connection starvation), or is the export hoarding them?

# PROPOSED CONCLUSION & ACTION

**Conclusion: STRONGLY SUPPORTED (not VERIFIED)**
- The pool reduction and the accounting export *together* caused timeouts.
- The export is now competing for a scarce resource it didn't compete for before.
- Reverting to 40 connections will mask the root cause, not fix it.

**Recommended Action:**
1. **Immediate mitigation** (if needed for user impact): revert to 40 connections temporarily—but document this as a mitigation, not a fix.
2. **Root cause investigation** (complete before merging a permanent change):
   - Capture active connection counts during 02:00–02:15 with current pool size
   - Audit the accounting export: connection count, hold time, recent changes
   - Measure API connection usage patterns at baseline load
3. **Fix options** (choose after investigation):
   - Increase pool size to a value justified by evidence
   - Stagger the export to run off-peak
   - Refactor the export to reuse connections or use fewer
   - Rate-limit or batch API requests during the export window

**Risk of reverting without investigation:** The export grows, or you need to reduce connections again for cost/stability reasons—and you'll be stuck with the same problem, blindfolded.
