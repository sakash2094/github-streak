# [LIVE] gettext-converter: Prototype pollution in js2i18next() via c

**Severity:** MEDIUM

**Description:** ### Impact

`js2i18next()` is vulnerable to prototype pollution. When converting translations, it splits nested keys on the key separator (default `##`) and uses each segment as a dynamic object key while building the output object. A key whose segment is `__proto__` (e.g. `__proto__##gcPolluted`) causes the converter to resolve `Object.prototype` as the nested write target and assign the translat

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-55451

---
*Generated on 2026-08-21*