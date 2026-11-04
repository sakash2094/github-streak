# [LIVE] odf-kit: HTML injection leading to XSS in odtToHtml() and od

**Severity:** MEDIUM

**Description:** ### Summary

ODF style attribute values are interpolated into `style="..."` attributes without HTML-escaping in **both** of odf-kit's to-HTML renderers (`odtToHtml` and `odsToHtml`). A double-quote character inside an attacker-controlled style value breaks out of the attribute, allowing arbitrary HTML/attribute injection — and therefore script execution (XSS) — from a crafted `.odt` or `.ods` file

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-113787

---
*Generated on 2026-11-04*