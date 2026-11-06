# [LIVE] filecoin-pin: Unbounded DAG pinning can exhaust server resou

**Severity:** MEDIUM

**Description:** ## Summary

The IPFS Pinning Service API implementation accepts a caller-controlled CID through `POST /pins`, queues background processing, and then recursively fetches the full DAG with `helia.pins.add(cid)`. The route and background pinning path do not enforce a request rate limit, per-user quota, maximum DAG byte count, maximum block count, traversal timeout, or concurrent pinning limit.

An au

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-62300

---
*Generated on 2026-11-06*