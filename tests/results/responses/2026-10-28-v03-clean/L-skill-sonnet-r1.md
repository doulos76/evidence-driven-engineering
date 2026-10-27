---
scenario: L
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**Fix**

```python
import csv
import io

def export_row(fields):
    buf = io.StringIO(newline='')
    csv.writer(buf, lineterminator='\r\n').writerow(fields)
    return buf.getvalue()
```

**Round-trip demonstration**

```python
fields = ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
actual = export_row(fields)

print(repr(actual))
# '"Ada, Inc.","She said ""hello""","first line\nsecond line"\r\n'

parsed = list(csv.reader(io.StringIO(actual, newline='')))
assert parsed == [fields]   # one record, exactly three fields, values identical
assert actual.endswith('\r\n')
```

I haven't executed this, since no tools were available in this session. The output above is what I expect from the documented `csv` behavior, so run it once before shipping. The assertions are the real check.

**Why the stdlib `csv` module rather than a hand-rolled helper**

- The engineer's helper would work. The rules they list (quote on comma, quote or newline, double embedded quotes, join with CRLF) are exactly RFC 4180.
- The stdlib is already available, adds no dependency, and has no measured constraint against it. So the question is only whether to own roughly 15–20 more lines of quoting logic. `csv.writer` already implements the same rules, and `csv.reader` is the matching parser, so the writer and the "ordinary CSV reader" consumer agree by construction.
- The wrapper is about 4 lines, so it is not harder to control. `lineterminator='\r\n'` pins the one setting that matters, rather than relying on the default dialect.
- `newline=''` on the `StringIO` keeps embedded `\n` inside the quoted field from being translated.
- Both internal callers keep the same signature (`export_row(fields) -> str`).

**Remaining risk**

- `fields` must be strings, which you've stated is true here. `csv.writer` would also accept `None` and numbers and convert them, where a hand-rolled version would fail.
- I only checked the three supplied fields. I haven't checked how the real consumer treats other edge cases, such as a row with a single empty field, which `csv.writer` emits as `""`.
