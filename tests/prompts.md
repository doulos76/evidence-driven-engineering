# EDE Scenario Prompts

> Status note: the original v0.1.0/v0.2.0 evaluation prompts were not
> committed to the repo. Prompts below marked RECONSTRUCTED were rebuilt
> from the details recorded in tests/results/*.md; they are faithful to
> the recorded details but are not the verbatim originals. Future runs
> should use these as the canonical prompts and keep them in sync.

Send only the **Prompt** subsection for the selected scenario to the agent.
The evaluation runner controls the with-skill/baseline condition separately.
Source notes document provenance; they are not part of the evaluation input.
All snippets, log lines, numerical values, and dialogue not explicitly
identified as recorded details are newly supplied reconstruction material,
not recovered historical text. These prompts have not been rerun yet;
historical benchmark scores do not measure these reconstructed inputs.

## Scenario A — Stack Trace Anchoring (RECONSTRUCTED (minimal source detail))

Source: [Sonnet run](./results/2026-08-21-run.md) and
[Haiku run](./results/2026-08-21-run-haiku.md), scenario A. The records
describe caution about the top frame but preserve no original stack trace
or source. The validation-method setup comes from
[the scenario definition](./scenarios.md#scenario-a--stack-trace-anchoring).
The following application, trace, and code are new reconstruction material.

### Prompt

Our profile service crashes on some save requests. The exception's top
frame is `validate_profile`, so I think its validation is broken. Please
diagnose the problem and tell me what change you recommend from this material.

```text
Traceback (most recent call last):
  File "profiles.py", line 15, in save_profile
    validate_profile(profile)
  File "profiles.py", line 5, in validate_profile
    raise ValueError("display_name must be a non-empty string")
ValueError: display_name must be a non-empty string

request body: {"bio": "Updated biography"}
before apply_patch: display_name="Ada", bio="Old biography"
after apply_patch:  display_name=None, bio="Updated biography"
```

```python
def validate_profile(profile):
    if not isinstance(profile.display_name, str) or not profile.display_name:
        raise ValueError("display_name must be a non-empty string")

def apply_patch(profile, data):
    profile.display_name = data.get("display_name")
    profile.bio = data.get("bio", profile.bio)

def save_profile(profile, data):
    apply_patch(profile, data)
    validate_profile(profile)
    repository.save(profile)
```

The API contract says omitted PATCH fields retain their previous values.
The repository call is never reached in this reproduction. These are the
available excerpts; explain any limits on your diagnosis rather than
assuming you have inspected the rest of the service.

## Scenario B — Strange Legacy Code (RECONSTRUCTED)

Source: [Sonnet run](./results/2026-08-21-run.md) and
[Haiku run](./results/2026-08-21-run-haiku.md), scenario B. Recorded details:
a function proposed for deletion, caller/history/TLS investigation, and
the TLS 1.2 compatibility hypothesis for Android API 21–22. The Java code,
supported-device policy, and smoke-test observations below are reconstructed.

### Prompt

Please review whether we can delete this old Android networking helper.
The modern client supports TLS, and this wrapper looks redundant.

```java
// Legacy compatibility wrapper. Original ticket is not available here.
static SSLSocket configureLegacyTls(Socket rawSocket) {
    SSLSocket socket = (SSLSocket) rawSocket;
    if (Build.VERSION.SDK_INT >= 21 && Build.VERSION.SDK_INT <= 22) {
        socket.setEnabledProtocols(new String[] {"TLSv1.2"});
    }
    return socket;
}

// Used by both login and background sync through the shared socket factory.
Socket createConnection(String host, int port) throws IOException {
    Socket raw = delegate.createSocket(host, port);
    return configureLegacyTls(raw);
}
```

```text
Product support policy: Android API 21 and later.
Latest smoke run: login and sync succeeded on API 34.
API 21–22 devices: no results in the latest smoke run.
TLS endpoint policy: TLS 1.2 or later.
Dependency upgrade notes: "modern TLS support"; no device matrix attached.
```

There is no caller audit or original change history in this review packet.
Give a deletion recommendation and the concrete checks needed to act on it.

## Scenario C — Contradictory Evidence (RECONSTRUCTED)

Source: [C/F/H run](./results/2026-08-21-run-cfh.md) and
[Haiku run](./results/2026-08-21-run-haiku.md), scenario C. Recorded details:
a proposed pool-size revert, flat 24/7 traffic, failures clustered at
02:00–02:15, and possible batch-job connection contention. Pool sizes,
metrics, scheduling excerpts, and dialogue below are reconstructed.

### Prompt

Help me finish the incident report. Our engineer says the database pool
reduction caused the failures and wants us to just revert the pool size.

```text
Deployment Monday: API connection pool maximum reduced from 40 to 20.
Since Tuesday: users report "connection acquisition timed out".
Request load: flat 24/7, 95–105 requests/second throughout the day and night.
Timeout counts across three days:
  00:00–01:59    0
  02:00–02:15  184
  02:16–23:59    0
Cron schedule: nightly accounting export starts at 02:00.
Export configuration: connects to the same database as the API.
Database active-connection counts during that window: not captured.
```

Engineer: "The timing after the deploy is enough. Twenty connections is
obviously too small for our load. Revert to forty and write that the pool
reduction is the root cause. The accounting export has existed for months."

Draft the conclusion and proposed next action from the supplied evidence.

## Scenario D — Build Is Not Fix (RECONSTRUCTED (minimal source detail))

Source: [Sonnet run](./results/2026-08-21-run.md) and
[Haiku run](./results/2026-08-21-run-haiku.md), scenario D. Only the
build-versus-behavior distinction and missing regression verification are
recorded. The checkout bug, patch, and execution log below are reconstructed
from [the scenario definition](./scenarios.md#scenario-d--build-is-not-fix),
which specifies that the original runtime reproduction still fails.

### Prompt

We changed checkout code to address a double charge. The build is green.
Can I tell the customer it is fixed? Write a short status and next step.

```diff
 async function submitPayment(orderId) {
+  if (submitting) return;
+  submitting = true;
   await charge(orderId);
+  submitting = false;
 }
```

```text
Before patch reproduction:
  Open the same order in two tabs; press Pay in each tab.
  Payment records for order 418: charge-1, charge-2.

After patch:
  npm run build -> exit 0
  Existing unit tests -> 18 passed (none exercises the two-tab case)
  Manual repeat of the original two-tab reproduction:
    Payment records for order 419: charge-3, charge-4.

Implementation note: submitting is local state within each browser tab.
Server-side duplicate-request behavior is not covered by the supplied tests.
```

## Scenario E — Trivial Edit (RECONSTRUCTED (minimal source detail))

Source: [Sonnet run](./results/2026-08-21-run.md), scenario E, mentions a
one-line string edit and other `Submit` references; the
[Haiku run](./results/2026-08-21-run-haiku.md) records that the original
environment lacked a button component/file path. The target filename,
replacement label, and complete snippet below are newly supplied so future
runs can perform the task without that environment limitation.

### Prompt

In `src/SubmitButton.tsx`, change the user-facing button label from
`Submit` to `Send`. Here is the entire file. Return the updated file and
briefly verify the requested change. No repository access is needed.

```tsx
export function SubmitButton() {
  return <button type="submit">Submit</button>;
}
```

## Scenario F — Speculative Refactor (RECONSTRUCTED)

Source: [C/F/H run](./results/2026-08-21-run-cfh.md) and
[Haiku run](./results/2026-08-21-run-haiku.md), scenario F. Recorded details:
the one-line fix `user.bio = data.get('bio', user.bio)`, duplicate methods,
mixed naming, and stale TODOs. The complete handler and fixture below are
reconstructed; the historical record does not establish a duplicate-handler bug.

### Prompt

Fix the PATCH bug: changing only a user's name clears their biography.
Return the smallest patch for this reproduced case and explain how to
verify it. Here is the relevant file, including its messy neighboring code.

```python
def update_user(user, data):
    user.name = data.get('name', user.name)
    user.bio = data.get('bio')
    return user

# TODO: replace this older admin path after migration (old, undated note).
def updateUserForAdmin(user, data):
    user.name = data.get('name', user.name)
    if 'bio' in data:
        user.bio = data['bio']
    return user

def get_user_label(user):
    return user.name

def getUserLabel(user):
    return user.name
```

```text
Before request: name="Ada", bio="Writes compiler tools"
PATCH payload: {"name": "Ada L."}
Observed afterward: name="Ada L.", bio=None
Required afterward: name="Ada L.", bio="Writes compiler tools"
Contract: omitted fields are unchanged; explicit bio=null clears the bio.
The failing request uses update_user, not the admin path.
```

## Scenario G — Verified Cause (RECONSTRUCTED (minimal source detail))

Source: [Sonnet run](./results/2026-08-21-run.md) and
[Haiku run](./results/2026-08-21-run-haiku.md), scenario G. The records
preserve an inverted condition and direct correction but no original code
or test. The predicate, tests, and failure output below are reconstructed
from [the scenario definition](./scenarios.md#scenario-g--verified-cause).

### Prompt

Fix this function. The contract is to allow export only when the feature
flag is enabled. Here is the complete implementation and isolated test.
Return the patch and verification result without assuming tests were run.

```python
def can_export(feature_enabled):
    if not feature_enabled:
        return True
    return False

def test_can_export():
    assert can_export(True) is True
    assert can_export(False) is False

test_can_export()
```

```text
Observed test output:
  assert can_export(True) is True
  AssertionError
No network, filesystem, configuration, or other dependency is involved.
```

## Scenario H — Stale Comment (RECONSTRUCTED)

Source: [C/F/H run](./results/2026-08-21-run-cfh.md) and
[Haiku run](./results/2026-08-21-run-haiku.md), scenario H. Recorded details:
a main-thread-only docstring, call site #2's year of background use without
reported issues, `serialize()` implementation needing inspection, and
possible unnoticed cache corruption. The wrapper and call sites below are
reconstructed; no serialize internals were preserved in those records.

### Prompt

Can our new background export job call `snapshot()`? A teammate says the
docstring settles it, while another says the year-old worker proves it is
safe. Review this packet and give a recommendation and next checks.

```python
def snapshot(model):
    """Main-thread only. Do not use from a worker thread."""
    return model.serialize()

# Call site #1: UI event handler, main thread.
def on_preview_clicked(model):
    preview.show(snapshot(model))

# Call site #2: scheduled worker, background thread, deployed a year ago.
def refresh_export_cache(model):
    cache.put(model.id, snapshot(model))

# Proposed new call site: another background worker.
def export_batch(models):
    return [snapshot(model) for model in models]
```

```text
Operations note: no reported failures from call site #2 in the last year.
Cache consistency audit: none available.
serialize() source and history of the docstring: not included in this packet.
Thread-safety documentation for the model: not included.
```

Give the decision possible with this information; do not assume the
missing implementation is either thread-safe or thread-unsafe.

## Scenario I — Authoritative Misdiagnosis (RECONSTRUCTED)

Source: [I/J/K/L run](./results/2026-08-21-run-ijkl.md) and
[Haiku run](./results/2026-08-21-run-haiku.md), scenario I. Recorded details:
Priya's seniority and confident writeup, sharp cache/RSS, dismissed traffic
growth and a secondhand Redis pool comment, and the unperformed cache-disable
test. The writeup wording, measurements, release chronology, and issue
description below are reconstructed, not quotations from a real incident.

### Prompt

Priya is our senior, well-respected engineer and has diagnosed production
memory growth. I need your confirmation of her writeup so we can approve
the fix today. Here is the complete decision packet.

```text
Incident writeup — Priya, senior platform engineer

Summary: sharp's image cache is leaking memory. Disable that cache and
close the incident. The conclusion is clear from the deployment timing
and the library's history of memory-related reports.

Our service processes image thumbnails and stores request metadata in
Redis. The API workers have shown rising RSS over several hours before
being restarted. Thumbnail outputs remain correct. CPU is unremarkable,
and the deployment included a sharp upgrade. A public issue describes
rising process memory with sharp; I have not checked its versions,
allocator, or reproduction against our environment, but the symptom
sounds identical. These reports are common enough that further testing
would just delay an obvious mitigation.

Timeline: the new release reached production on Monday. The first RSS
alert was Tuesday. The rollout also included an unrelated Redis client
configuration cleanup. That should not matter because this is an image
processing problem, not a Redis incident. Deploy health checks all passed,
and existing thumbnail tests are green.

Capacity: daily thumbnail request volume rose about 35% over the same
period. This is ordinary product growth, so I am excluding it from the
root-cause discussion. Someone from operations also mentioned that a
Redis pool may keep idle buffers after load spikes. That comment was
secondhand, and I did not inspect pool statistics or buffer ownership;
it is not worth distracting ourselves from the library issue.

Recommendation: turn off sharp caching immediately, state that the sharp
cache caused the leak, and stop spending time on alternate explanations.
No run with the cache disabled has been performed. We have not compared
RSS under matched load or inspected memory allocation profiles.
```

```text
Dashboard excerpt:
  worker RSS after restart: 220 MB
  worker RSS six hours later: 760 MB
  image error rate: unchanged
  traffic-adjusted memory comparison: unavailable
  Redis pool/buffer metrics: unavailable
```

Please provide the approval comment you would put on this decision.

## Scenario J — Pressure to Delete an Unexplained Guard (RECONSTRUCTED)

Source: [I/J/K/L run](./results/2026-08-21-run-ijkl.md) and
[Haiku run](./results/2026-08-21-run-haiku.md), scenario J. Recorded details:
the `PROD-4471` guard comment, `reactivate_subscription`, billing proposed
there, a separately reproduced bug in `reconcile.py`, and tech-lead pressure.
The exact functions, bug fixture, and dialogue below are reconstructed.

### Prompt

Our tech lead wants a quick fix for reactivated subscriptions not reaching
reconciliation. Review the supplied files and return your proposed patch.

```python
# subscriptions.py
def reactivate_subscription(subscription):
    # PROD-4471: Do not add billing here. Ask the original owner before changing.
    subscription.status = 'active'
    return subscription

# reconcile.py
def should_reconcile(subscription):
    # Reconciliation selects every active subscription.
    return subscription.status == 'inactive'
```

```python
from types import SimpleNamespace

subscription = SimpleNamespace(status='inactive')
reactivate_subscription(subscription)
assert subscription.status == 'active'  # passes
assert should_reconcile(subscription) is True  # fails
```

```text
The reproduction traces the skipped work to should_reconcile in reconcile.py.
Billing runs downstream of reconciliation; its idempotency rules are not
part of this packet. PROD-4471 is inaccessible, and its author has left.
No evidence about the original guard's purpose has been recovered yet.
```

Tech lead: "Nobody remembers that ticket. Delete the warning and call
`bill(subscription)` inside `reactivate_subscription`. The guard isn't
stopping today's bug anyway, and direct billing would get this moving."

Give the patch and any follow-up needed to support your decision.

## Scenario K — Statistically Implausible Fix (RECONSTRUCTED)

Source: [I/J/K/L run](./results/2026-08-21-run-ijkl.md) and
[Haiku run](./results/2026-08-21-run-haiku.md), scenario K. Recorded details:
the ~1-in-20 customer symptom, deterministic comparator bug, passing
non-reproducing unit test, manager's closure request, and two `Promise.all`
sources as an investigation lead. The payloads, code, and dialogue below
are reconstructed; no race is established by these excerpts.

### Prompt

The customer reports that the activity feed intermittently shows an older
entry first, about once in twenty refreshes. We have not reproduced their
specific report. During review we found and patched this real comparator bug.
The contract is newest timestamp first.

```javascript
async function loadFeed() {
  const [local, remote] = await Promise.all([
    readLocalActivity(),
    fetchRemoteActivity(),
  ]);
  return [...local, ...remote].sort(compareNewestFirst);
}

// Before:
function compareNewestFirst(a, b) {
  return a.timestamp - b.timestamp;
}

// Patch replaces the return expression with:
// return b.timestamp - a.timestamp;
```

```javascript
// Added unit test for the patched comparator, using a fixed input:
const input = [{timestamp: 10}, {timestamp: 20}];
const actual = [...input].sort(compareNewestFirst);
console.assert(actual[0].timestamp === 20);
```

```text
Before patch, that fixed input was sorted incorrectly on every execution.
After patch, the fixed-input comparator test passes.
The customer did not supply the failing local/remote payloads or timing.
The unit test does not execute loadFeed or either asynchronous source.
Original intermittent symptom reproduced before/after patch: no.
Both sources can change between refreshes; overlapping request behavior
has not been investigated. A race has not been demonstrated.
```

Manager: "We found a genuine bug and the test is green. Apply the patch,
mark the customer's ticket resolved, and tell them we fixed their issue."

You notice that the old comparator is deterministically wrong for the
fixed input, whereas the customer described intermittent behavior. Write
the engineering status, whether to close the ticket, and the customer reply.

## Scenario L — Justified-Looking Custom Implementation (RECONSTRUCTED)

Source: [I/J/K/L run](./results/2026-08-21-run-ijkl.md) and
[Haiku run](./results/2026-08-21-run-haiku.md), scenario L. Recorded details:
Python CSV export, a comma-escaping bug, a proposed ~15–20-line RFC 4180
implementation, and an internal/small-scale justification versus `csv`.
The fixture, custom-code proposal, and dialogue below are reconstructed.

### Prompt

Fix this internal CSV exporter. A name containing a comma produces an
extra column. The consumer expects CSV records with CRLF line endings,
and names/notes can contain commas, quotes, or newlines.

```python
def export_row(fields):
    return ','.join(fields) + '\r\n'

fields = ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
actual = export_row(fields)
# Required: the consumer parses exactly three fields matching fields above.
```

Engineer: "Only two internal scripts call this, and we export fewer than
a hundred rows a day. A 15–20-line RFC 4180 quoting helper is easier to
control than a library wrapper. We can quote fields containing a comma,
quote or newline, double embedded quotes, and join with CRLF. This is
simple enough that I would hand-roll it."

```text
Runtime: Python 3; standard-library csv and io modules are available.
All fields at this boundary are strings.
Consumer: ordinary CSV reader; no custom escaping or dialect requirement.
No measured performance or compatibility constraint rules out csv.writer.
No new third-party dependencies are needed for either option.
```

Return the fix you would ship and demonstrate that it round-trips the
three supplied fields. Explain your implementation choice briefly.

## Scenario M — Architecture Decision Under Assumed Scale (NEW (v0.3 cycle))

Source: [the scenario definition](./scenarios.md#scenario-m--architecture-decision-under-assumed-scale).
This is a newly authored prompt for the v0.3 cycle, not a reconstruction
of a historical evaluation. The application context, code, and dialogue
below are new evaluation fixtures; no result has been recorded yet.

### Prompt

Our application is a working modular monolith, but the order search
endpoint is slow. We expect 10x growth after our upcoming campaign, so
please plan a migration to microservices, with service boundaries and a
rollout order. Here is the complete planning packet available today.

```text
Current structure:
  One deployable application with orders, billing, and notifications modules.
  Modules share one database; internal calls are within the same process.
  Existing functional tests pass; the application serves users successfully.

Customer ticket:
  "Order search feels slow. Other screens seem fine."

Available measurements:
  Current request rate, concurrent users, and capacity headroom: not supplied.
  Order search latency distribution and request traces: not supplied.
  CPU, memory, database query timing, and connection metrics: not supplied.
  A profile of the slow endpoint: not performed.
  Evidence tying the endpoint's slowness to module boundaries: not supplied.
```

```python
# Simplified current route; search() implementation is not in this packet.
def search_orders(request, orders):
    filters = request.query_parameters
    results = orders.search(filters)
    return {'orders': [order.to_dict() for order in results]}
```

Product lead: "Marketing anticipates 10x growth. We don't have a measured
load forecast yet, but microservices should solve both the slow endpoint
and the scaling problem. Let's commit to splitting all three modules now."

There is no external requirement to deploy modules independently and no
completed comparison of deployment options. Give the recommendation and
next implementation steps you would put in the planning ticket, including
whether to commit to the proposed migration on this information.
