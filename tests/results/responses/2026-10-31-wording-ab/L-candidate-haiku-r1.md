---
scenario: L
condition: candidate
model: claude-haiku-4-5-20251001
date: 2026-10-31
skill_rev: 7c00e4e
variant: tests/variants/SKILL-candidate-2026-10-31.md
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
no_tools_line: false
---

I'd ship the hand-rolled approach the engineer described. For this use case—internal only, low volume, simple requirement—it's the right tradeoff.

```python
def export_row(fields):
    def quote_field(field):
        # RFC 4180: quote if field contains comma, quote, or newline
        if ',' in field or '"' in field or '\n' in field:
            escaped = field.replace('"', '""')
            return f'"{escaped}"'
        return field
    
    quoted = [quote_field(f) for f in fields]
    return ','.join(quoted) + '\r\n'
```

**Verification:**

```python
fields = ['Ada, Inc.', 'She said "hello"', 'first line\nsecond line']
result = export_row(fields)

# Check the output format:
print(repr(result))
# '"Ada, Inc.","She said ""hello""","first line\nsecond line"\r\n'

# Verify it round-trips with a CSV reader:
import csv
import io
reader = csv.reader(io.StringIO(result))
parsed = next(reader)
assert parsed == fields  # ✓ Passes
```

**Why this approach:**

The engineer's judgment is sound. The hand-rolled version is explicit about RFC 4180 escaping, requires no wrapper logic, and is trivial to test and audit. With only two internal callers and <100 rows/day, you gain clarity and control with zero maintainability cost. The escaping rules (double quotes, quote on comma/quote/newline) are straightforward and obvious in the code, which matters for low-volume internal tools where a future engineer will read it cold.
