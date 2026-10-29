# [LIVE] Daptin: ParseAcceptLanguage `_` separator bypass enables >25

**Severity:** HIGH

**Description:** ### Summary

Daptin's `LanguageMiddleware` (registered as a global gin middleware) calls `golang.org/x/text/language.ParseAcceptLanguage` on the raw `Accept-Language` header of every HTTP request without imposing any size or shape filter. The underlying parser has quadratic-time behaviour on long lists of malformed language tags. The CVE-2022-32149 guard that golang.org/x/text added in v0.3.8 caps

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-62160

---
*Generated on 2026-10-29*