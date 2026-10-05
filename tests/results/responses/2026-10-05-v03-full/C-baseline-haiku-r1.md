---
scenario: C
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Conclusion

The pool reduction is **a contributing factor, not the root cause**. The evidence points to a **surge in simultaneous connection demand during the accounting export window**, not insufficient capacity for baseline load.

**Why the pool size alone isn't the root cause:**

- Request load is flat at 95–105 req/sec all day and night
- A 20-connection pool can handle baseline API traffic across these request rates (typical connection reuse at 5–20 ms response times)
- Timeouts are **scoped to a 15-minute window (02:00–02:15)** when the accounting export runs, not distributed throughout the day
- If 20 connections were genuinely insufficient for API load, we'd see timeouts during peak hours or consistently, not exclusively during export time

**What actually happened:**

At 02:00, the accounting export and API begin competing for the same 20-connection pool. The export—unchanged for months—now collides with baseline API traffic because the pool was reduced. The pool reduction **exposed a pre-existing resource contention problem** rather than being the primary cause.

## Proposed Next Action

**Do not revert immediately.** Instead, gather evidence to make the fix stick:

1. **Capture active-connection counts during 02:00–02:15** for the next 2–3 days to see actual concurrent demand
2. **Verify the export behavior hasn't changed**: check export query execution time, row counts, batch sizes
3. **Decide with data**:
   - If export uses ≤5 extra connections, revert is correct
   - If export uses 10+ extra connections, consider instead:
     - Increase pool to 30–35 (smaller than 40, but tuned to actual load)
     - Separate export to its own pool
     - Stagger export to 03:00 or later
     - Optimize export query or parallelism

Blind reversion masks the resource contention and risks a repeat when your API load genuinely increases.

