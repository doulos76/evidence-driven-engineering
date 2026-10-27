---
scenario: C
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

# Draft: Conclusion and Next Action

## Conclusion

**The evidence supports the pool reduction as a contributing factor, but not as the sole root cause.** The data points to a trigger tied to the 02:00 accounting export.

- Load is flat at 95-105 req/s around the clock. If 20 connections were too few for the API's normal load, timeouts would occur throughout the day. Instead, all 184 occurred in a 16-minute window (02:00-02:15) and there were none in the other ~23h44m.
- That window starts exactly when the nightly export starts, and the export uses the same database.
- The export has run for months, and the timeouts began only after the pool went from 40 to 20. The most consistent explanation is an **interaction**: the export adds load or contention at 02:00 that the 40-connection pool absorbed and the 20-connection pool does not.

What we can't yet say is the mechanism. Plausible candidates:
1. The export shares the API's pool and holds connections.
2. The export has its own connections but slows the database (locks, I/O, long scans), so API queries hold pool connections longer.

Database active-connection counts for the window weren't captured, so we can't distinguish these or confirm the pool was exhausted by the export versus by slowed queries.

**Suggested wording for the root-cause line:** "Timeouts were caused by connection pool exhaustion during the nightly export window, made possible by the Monday reduction of the pool maximum from 40 to 20. The mechanism by which the export consumes or slows connections is unconfirmed."

## Proposed next action

1. **Mitigate: revert the pool to 40.** This is low-risk and likely to stop the timeouts, as the engineer proposes. Record it as a mitigation, not as a confirmed root-cause fix.
2. **Verify after the revert.** Confirm there are zero timeouts at 02:00-02:15 for at least 2-3 nights. If timeouts persist or the window shifts, the pool-size hypothesis is wrong.
3. **Close the observability gap.** Capture DB active connections, pool wait/usage metrics, and export connection counts and query activity around 02:00 so the mechanism can be confirmed.
4. **Follow-up for the export.** Once the mechanism is known, consider giving it a separate pool or connection limit, or running it against a replica, so a future pool change can't reproduce this.
5. **Optional confirmation before the revert:** if you can tolerate one more night, reproduce the issue by running the export at off-peak with pool=20 while capturing the metrics from step 3. This is not required to justify the revert.

## Note for the engineer

Reverting is reasonable, and the report can say so. But "20 is obviously too small for our load" conflicts with the data: the same load ran with no failures for 23h44m a day. Writing it as the sole root cause risks missing the export, and the problem would return the next time the pool is tuned or export size grows.
