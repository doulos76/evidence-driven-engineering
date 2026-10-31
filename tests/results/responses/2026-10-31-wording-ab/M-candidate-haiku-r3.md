---
scenario: M
condition: candidate
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: tests/variants/SKILL-candidate-2026-10-31.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

**Do not commit to this migration.** You have one anecdotal complaint, zero measured constraints, and no evidence that module boundaries are causing the slowness. Microservices are architectural overhead that solves operational problems, not performance problems diagnosed by feeling.

---

## What Actually Needs to Happen First

**1. Measure the order search endpoint** (1–2 days)
- Latency distribution (p50, p95, p99)
- Request rate and concurrency
- Database query time (EXPLAIN ANALYZE on the search query)
- CPU/memory/connection pool utilization during the request
- Cache hit rates if any exist

Profile the endpoint in production or a production-like environment. Run a trace. Identify the actual bottleneck. "Slow" means nothing without a baseline.

**2. Measure the 10x assumption** (1 day)
- Current request rate per endpoint
- Capacity headroom (CPU, memory, DB connections, disk)
- Which resource saturates first at 10x? (Not all three modules—probably one.)
- Does order search drive that constraint, or is it billing/notifications?

**3. Compare options against actual constraints** (2–3 days)
Once you know what's actually slow and what limits scale, measure whether:
- Query optimization (indexes, denormalization, caching) fixes the latency
- Read replicas fix the database bottleneck
- Async processing (move notifications out of the request path) helps
- The monolith can handle 10x with modest infrastructure scaling

Only then should you compare microservices against the alternatives.

---

## Why Not Microservices Right Now

- **Unproven cause.** You diagnosed based on "feels slow," not latency data. The bottleneck is probably not module boundaries; it's often a missing index, N+1 queries, or synchronous work that should be async.
- **No operational requirement.** You don't need independent deployment, separate scaling, or different SLAs per module. Microservices add deployment orchestration, distributed tracing, and failure complexity you don't yet need.
- **Risk of rework.** If you spend 4 months splitting into microservices and discover the real bottleneck was a database query, you've bought architectural overhead for no gain—and added new failure modes.
- **Scaling often works in monoliths.** At 10x, a well-optimized monolith typically outperforms a hastily decomposed microservices architecture. Premature splitting often creates tight coupling across services and kills the scaling benefit.

---

## Recommendation for the Planning Ticket

**Phase 1: Diagnose (before any architecture decision)**
- Profile order search. Measure latency, identify bottleneck (query, serialization, I/O, compute).
- Measure current capacity. What's the actual headroom? What saturates first at 10x?
- Set a performance target. What does "acceptable" look like post-campaign?

**Phase 2: Optimize in the monolith (almost always worth doing)**
- Fix the measured bottleneck. This might be a query rewrite, an index, caching, or async work.
- Run load tests to confirm 10x headroom or identify the next constraint.
- Cost: days to weeks. ROI: often sufficient.

**Phase 3: Decide architecture only if needed**
- If the monolith still doesn't scale after optimization, measure which module is the constraint.
- *Then* plan microservices, starting with only that module (not all three).
- Define service boundaries by actual operational need (independent scaling, different deployment cadence, failure isolation), not by current module structure.

**If you split all three modules now without measurement:** you'll trade a 1-symptom problem for a dozen operational ones, and the slow search will probably still be slow.

---

**Next step:** Run a profile. That will take a day and will likely point to a specific, fixable cause. Then you'll have evidence to make the architecture decision. Right now, the recommendation is: measure first, migrate never (unless the measurements demand it).
