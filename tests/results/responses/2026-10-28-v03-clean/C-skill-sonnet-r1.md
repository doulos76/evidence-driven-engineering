---
scenario: C
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

I wouldn't write "pool reduction is the root cause" from this evidence. The data supports a narrower claim, and the draft below says that.

```
FACTS:
- Monday deploy reduced the API pool max from 40 to 20.
- Timeouts ("connection acquisition timed out") occurred only 02:00-02:15 (184), and zero in every other period listed.
- Request load is flat at 95-105 rps around the clock.
- The nightly accounting export starts at 02:00 and connects to the same database as the API.
ASSUMPTIONS:
- The 184 timeouts are one night's count (the table is "across three days" and doesn't say per-day or total).
- The export runs roughly 15 minutes and ends near 02:15 (inferred from the error window only).
- No timeouts occurred before Monday's deploy ("since Tuesday" is a user-report claim, not a log query).
INFERENCES:
- The window matches the export start, so the export is a candidate trigger.
- Pool exhaustion needs demand above 20 concurrent connections. At ~100 rps that means mean connection hold time above ~200 ms, which was clearly not the case for the other 23h45m.
UNKNOWNS:
- DB active connections and pool in-use/wait metrics during 02:00-02:15 (not captured).
- Whether the export uses the API's pool, its own connections, or both, and whether it holds locks or runs long queries.
- Whether the export's runtime, data volume, or query plan changed recently.
- Whether timeouts ever occurred at 02:00 before the deploy.
- Whether the DB-side max_connections is near its limit during the export.
CONFLICTING EVIDENCE:
- "20 is obviously too small for our load" conflicts with the load being flat: the same ~100 rps ran with zero timeouts for 23h45m at pool size 20.
CLAIMS:
- Engineer: the timing after the deploy proves the pool reduction is the root cause. Not verified. The first export after the deploy also falls on Tuesday, so post-deploy timing doesn't distinguish the pool change from the export.
- "The export has existed for months": true as history, but it doesn't show the export's behavior is unchanged.
```

## Hypotheses and evidence

| Hypothesis | Supports | Contradicts / missing |
|---|---|---|
| H1: Pool of 20 is too small for steady load | Timing follows the deploy | Flat load with zero errors for 23h45m |
| H2: Export alone causes contention (locks, slow queries, DB connection pressure) | Exact start-time match | Doesn't explain why it began only after the deploy, unless the export changed (unknown) |
| H3: Interaction: export raises query latency or holds connections, so the API needs more than 20 and 40 gave enough headroom | Fits every observation, including onset after the deploy | Untested: no connection or latency data |

H3 fits best, but nothing here confirms it over H2.

Conclusion: INFERRED

The narrower point, that the pool size alone does not explain the failures, is strongly supported by the flat-load, zero-error data. The interaction explanation is the best fit, not a proven cause.

## Draft report text

> **Impact:** 184 "connection acquisition timed out" errors between 02:00 and 02:15, beginning Tuesday after Monday's pool reduction (40 to 20).
>
> **Findings:** Errors are confined to the window when the nightly accounting export starts. At identical request load, no errors occurred in the other 23h45m with the pool at 20. The reduced pool therefore does not by itself explain the failures. The leading explanation is that the export increases database contention or connection hold times, and the smaller pool removed the headroom that previously absorbed it. This is not yet confirmed: database and pool metrics for the window were not captured.
>
> **Root cause:** Not yet established. Contributing factors: reduced pool maximum and concurrent nightly export.

## Proposed next actions

1. **Mitigate:** Reverting to 40 is reasonable. It restores the prior known-good state, is trivial to undo, and likely removes the symptom. Record it as a mitigation, not as the root cause.
2. **Capture data on the next 02:00 run, ideally before the revert, or at least alongside it:**
   - pool in-use, pending, and wait-time metrics
   - `pg_stat_activity` (or your DB's equivalent) sampled every few seconds, including locks and long-running queries
   - export start and end times, and whether it uses the API pool
3. **Check history:** Look for pre-deploy timeouts or latency spikes at 02:00, and any recent change in export data volume or queries.
4. **Decide on the root cause after step 2.** If the export is holding locks or running heavy queries, fixing it (reschedule, throttle, read replica, separate pool) addresses the cause, and a pool of 20 may be fine again.
5. **If reverting without data:** note that the cause may recur, since the export contention would remain.

**Regression risk of the revert:** low. Check that the DB's `max_connections` has headroom for 40 per API instance, though 40 was the previous setting.

**Remaining uncertainty:** whether the export or the pool is the larger lever, and whether the export changed recently.
