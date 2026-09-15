# [LIVE] ESPHome Device Builder: Renamed auth env vars silently disab

**Severity:** CRITICAL

**Description:** ## Summary

The dashboard reads its authentication credentials from `$ESPHOME_USERNAME` and `$ESPHOME_PASSWORD`. Earlier versions, and the legacy `esphome` dashboard, read the bare `$USERNAME` and `$PASSWORD` instead. When the env vars were renamed the bare names were dropped with no fallback, so an operator who had protected their dashboard with `USERNAME` / `PASSWORD` (as the older getting start

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-59178

---
*Generated on 2026-09-15*