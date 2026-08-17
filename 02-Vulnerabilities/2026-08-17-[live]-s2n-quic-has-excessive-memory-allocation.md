# [LIVE] s2n-quic has excessive memory allocation

**Severity:** MEDIUM

**Description:** s2n-quic is a Rust implementation of the QUIC protocol. An unauthenticated user can attempt to exhaust server memory on an s2n-quic endpoint by sending crafted CRYPTO frames with high offsets. The buffer used for processing CRYPTO frames does not enforce a maximum size. In the worst case, a single 1200-byte packet can cause approximately 9.4 MB of allocation. By repeatedly sending such packets, th

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-10740

---
*Generated on 2026-08-17*