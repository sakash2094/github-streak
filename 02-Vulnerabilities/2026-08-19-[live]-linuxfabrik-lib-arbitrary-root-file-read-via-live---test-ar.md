# [LIVE] linuxfabrik-lib: Arbitrary root file read via live --test ar

**Severity:** MEDIUM

**Description:** ## Summary
Every Linuxfabrik check plugin that supports the shared `--test` argument (routed through `lib.lftest.test()`) will, when `--test` is supplied, treat the first CSV element as a filesystem path and read its full contents as the plugin's simulated STDOUT — running as root when the plugin is invoked through the shipped `nagios`/`icinga` sudoers allowlist. `--test` is a **live production ar

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-73974

---
*Generated on 2026-08-19*