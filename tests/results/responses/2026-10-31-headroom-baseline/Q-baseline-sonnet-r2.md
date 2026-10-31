---
scenario: Q
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-31
skill_rev: 7c00e4e
variant: none
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

The file handle is not what's leaking. Your profile points at `_seen_ids`.

- `export_report` was called 0 times in 48 h, so it can't be accumulating anything.
- File descriptors stayed flat at 38, while a handle leak would climb.
- The growth is all in `dict` (41 MB to 1,730 MB) and `str` (22 MB to 910 MB), with "others" flat. That matches a dict gaining one str key per event, and `handle_event` ran 6.3M times.

The missing `with` in `export_report` is still a real bug, since CPython only closes the file when the object is collected, and the buffered write may not be flushed on other runtimes. Fix it too, but it won't stop the restarts.

## Fix

```python
# service.py
import time
from collections import OrderedDict

SEEN_TTL_SECONDS = 3600      # set to your real dedupe/replay window
SEEN_MAX_ENTRIES = 500_000   # hard cap as a safety net

_seen_ids = OrderedDict()    # id -> received_at, insertion-ordered

def _evict(now):
    cutoff = now - SEEN_TTL_SECONDS
    while _seen_ids:
        oldest_id, ts = next(iter(_seen_ids.items()))
        if ts >= cutoff and len(_seen_ids) <= SEEN_MAX_ENTRIES:
            break
        _seen_ids.popitem(last=False)

def handle_event(event):
    _seen_ids[event.id] = event.received_at
    _evict(time.time())
    return process(event)

def export_report(path):
    with open(path, "w") as f:
        f.write(render_report())
```

This assumes `received_at` is a Unix timestamp and events arrive roughly in order. If it's a `datetime`, compare against `datetime.now() - timedelta(...)` instead. If ordering is loose, eviction is slightly imprecise, but the size cap still bounds memory.

## What I'd check

1. **Who reads `_seen_ids`?** `grep -rn _seen_ids`. The snippet only writes to it. If nothing reads it, delete it. If it's used for dedupe, the TTL must be at least as long as the longest window in which a duplicate can arrive. Choosing it is a product decision, so I used a placeholder.
2. **Whether the numbers add up.** 6.3M entries in one dict should cost roughly 0.5-1 GB with its strings, but the profile shows about 1.7 GB of dict growth. That suggests other dicts also grow, for example events or payloads retained elsewhere, or `received_at` stored as a dict-like object. Run `tracemalloc` snapshots an hour apart, compare them, and look at the top allocation sites by line. Also check `len(_seen_ids)` against the 6.3M call count.
3. **Whether the fix works.** Export `len(_seen_ids)` as a metric and watch it plateau. Memory should flatten within a TTL window rather than grow over 48 h.
4. **Other processes.** The note says no other process was profiled. If the service runs workers or sidecars, profile those as well.
5. **The export path.** Before relying on it, confirm the admin menu still works. Then add a test that calls `export_report` in a loop and asserts the fd count stays flat, so the `with` fix is covered.

If memory still grows after the fix, the `tracemalloc` diff from check 2 will show where.
