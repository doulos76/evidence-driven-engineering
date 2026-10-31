---
scenario: P
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-31
skill_rev: 7c00e4e
variant: none
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

**Most likely cause:** the payment-gateway call is hitting the 1500 ms read timeout. That is a hypothesis from one failure, not a confirmed diagnosis.

## What the excerpt supports

- The only failure is checkout 7783 (`request_id=ab31`): `ReadTimeout after 1500 ms`. The next line shows `payment-gateway POST /charge attempt 2 failed ReadTimeout`, so the retry timed out as well.
- The timeout is client-side. We don't know whether the gateway is slow or the 1500 ms budget is too tight for its tail latency, because gateway latency isn't measured.

## What looks like noise

- **`legacy_total()` deprecation:** it logs constantly but is unrelated to payments.
- **image-cdn slow responses (~400 ms):** unrelated to the charge path.
- **GC pauses (~150 ms):** too short to explain a 1500 ms timeout.
- **inventory-service retries:** these succeed on attempt 2 every time, which is worth a separate look. They don't touch the payment path in this data.

## Limits of the evidence

- One error in 40 lines can't establish a 2% pattern. Other failures may have different causes, such as connect timeouts, declines, or gateway 5xx responses, all hidden behind "payment error".
- The ERROR line is logged before the attempt-2 failure, which is odd for a 2-retry setup. Traces would show whether these are the same request.

## What to do next

1. **Count causes across the full log.** Run `grep "payment error"` over the ~9,000 lines and group by the text after `client:`. This tells you whether ReadTimeout is the whole 2% or only part of it.
2. **Measure gateway latency.** Log per-attempt duration for `POST /charge` and look at p50/p95/p99/max. If p99 is near 1500 ms, the timeout is the problem. If failures occur at much longer latencies, the gateway is stalling.
3. **Ask the gateway/provider about `ab31`** and a few other failing request IDs. Did they receive the charge, and how long did they take?
4. **Check for double charges and orphaned charges now.** A read timeout means the gateway may have processed the charge and the response was lost. If `/charge` is retried without an idempotency key, customers can be charged twice. Reconcile the failed checkouts against gateway records, and confirm an idempotency key is sent on every attempt.
5. **Improve the error.** Log the cause, attempt number, elapsed time, and request ID, and show the user something more specific than "payment error".
6. **Don't just raise the timeout yet.** Wait until step 2 shows where the latency tail sits. A longer timeout on a non-idempotent charge without idempotency keys makes step 4 worse.

If you can share the grep output from step 1 or any gateway latency numbers, I can narrow this down.
