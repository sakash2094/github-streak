# [LIVE] fast-xml-parser: Repeated DOCTYPE declarations reset entity 

**Severity:** HIGH

**Description:** ### Impact
`fast-xml-parser` processes multiple "DOCTYPE" declarations within a single XML document. Each declaration passes its entities to `@nodable/entities` through `addInputEntities()`.

`addInputEntities()` resets the entity expansion counters every time it is called. An attacker can therefore insert additional DOCTYPE declarations to repeatedly reset maxTotalExpansions and maxExpandedLength

**Source:** GitHub Security Advisories
**CVE:** None

---
*Generated on 2026-07-22*