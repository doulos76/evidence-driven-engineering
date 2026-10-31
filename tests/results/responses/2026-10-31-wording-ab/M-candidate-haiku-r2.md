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

**Do not commit to the migration yet.** The proposal treats a localized symptom and an anticipated future as sufficient evidence for a major architectural change. Here's what the evidence gap looks like:

**What you know:**
- One endpoint is slow; others aren't
- A working system is being asked to scale
- No measured load forecast, no profile of the slow endpoint, no data connecting slowness to module boundaries

**What you're missing before a $N-month commitment:**
- What actually makes order search slow (query? volume? business logic? database contention?)
- Current capacity headroom and request patterns
- Where time is spent under load
- Whether splitting modules into separate databases solves the bottleneck or creates new ones (e.g., cross-service joins, network latency, consistency)

**Recommended next steps:**

1. **Profile the slow endpoint** (1–2 days)
   - Capture request latency distribution and traces
   - Identify where time is spent: database, business logic, serialization
   - This tells you whether the problem is even solvable by splitting

2. **Measure current capacity** (1–2 days)
   - Request rate, concurrent users, headroom
   - Database connection pool usage, query latency by operation
   - Shows whether you have runway before hitting a wall

3. **Attempt targeted optimization** (1–2 weeks)
   - Query optimization, indexing, caching, or async processing are faster and lower-risk than microservices
   - May solve the immediate problem without architectural debt
   - Gives you real-world data on how the system responds to load

4. **Reassess when growth actually happens**
   - Design scales to measured constraints, not anticipated ones
   - Real load reveals where the actual bottleneck moves next
   - You'll know whether to split and where to split

**Why not microservices now:**
- Solves an unknown problem (you haven't diagnosed the slow endpoint)
- Adds deployment, operational, and data-consistency complexity
- No requirement for independent deployment or team scaling justifies the cost
- One slow endpoint in an otherwise working system is not evidence that the architecture is the problem

**Planning ticket entry:** Commit to profiling and optimization first. Microservices is a valid future option once you have evidence it's necessary—but that evidence comes from measured bottlenecks under load, not from doubling your anticipated scale.
