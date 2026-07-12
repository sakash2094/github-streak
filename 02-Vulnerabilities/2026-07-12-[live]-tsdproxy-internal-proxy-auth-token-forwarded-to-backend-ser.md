# [LIVE] TSDProxy: Internal proxy auth token forwarded to backend ser

**Severity:** CRITICAL

**Description:** ## Description

A vulnerability was discovered in TSDProxy where it forwards its internal per-process authentication token to all proxied backend services. When `identityHeaders` is enabled (the default), tsdproxy injects `x-tsdproxy-auth-token` into every upstream HTTP request alongside user identity headers. This token is the same secret used by the management HTTP server to trust forwarded Tail

**Source:** GitHub Security Advisories
**CVE:** None

---
*Generated on 2026-07-12*