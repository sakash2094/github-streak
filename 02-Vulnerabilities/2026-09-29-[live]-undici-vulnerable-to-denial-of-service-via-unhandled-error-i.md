# [LIVE] undici vulnerable to Denial of Service via unhandled error i

**Severity:** MEDIUM

**Description:** ## Impact

undici's WebSocket client (including Node.js's bundled `globalThis.WebSocket`) crashes the entire Node.js process when a remote WebSocket peer sends a permessage-deflate compressed message that crosses the decompressed-payload size limit and then contains a malformed DEFLATE block. In `lib/web/websocket/permessage-deflate.js`, the size-limit cleanup calls `removeAllListeners()` on the i

**Source:** GitHub Security Advisories
**CVE:** CVE-2026-85024

---
*Generated on 2026-09-29*