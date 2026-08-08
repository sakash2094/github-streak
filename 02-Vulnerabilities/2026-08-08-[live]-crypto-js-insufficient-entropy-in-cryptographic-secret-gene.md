# [LIVE] crypto-js: Insufficient Entropy in Cryptographic Secret Gene

**Severity:** CRITICAL

**Description:** ### Summary

`CryptoJS.lib.WordArray.random()` in affected versions is not a cryptographically secure random number generator. Nominal requests for 128 or 256 bits of entropy produce effective search spaces of approximately 2^39 and 2^47 possibilities — small enough to enumerate on commodity hardware.

Coinspect's [Ill Bloom](https://www.coinspect.com/blog/ill-bloom-investigation/) investigation c

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-71851

---
*Generated on 2026-08-08*