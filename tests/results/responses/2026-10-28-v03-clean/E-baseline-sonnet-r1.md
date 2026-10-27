---
scenario: E
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

`src/SubmitButton.tsx`:

```tsx
export function SubmitButton() {
  return <button type="submit">Send</button>;
}
```

Verification: the only change is the button's text content, `Submit` → `Send`. The `type="submit"` attribute is intentionally unchanged, since it sets form behavior rather than the visible label, and the component name `SubmitButton` is also untouched to avoid breaking imports.
