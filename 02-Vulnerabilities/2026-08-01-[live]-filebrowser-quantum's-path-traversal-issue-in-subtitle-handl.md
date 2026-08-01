# [LIVE] FileBrowser Quantum's path traversal issue in subtitle handl

**Severity:** HIGH

**Description:** ### Summary

The `subtitlesHandler` endpoint (`GET /api/media/subtitles`) accepts two user-controlled query parameters: `path` and `name`, both of which are used in filesystem operations without sanitization, creating two independent path traversal vectors.

The primary vector is the `path` parameter: it is passed directly to `idx.GetRealPath()` without calling `SanitizeUserPath()`, allowing an at

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-54910

---
*Generated on 2026-08-01*