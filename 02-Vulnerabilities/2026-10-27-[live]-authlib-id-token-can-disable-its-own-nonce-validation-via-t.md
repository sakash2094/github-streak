# [LIVE] Authlib: ID token can disable its own nonce validation via t

**Severity:** MEDIUM

**Description:** ### Summary

`OpenIDMixin.parse_id_token()` reads the `nonce_supported` claim from the ID token it is validating. When that claim is boolean `false`, the expected nonce is set to `None` and nonce validation is skipped for that token.

An ID token that carries this claim is therefore accepted in a session whose nonce does not match. A captured, validly signed ID token belonging to a victim can be r

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-114617

---
*Generated on 2026-10-27*