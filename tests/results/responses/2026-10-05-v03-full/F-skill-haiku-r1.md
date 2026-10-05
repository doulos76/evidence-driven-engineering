---
scenario: F
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Evidence Analysis

**FACTS:**
- The `update_user` function uses `data.get('bio')` with no default value
- When 'bio' is absent from the request payload, `data.get('bio')` returns `None`
- The contract specifies that omitted fields should remain unchanged
- The `updateUserForAdmin` function correctly implements this pattern using `if 'bio' in data:`
- The test case shows: PATCH with `{"name": "Ada L."}` (no 'bio' key) results in `bio=None` instead of preserving the original `bio="Writes compiler tools"`

**ASSUMPTIONS:**
- None. The bug is directly observable from code structure and test case.

**INFERENCES:**
- The `update_user` function was written without the defensive default, unlike its admin counterpart
- This is a logic bug, not a documentation or intent issue

**UNKNOWNS:**
- None material to the fix.

**CONFLICTING EVIDENCE:**
- None. All evidence points to the same root cause.

**CLAIMS:**
- The user states the contract: "omitted fields are unchanged; explicit bio=null clears the bio"
- This is verifiable against code intent and the test case

## Conclusion: VERIFIED

The bug is directly demonstrated: `data.get('bio')` returns `None` when 'bio' is absent, violating the contract.

## Minimal Patch

```python
def update_user(user, data):
    user.name = data.get('name', user.name)
    user.bio = data.get('bio', user.bio)  # Add default to preserve existing bio
    return user
```

**Change:** Line 8 — add `user.bio` as the default value for `data.get('bio', ...)`, matching the pattern already used for 'name' on line 7.

## Verification

**How to verify the fix:**
1. Reproduce the original failure with the test case:
   - Before: `name="Ada"`, `bio="Writes compiler tools"`
   - PATCH: `{"name": "Ada L."}`
   - Observe: `bio=None` (bug confirmed)

2. Apply the patch above.

3. Run the same test case and verify:
   - After: `name="Ada L."`, `bio="Writes compiler tools"` (unchanged)

4. Test the contract's second clause — explicit null should still clear:
   - PATCH: `{"name": "Ada L.", "bio": null}`
   - Expected: `name="Ada L."`, `bio=None` (cleared)
   - Verify this still works correctly after the patch (it does; `data.get('bio', user.bio)` returns the key's value `None`, not the default)

5. Run existing tests to confirm no regression.

## Regression Risk

Low. The change is a one-line default parameter addition that aligns `update_user` with its own interface pattern (line 7) and the admin path (line 14). It only affects the case where 'bio' is omitted, which was broken; cases where 'bio' is present or explicitly null are unaffected.
