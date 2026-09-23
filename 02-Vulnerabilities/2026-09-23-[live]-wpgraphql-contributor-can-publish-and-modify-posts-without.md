# [LIVE] WPGraphQL: Contributor can publish and modify posts without 

**Severity:** MEDIUM

**Description:** ## Summary

WPGraphQL 2.19.0 contains an authorization bypass in the `updatePost` mutation. An authenticated WordPress Contributor can change one of their own draft posts to `PUBLISH` despite lacking the `publish_posts` capability. The same mutation also permits the Contributor to modify their own previously published posts despite lacking `edit_published_posts` and failing WordPress's object-leve

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-88974

---
*Generated on 2026-09-23*