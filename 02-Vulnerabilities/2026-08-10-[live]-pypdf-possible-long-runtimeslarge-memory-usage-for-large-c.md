# [LIVE] pypdf: Possible long runtimes/large memory usage for large C

**Severity:** MEDIUM

**Description:** ### Impact

An attacker who uses this vulnerability can craft a PDF which leads to long runtimes and large memory consumption. This requires parsing the font width entries of a font with unusually large values, for example during text extraction.

### Patches

This has been fixed in [pypdf==6.15.0](https://github.com/py-pdf/pypdf/releases/tag/6.15.0).

### Workarounds

If you cannot upgrade yet, c

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-71852

---
*Generated on 2026-08-10*