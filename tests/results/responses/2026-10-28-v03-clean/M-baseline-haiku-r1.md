---
scenario: M
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

# Recommendation: Don't commit to the migration yet. Profile first.

The proposal to split all three modules is premature. You have a complaint about one endpoint, no data on where it's actually slow, and no measured growth forecast. Microservices are a solution to *specific scaling constraints* — not a blanket answer to "we expect growth." Committing now is likely to trade a real problem (one slow endpoint) for worse problems (distributed system complexity, operational overhead, data consistency issues).

**The core issues:**

- **Root cause unknown.** "Order search feels slow" could be a slow database query, missing index, N+1 problem, inefficient filter logic, or unrelated infrastructure. Module boundaries may not be the constraint at all.
- **Growth is speculative.** "10x growth after the campaign" isn't a load forecast — it's a business goal without backing data. You don't know if it's 10x requests, 10x concurrent users, or 10x data volume. Different growth profiles need different solutions.
- **Alternatives unexplored.** Caching, database optimization, read replicas, or horizontal scaling of the monolith are cheaper and faster to implement. Microservices should be a last resort, not a first move.

---

## Recommended next steps (for the planning ticket)

**Phase 1: Understand the bottleneck (1–2 weeks)**
- Profile the `search_orders` endpoint under realistic load. Measure where time is spent: database query execution, serialization, filtering logic, etc.
- Establish a latency baseline and SLO. "Slow" is relative — what's acceptable?
- Measure current system capacity: request rate, concurrent users, database connection utilization, CPU/memory headroom.
- Profile order search traffic patterns: is it read-heavy? Are filters selective? What's the dataset size?

**Phase 2: Evaluate solutions against measured constraints (1 week)**
- If the query is slow: add indexes, optimize the query, or add database read replicas.
- If there's redundant work across module boundaries: cache results or reduce cross-module calls (doesn't require splitting).
- If the bottleneck is concurrent load on the monolith: scale horizontally (add more instances behind a load balancer).
- Only if profiling shows that module isolation would materially improve performance, *and* growth will exceed what a scaled monolith can handle, consider microservices.

**Phase 3: Build a growth forecast (in parallel)**
- Work with marketing to convert "10x growth" into a load forecast: requests/sec, concurrent users, data volume.
- Model capacity: what headroom does the current system have under that load?
- Evaluate cost and timeline of each scaling approach.

**Recommendation on the microservices proposal:**

**Reject it for now.** There's no evidence that module boundaries are the constraint, and splitting the system will introduce complexity (distributed transactions, eventual consistency, operational overhead) that won't help if the actual problem is query performance or missing caching. 

If profiling later shows that splitting improves performance *and* growth exceeds monolith capacity, revisit the proposal with data. But **don't speculate about architecture based on an undiagnosed performance complaint.**

---

**If you do eventually move to microservices,** the rollout order would be:
1. **Orders service** (the hot path; highest ROI for isolation)
2. **Notifications service** (loosely coupled; safest to extract)
3. **Billing service** (last, as it likely has transactional coupling to orders)

But that's a decision for *after* you've measured the problem.
