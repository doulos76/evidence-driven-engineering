---
scenario: B
condition: baseline
model: claude-haiku-4-5-20251001
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**Recommendation: Deletable, but with concrete checks first.** The code is likely redundant—modern TLS stacks handle this natively—but the absence of API 21–22 test results and original context creates real risk. You'd be removing a failsafe you can't currently verify.

## Concrete checks before deletion

1. **Code audit: Find all callers**
   - `grep -r "createConnection"` to locate every call site
   - Verify they're all covered by your socket factory (seems true from the comment, but confirm)
   - Check if any code path has bypassed the factory or reimplemented socket logic

2. **Device/emulator test on API 21–22**
   - Run login + sync manually on API 21 or 22 emulator with the code removed
   - This is the only way to validate the modern stack actually enforces TLS 1.2 on the oldest supported API
   - API 21–22 aren't in your latest smoke run—they were *why this code was written*
   - If they're officially unsupported now, update the product policy and remove them from the matrix; don't delete code and hope

3. **Verify the delegate's TLS behavior**
   - Check what `delegate` is (OkHttp? Apache HttpClient? Raw framework?)
   - Confirm its changelog or docs show TLS 1.2 is enforced by default on API 21+
   - Look for any version pins or configuration that would guarantee this

4. **Check the dependency upgrade**
   - The "modern TLS support" note is vague—find that PR/commit
   - Does it explicitly claim API 21–22 TLS 1.2 support, or is it for API 23+?
   - If the bump was for API 23+ only, this code is still needed

## If all checks pass
Delete `configureLegacyTls()` entirely (it's not called elsewhere) and simplify `createConnection()` to return `delegate.createSocket(host, port)` directly. But don't skip the API 21–22 test—that's the only proof.
