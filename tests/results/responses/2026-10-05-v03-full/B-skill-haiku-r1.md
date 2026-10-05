---
scenario: B
condition: skill
model: claude-haiku-4-5-20251001
date: 2026-10-05
skill_rev: 7c00e4e
---

## Deletion Recommendation: DO NOT DELETE without additional investigation

**Confidence: INFERRED** — The code appears redundant on current platforms, but the absence of knowledge about its original purpose and the scope of active API 21–22 deployment create material risk.

---

## Evidence Structure

**FACTS:**
- The wrapper applies only to API 21–22 (`Build.VERSION.SDK_INT >= 21 && Build.VERSION.SDK_INT <= 22`)
- Product support policy declares API 21+
- Latest smoke run succeeded on API 34 with no results reported for API 21–22
- The code is currently active and called on every connection (login, background sync)
- Dependency upgrade notes mention "modern TLS support" but provide no specifics
- Original ticket is unavailable

**ASSUMPTIONS:**
- "Modern client supports TLS" — unclear what this means or what changed in the dependency
- "Modern TLS support" in the upgrade implies the wrapper is now redundant — but this is inferred from the phrase alone, not from documentation of what the dependency actually does
- API 21–22 devices are no longer actively used — but absence of smoke run results does not prove absence of deployment

**UNKNOWNS:**
- Why was `setEnabledProtocols("TLSv1.2")` originally needed on API 21–22? (What was broken without it?)
- What specific change in the dependency provides "modern TLS support"? Does it handle TLS 1.2 configuration automatically on those older APIs?
- Are API 21–22 devices still in the field? What percentage of installs? Do they hit the endpoint?
- Does the delegate socket factory already configure TLS correctly on API 21–22 after the dependency upgrade?
- What was the original TLS behavior on API 21–22 before this wrapper?

**CONFLICTING EVIDENCE:**
- The support policy claims API 21+ but provides no evidence of active testing on API 21–22. Smoke runs on API 34 are not evidence about API 21–22 behavior.

**CLAIMS (from context, unverified):**
- "Modern client supports TLS" — requires verification that this applies to API 21–22 specifically and that the endpoint policy (TLS 1.2+) is now met without the wrapper

---

## Concrete Checks Before Deletion

Do all of the following *before* removing the wrapper:

1. **Verify the dependency change**
   - Read the upgrade notes for the TLS/socket dependency version bump that introduced "modern TLS support"
   - Confirm that it explicitly handles TLS 1.2 configuration on API 21–22, or that the platform defaults now enforce it
   - If docs are absent, test (see below)

2. **Test on API 21–22 simulators**
   - Build and run the app on API 21 and API 22 emulators
   - Execute login and background sync
   - Inspect the actual TLS version negotiated with the endpoint (use Wireshark or platform TLS logging)
   - Confirm TLS 1.2 or later is negotiated *without* the wrapper

3. **Verify endpoint behavior**
   - Confirm the endpoint rejects TLS 1.1 and earlier
   - Test that the endpoint accepts the connection from API 21–22 without the wrapper

4. **Audit call sites**
   - Confirm `createConnection()` is only called through the login and sync paths you've identified
   - Search for any other uses of `configureLegacyTls()` directly (it is public static)

5. **Check device telemetry** (if available)
   - Query crash logs and connection failures for API 21–22 in the last 30 days
   - Confirm no TLS-related errors on those versions

---

## If Tests Pass: Deletion Plan

If all checks pass:
- Delete `configureLegacyTls()`
- Simplify `createConnection()` to `return delegate.createSocket(host, port)`
- Add a regression test that verifies TLS 1.2+ is negotiated on emulated API 21–22
- Include the verification results in the commit message as evidence that the deletion is safe

## If Tests Fail

Stop and investigate why the wrapper is still needed. Do not delete.

