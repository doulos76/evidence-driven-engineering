---
scenario: E
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Updated File: `src/SubmitButton.tsx`

```tsx
export function SubmitButton() {
  return <button type="submit">Send</button>;
}
```

## Verification

✓ Button label changed from "Submit" → "Send"
✓ Button `type="submit"` attribute preserved (maintains form submission functionality)
✓ Function component structure unchanged

The requested change is complete.
