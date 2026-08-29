# [LIVE] RestrictedPython guard hooks can be shadowed via positional-

**Severity:** HIGH

**Description:** ### Impact

RestrictedPython rewrites sensitive operations to go through guard hooks. Attribute access becomes `_getattr_(obj, name)`, item access becomes `_getitem_(obj, key)`, writes go through `_write_`, and print goes through `_print_`. The embedding application supplies these hooks to enforce its policy.

Argument-name validation rejects these protected names for regular arguments, `*args`, `

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-55830

---
*Generated on 2026-08-29*