# [LIVE] MLflow: Unauthenticated full-read SSRF in webhook delivery: 

**Severity:** CRITICAL

**Description:** ### Summary
The default MLflow Tracking Server (`mlflow server`, no authentication, default SQLite backend) exposes the model-registry webhooks API unauthenticated, including a synchronous `POST /api/2.0/mlflow/webhooks/{id}/test` endpoint that returns the upstream response status and body to the caller. The SSRF guard added in PR #20747 (`_validate_webhook_url`, shipped in 3.10.0) resolves the we

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-64849

---
*Generated on 2026-08-18*