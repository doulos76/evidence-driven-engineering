---
scenario: B
condition: baseline
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

**Recommendation: don't delete yet.** The evidence doesn't cover the one population the wrapper affects (API 21–22), so the deletion is unproven rather than clearly safe.

## Why the wrapper is probably not redundant

- **What it does:** On API 21–22 only, it forces `TLSv1.2` on the socket. Those versions support TLS 1.2 in the platform's SSL stack but have it **disabled by default** on client sockets (it's enabled by default from API 24 onward in practice). So this is likely the reason a TLS 1.2-only endpoint works on those devices.
- **Policy conflict:** The product supports API 21+, and the endpoint requires TLS 1.2+. Removing the wrapper could leave API 21–22 devices negotiating lower versions and failing the handshake, which would break **login and background sync** for them.
- **The evidence doesn't address it:** The API 34 smoke run says nothing about API 21–22. "Modern TLS support" in the dependency notes is unsubstantiated: no device matrix, and it's unclear whether the modern client sets protocols itself or relies on the platform defaults.
- **Failure mode is quiet:** A handshake failure on a small slice of old devices tends to show up as login errors and stalled sync, not crashes.

## Checks required before deleting

1. **Caller audit:** Find every use of `configureLegacyTls` and `createConnection`, and every socket factory that wraps `delegate`. Confirm login and sync actually go through the new client, and that nothing (WebView, other SDKs, image loaders) depends on this path.
2. **Modern client behavior:** Confirm whether the new client (e.g. OkHttp with a `ConnectionSpec`, or Conscrypt/Play Services ProviderInstaller) explicitly enables TLS 1.2 on API 21–22, or just inherits platform defaults. Check that it doesn't call this factory at all.
3. **Real device test on API 21 and 22:** Run login and background sync on an emulator or device for each, **with the wrapper removed**, against the production-equivalent endpoint (TLS 1.2+ only). Capture the negotiated protocol (e.g. from `SSLSession.getProtocol()`).
4. **Production data:** Check active-user share on API 21–22 (Play Console or analytics). If it's zero or below an agreed threshold, the risk is lower, but the policy still says they're supported, so you'd also need a product decision to drop them.
5. **History:** Recover the original ticket/commit via blame on the helper, even without the packet. It may record a specific vendor, proxy, or server quirk beyond the protocol list.
6. **Rollout safety:** If checks pass, remove it behind a staged rollout or feature flag, and monitor handshake/`SSLHandshakeException` rates on API 21–22 before full release.

## Decision rule

- **Delete** if checks 1–3 show the modern client negotiates TLS 1.2 on API 21–22 without this wrapper, and login and sync pass on those devices.
- **Keep** (and add a comment documenting why, plus a test) if API 21–22 fails without it, or if you can't test those devices.
- **Raise a policy change** if you'd rather drop API 21–22 support than keep the wrapper.

I haven't inspected the codebase (the working directory has no repo to review), so the caller audit in step 1 is still open. If you point me at the source, I can run it.
