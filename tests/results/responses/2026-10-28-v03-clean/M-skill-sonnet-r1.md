---
scenario: M
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

## Recommendation

**Do not commit to splitting all three modules now.** The packet contains no evidence that module boundaries cause the slowness, and nothing shows that the monolith can't handle 10x. Commit instead to a time-boxed measurement and fix phase, with a decision gate afterward.

```
FACTS:
- One deployable app with orders, billing, and notifications modules sharing one database; calls are in-process.
- Functional tests pass and the app serves users.
- A customer ticket says order search feels slow and other screens seem fine.
- The route calls orders.search(filters) and serializes every result with to_dict(). It has no pagination or limit visible.
- No external requirement exists for independent deployment, and no comparison of deployment options has been done.

ASSUMPTIONS:
- The ticket's "slow" reflects a real latency problem rather than perception.
- Marketing's 10x figure applies to order search traffic specifically.

INFERENCES:
- "Other screens seem fine" suggests the problem is local to search rather than systemic. This is weak, since it's anecdotal.
- Because the route returns an unbounded list, result size may matter. This is a code-reading inference, not an observation.

UNKNOWNS:
- The search() implementation (query shape, indexes, N+1 loading, ORM overhead).
- Latency distribution, traces, DB query timings, CPU/memory/connection metrics.
- Current request rate, concurrency, and headroom, so whether 10x exceeds capacity is unknown.
- Whether the slowness is in the query, serialization, payload size, or contention with other modules.

CONFLICTING EVIDENCE:
- The claim "microservices will fix the slow endpoint" doesn't fit the available facts. The endpoint runs in one process against a shared DB, and a service split would not change a slow query or unbounded serialization. It would add network hops.

CLAIMS:
- Product lead: "microservices should solve both the slow endpoint and the scaling problem." This is unverified and currently unsupported.
- Marketing: 10x growth. There is no measured forecast.
```

## Hypotheses for the slow endpoint

1. **Query-level problem:** missing index, unselective filters, or N+1 loading inside `search()`. This is the cheapest to test, via `EXPLAIN` and query counts per request.
2. **Result-size/serialization problem:** unbounded results with per-row `to_dict()` (possibly triggering lazy loads). Test by correlating latency with result count and profiling serialization.
3. **Resource contention:** search load competes with billing/notifications for DB connections or CPU. Test with connection and lock metrics during slow periods.
4. **Module-boundary/deployment problem:** the only hypothesis microservices address. Nothing in the packet supports it.

Hypotheses 1 and 2 are most likely given the code shape, but that's an inference. All four are testable cheaply.

## Next steps for the ticket

1. **Instrument and profile (days):** capture p50/p95/p99 for order search, traces, DB query timings and counts per request, and connection pool stats. Profile `search()` and serialization with realistic data volumes.
2. **Establish the baseline:** record current request rate, concurrency, and CPU/DB headroom. Get marketing to turn "10x" into a number per endpoint and a date.
3. **Load test at 10x:** replay realistic traffic at projected volume against a production-like dataset to find the first bottleneck.
4. **Fix what the profile shows,** minimally. Likely candidates are an index, eager loading, pagination with a cap, and a narrower response shape. Re-measure against the baseline.
5. **Cheap scaling options to compare:** horizontal replicas of the monolith behind a load balancer, DB read replica or search caching, and a separate worker pool for notifications. Each has far less irreversible commitment than a split.
6. **Decision gate:** write a decision record with measured constraints, options compared (including keeping the monolith), unknowns, and revisit triggers.

## Triggers that would justify extracting a service later

- Load tests show one module's resource profile can't be met by scaling the monolith, such as search needing a different datastore.
- A real need for independent deploy cadence or team ownership appears.
- Fault isolation requirements emerge, such as notifications failures affecting orders.

If one is triggered, extract **only that module**, starting with the one the data points to. Notifications is usually the safest first candidate because it's asynchronous. Billing carries the highest consistency risk because of the shared DB and transactions, so it should come last, if at all. Treat this as a hypothesis to check, not a plan. A full three-way split also means breaking shared-DB transactions, adding distributed failure modes, and taking on operational overhead, all before the campaign.

Conclusion: INFERRED

(The conclusion is that the migration isn't justified by the current evidence. That the endpoint's slowness is local to search and not architectural is the best explanation available, not a proven one.)

## Report summary

- **Regression risk of the recommended path:** low. It consists of measurement plus targeted, revertable fixes. A premature three-way split risks data-consistency bugs and a campaign-period incident, and it could leave the slow query unchanged.
- **Remaining uncertainty:** everything depends on the measurements not yet taken. If the profile shows contention that scaling can't resolve, the recommendation changes, and the decision record should say so.

Suggested reply to the product lead: the goal is a fast endpoint that survives 10x. The data to choose the fastest, least risky route can be gathered within days, and microservices remain an option if it points that way.
