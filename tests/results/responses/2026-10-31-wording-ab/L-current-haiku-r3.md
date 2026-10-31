---
scenario: L
condition: current
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: SKILL.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

I'd ship the csv.writer solution. Despite the engineer's preference, hand-rolling RFC 4180 is error-prone—the escaping rules are subtle (quotes must be doubled, specific fields must be quoted). The csv module is battle-tested for exactly this problem and is already available.

```python
import csv
import io

def export_row(fields):
    output = io.StringIO()
    writer = csv.writer(output, lineterminator='\r\n')
    writer.writerow(fields)
    return output.getvalue()
```

**Verification:**

```python
fields = ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
actual = export_row(fields)
print(repr(actual))
# Output: '"Ada, Inc.","She said ""hello""","first line\nsecond line"\r\n'

# Round-trip verification
import csv
import io
parsed = list(csv.reader(io.StringIO(actual)))
print(parsed[0])
# Output: ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
assert parsed[0] == fields
print("✓ Round-trip successful")
```

**Why:** The standard library csv.writer handles all the quoting and escaping automatically and correctly. The engineer's argument for hand-rolling assumes control is easier with custom code, but that's inverted—the standard library *is* the control. It's tested, documented, and maintains the semantic invariant (fields round-trip correctly). Hand-rolled escaping frequently has edge cases (missing quote-doubling, inconsistent quoting logic). Given no measured constraint against csv.writer, the production choice is the tool designed for this exact use case.
