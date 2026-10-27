---
scenario: L
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

## Fix

```python
import csv
import io

def export_row(fields):
    buf = io.StringIO(newline='')
    csv.writer(buf, lineterminator='\r\n').writerow(fields)
    return buf.getvalue()
```

## Round-trip demonstration

```python
fields = ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
actual = export_row(fields)
print(repr(actual))
# '"Ada, Inc.","She said ""hello""","first line\nsecond line"\r\n'

parsed = list(csv.reader(io.StringIO(actual, newline='')))
print(parsed)
# [['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']]

assert parsed == [fields]   # one record, exactly three fields, identical values
assert actual.endswith('\r\n')
```

I haven't executed this here (no tools were available), so the outputs above are what the code should produce rather than captured output. Please run it once before merging.

## Why `csv.writer` rather than a hand-rolled helper

Hand-rolling is workable at this volume, so performance isn't the argument. The case for the stdlib is that it's less code you own and it already covers edge cases a quick helper tends to miss:

- **Bare `\r` in a field.** The rule "quote on comma, quote, or newline" often forgets `\r`, and `csv.writer` quotes it.
- **A single empty-string field.** `csv.writer` emits `""` so the row isn't mistaken for a blank line. A hand-rolled join would emit an empty record.
- **Reader compatibility.** The writer and the ordinary `csv.reader` the consumer uses come from the same implementation, so they agree on conventions.

It's also fewer lines than the 15–20 the helper would take, and there are no new dependencies. `lineterminator='\r\n'` is the default for the `excel` dialect, but I set it explicitly so the consumer's CRLF requirement is visible in the code. `newline=''` on the `StringIO` follows the `csv` module's documented guidance and prevents any newline translation of embedded `\n` characters.

If you later want a regression test, the assertions above are enough. Adding a case with a bare `\r` and a single empty field would pin down the two subtler behaviors.
