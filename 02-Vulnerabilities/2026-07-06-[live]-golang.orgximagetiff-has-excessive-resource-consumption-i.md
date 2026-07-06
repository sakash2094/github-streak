# [LIVE] golang.org/x/image/tiff has excessive resource consumption i

**Severity:** HIGH

**Description:** The TIFF decoder does not place a limit on the size of PackBits-compressed data. A maliciously-crafted image can exploit this to cause a small image (both in terms of pixel width/height and encoded size) to make the decoder decode large amounts of compressed data.

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-46599

---
*Generated on 2026-07-06*