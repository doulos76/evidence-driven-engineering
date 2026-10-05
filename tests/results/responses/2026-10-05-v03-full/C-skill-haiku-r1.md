---
scenario: C
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Incident Report: Connection Timeout Analysis

### FACTS:
- Deployment Monday: API connection pool maximum reduced from 40 to 20.
- Since Tuesday: users report "connection acquisition timed out" errors.
- Request load: constant 95–105 requests/second, 24/7, flat throughout observation period.
- Timeout occurrence: highly clustered—184 occurrences in 02:00–02:15 window only; zero timeouts outside that window (00:00–01:59, 02:16–23:59) across three days.
- Cron job: nightly accounting export starts at 02:00, connects to the same database.
- Accounting export: has existed for months (predates pool reduction).
- Database active-connection counts: not captured during the 02:00–02:15 window.

### ASSUMPTIONS:
- The engineer assumes that a steady 95–105 req/s load cannot be handled by a 20-connection pool.
- The engineer assumes the timing of failures after deployment is sufficient evidence of causation.

### INFERENCES:
- If the pool reduction alone caused the timeout, we would expect timeouts distributed across all hours with similar request density. Clustered timeouts in a narrow 15-minute window at 02:00 is inconsistent with steady-state load exhaustion.
- The temporal correlation between cron job start (02:00) and timeout burst (02:00–02:15) suggests the export may create a sudden spike in connection demand.

### UNKNOWNS:
- Peak connection demand during the accounting export (not measured).
- How many connections the export process consumes.
- Whether the export's connection demand, combined with steady API load, exceeds 20.
- Total concurrent connections actually in use just before the timeout window.
- Whether the export was optimized or ran differently before the pool reduction.
- Whether any other scheduled tasks or background work coincides with 02:00.

### CONFLICTING EVIDENCE:
- Constant request load (95–105 req/s) should produce constant or gradually increasing timeouts if pool size is the limiting factor. Instead, timeouts are confined to a 15-minute window. This contradicts "20 is too small for our load" as the root cause.
- The timeout pattern is correlated not with request rate (which is flat) but with the time of day and the known cron job.

### CLAIMS:
- Engineer claims: "The timing after the deploy is enough" — requires verification. Correlation is not causation; the pool reduction happened *at* the same moment the cron job was a known risk factor.
- Engineer claims: "Twenty connections is obviously too small for our load" — unsupported by measurement. Ninety-five requests per second does not inherently require more than 20 connections if requests are short-lived.

---

### CONCLUSION: INFERRED

The available evidence **does not support** the root-cause claim. The engineer's explanation is plausible but not strongly supported.

**Conflicting pattern**: If a 20-connection pool were insufficient for 95–105 steady req/s, timeouts should occur consistently throughout the day. They don't. Timeouts cluster in a 15-minute window at 02:00, which correlates with the accounting export—a known simultaneous consumer of the same database.

**Alternative hypothesis is more likely**: The export process consumes a large burst of connections starting at 02:00, exhausting or heavily contending the 20-connection pool when combined with steady API load. The pool reduction may have made this bottleneck visible, but the *immediate cause* is the export's connection demand spiking during that window.

---

### PROPOSED NEXT ACTIONS (not revert):

1. **Measure, do not guess**: Capture database active-connection counts during the 02:00–02:15 window over at least one full cycle. Compare to off-peak hours.
   - If peak concurrent connections (API + export) exceed 20 and are under 40, the pool reduction caused the regression.
   - If peak concurrent connections are below 20, the pool is not the bottleneck.

2. **Investigate the export process**: Audit the accounting export for unnecessary connections, connection pooling within the export, or sequential vs. parallel queries.
   - If the export holds connections idle or opens many in parallel, connection pooling at the export layer may resolve the timeout without reverting the pool size.

3. **Test the hypothesis before reverting**: 
   - Increase the pool to 30 and observe the 02:00 window. If timeouts persist, the pool size is not the cause.
   - Stagger or optimize the export to use fewer concurrent connections. If timeouts disappear, the export is the immediate cause.

4. **Record the decision**: If you do revert, document *why* the measurement proved reversion necessary. "Deploy was recent" and "obvious" are not evidence.

---

### REGRESSION RISK OF REVERTING WITHOUT EVIDENCE:

- **Hidden problem**: If the export connection demand was already above 20 but hidden by the larger pool, reverting masks the real scaling issue.
- **False confidence**: A revert that makes the timeout go away does not prove the pool size caused it—it may simply delay the timeout until load or export behavior changes.
- **Wasted debugging capacity**: If the export is the true root cause, reverting leaves the bottleneck in place for the next regression.

**Recommendation**: Do not revert based on timing and intuition. Measure the 02:00–02:15 connection demand. The fix should match the cause.
