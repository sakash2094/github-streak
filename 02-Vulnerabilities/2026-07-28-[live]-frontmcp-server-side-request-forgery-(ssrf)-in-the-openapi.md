# [LIVE] FrontMCP: Server-Side Request Forgery (SSRF) in the OpenAPI 

**Severity:** MEDIUM

**Description:** ## Summary

The OpenAPI adapter's spec-change **poller** (`OpenApiSpecPoller`) re-fetched the
configured spec `url` on a timer using a raw global `fetch()`, bypassing the SSRF
guard (`safeFetch` / `assertUrlSafe`) that `OpenAPIToolGenerator.fromURL()` applies
to the initial spec load. As a result, the pinning/DNS-resolution hardening delivered
via `mcp-from-openapi >= 2.5.0` (advisory GHSA-65h7-9w

**Source:** GitHub Security Advisories
**CVE:** None

---
*Generated on 2026-07-28*