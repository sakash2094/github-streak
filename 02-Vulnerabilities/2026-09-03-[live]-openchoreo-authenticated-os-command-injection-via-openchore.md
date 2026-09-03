# [LIVE] OpenChoreo: Authenticated OS command injection via OpenChore

**Severity:** HIGH

**Description:** ### Summary
OpenChoreo Workflow Plane templates were vulnerable to OS command injection because some developer-controlled workflow parameters were interpolated directly into shell program text executed through sh -c.

An authenticated user with permission to configure and trigger an affected workflow could supply crafted parameter values containing shell metacharacters. Because Argo substituted th

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-73667

---
*Generated on 2026-09-03*