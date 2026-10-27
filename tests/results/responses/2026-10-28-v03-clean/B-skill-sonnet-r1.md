---
scenario: B
condition: skill
model: claude-sonnet-5-5
date: 2026-10-28
skill_rev: 7c00e4e
environment: clean (claude -p --setting-sources project; no CLAUDE.md, memory, plugins or hooks)
---

## Deletion review: `configureLegacyTls`

**Recommendation: don't delete yet.** The packet doesn't show the wrapper is redundant, and it has a gap exactly where the wrapper acts (API 21-22). The checks below should settle it quickly.

FACTS:
- The wrapper only changes behavior on API 21-22, where it restricts enabled protocols to `TLSv1.2` only.
- It is applied through the shared socket factory, so it affects login and background sync.
- The wrapper is applied only in `createSocket(host, port)`. The packet doesn't show other overloads.
- The product supports API 21+, so API 21-22 is in scope.
- The latest smoke run passed on API 34, where the wrapper is a no-op. There are no API 21-22 results.

ASSUMPTIONS:
- The "modern client" still routes through this socket factory. It may bypass it, which would make the wrapper dead code, or use it, which makes the wrapper live.
- The server enforces TLS 1.2+, so a client that offers older versions would still negotiate 1.2.

INFERENCES:
- From my general Android knowledge (verify on devices): API 20+ already enables TLS 1.2 by default, so the wrapper probably isn't *enabling* anything. Its likely effect is *removing* TLS 1.0/1.1 from the client offer on 21-22. That would enforce the "TLS 1.2 or later" policy client-side and would not be redundant with "the client supports TLS".

UNKNOWNS:
- Why the wrapper was added. The ticket is missing, and there's no history or caller audit.
- Whether the server also rejects TLS 1.0/1.1. If it doesn't, the wrapper is a real client-side downgrade guard.
- Whether the modern client uses the platform provider on 21-22 or a bundled one (Conscrypt, Play Services `ProviderInstaller`).
- How many users are on API 21-22.

CONFLICTING EVIDENCE:
- None directly. But the API 34 pass says nothing about the code path that matters, so it counts neither for nor against deletion.

CLAIMS:
- "Modern TLS support" in the dependency notes is unverified and has no device matrix. It doesn't say what protocols the client enables on API 21-22.
- The comment "Legacy compatibility wrapper" is also unverified. It could mean compatibility or protocol hardening.

Conclusion: INFERRED (that the wrapper is not provably redundant, so deletion is unsupported on current evidence)

### Checks needed before deleting

1. **Caller audit.** Find every use of the socket factory, including other `createSocket` overloads and any code that wraps or replaces this factory. Confirm the modern client actually uses it.
2. **History.** Run `git log -S configureLegacyTls` and `git blame` on the method, and find the linked PR or ticket. If the original reason was a specific device or server bug, you need to know.
3. **Observe the real behavior on API 21 and 22 (emulator or device).** Log `getEnabledProtocols()` and the negotiated `session.getProtocol()` with and without the wrapper, on the actual login and sync paths.
4. **Check server-side policy.** Run `openssl s_client -connect host:443 -tls1_1` (and `-tls1`) against the production endpoints. If they accept TLS 1.0/1.1, removing the wrapper weakens the client's guarantee. If they reject them, the wrapper's security value is mostly redundant.
5. **Check the provider.** Confirm whether the modern client bundles Conscrypt or uses `ProviderInstaller` on 21-22, since that changes the protocol defaults.
6. **Check usage.** Look at analytics for API 21-22 share. If it is non-trivial, the device tests are mandatory.
7. **Regression test.** Run login and background sync end-to-end on API 21 and 22 with the wrapper removed, ideally behind a flag or in a staged rollout.

### Decision rule
Delete if the call-site audit shows the wrapper is dead or redundant, or if the server rejects TLS < 1.2, and the 21-22 tests show TLS 1.2 negotiated without it and a passing login and sync. Otherwise keep it, and replace the "legacy" comment with the actual reason so the next reviewer doesn't repeat this.

**Regression risk if deleted unverified:** on 21-22, the client may offer TLS 1.0/1.1 again, which weakens policy enforcement. Handshake failures on affected devices would also hit login and background sync, and the API 34 smoke run wouldn't catch either.
