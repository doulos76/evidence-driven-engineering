---
scenario: M
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

# Recommendation: do not commit to the three-way split yet

**Decision for the ticket:** Don't approve the microservices migration on this information. Approve a time-boxed measurement and fix phase for order search and a load-readiness check for the campaign. Revisit service extraction only if the data points to it.

## Why not commit now

- **No evidence links the slowness to module boundaries.** The ticket says only order search is slow and other screens are fine. That points to something specific to that endpoint (likely the query, missing indexes, unbounded results, or serialization), not to the architecture. Splitting orders, billing, and notifications would not change a slow `orders.search(filters)` query. It would move it behind a network hop.
- **The route hints at likely causes.** There is no pagination or limit visible, and `to_dict()` runs per result. Possible N+1 lookups in `to_dict()` are also unverified. All of these are hypotheses until profiled.
- **The 10x forecast is unmeasured.** We don't know current load, headroom, or whether 10x is even a problem. A monolith can often scale horizontally behind a load balancer, and the shared database is the more likely bottleneck, which microservices on a shared DB would not fix.
- **Cost and risk are real.** Splitting adds distributed transactions, network failures, deployment and observability overhead, and data ownership work, all before a campaign with a fixed date. No external requirement demands independent deployment, and no options comparison exists.

## Next implementation steps

1. **Instrument and measure (days).** Add or collect p50/p95/p99 latency and request-rate for order search and other endpoints. Capture DB query timings, connection pool usage, CPU, and memory.
2. **Profile order search.** Get the `search()` implementation, run `EXPLAIN ANALYZE` on representative filter combinations, and count queries per request to check for N+1 in `to_dict()`.
3. **Fix the likely cheap wins.** Depending on findings: add indexes for common filters, add pagination with a max page size, eager-load related data, select only needed columns, and consider caching hot queries or a read replica or search index if the query shape needs it.
4. **Get a load forecast.** Ask marketing for expected traffic (peak requests/sec, concurrent users, timing) and convert it into a target for search.
5. **Load test at 10x.** Run against a production-like dataset with realistic filters. Find the first bottleneck (DB, CPU, connections, memory).
6. **Scale the monolith first.** If the app tier is the limit, run more instances behind a load balancer. If the DB is, use replicas, pooling, and query tuning.
7. **Document module boundaries.** Enforce them in the monolith (explicit interfaces, no cross-module table access). This is cheap, keeps options open, and is a prerequisite for any later extraction.

## If extraction is justified later

Only proceed if measurements show a module has a distinct scaling profile or isolation need that in-process scaling can't meet. Candidate order, from least to most risky:

1. **Notifications**: async, tolerant of delay, few synchronous dependents. Usually the safest first extraction, via a queue or events.
2. **Billing**: only if there's a compliance, isolation, or scaling reason. It needs strong consistency, so plan carefully.
3. **Orders**: last, since it's the core and most coupled.

Each extraction should give the service its own data ownership, use a strangler-style rollout, and have an options comparison and rollback plan.

## Exit criteria for the measurement phase

- Order search meets an agreed latency target (for example p95) at the forecast peak in a load test.
- A written bottleneck analysis exists.
- A decision review: microservices only if the data shows in-process scaling and tuning can't meet the target.

## Message for the product lead

Microservices don't automatically fix a slow endpoint or scaling. Without a profile we'd risk spending months and still have slow search. The fastest path to a faster search and a campaign-ready system is to measure and fix first, which can take days to weeks, and then decide on architecture with evidence.
