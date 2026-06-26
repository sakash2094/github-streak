# Cross-Site Scripting (XSS)

**What it is:** Happens when an application includes untrusted data in web pages without proper escaping, allowing attackers to inject malicious JavaScript.

**Impact:** Session hijacking, credential theft, website defacement, malware distribution, and unauthorized actions on behalf of users.

**Prevention:** Sanitize and escape all user input before rendering. Use Content Security Policy (CSP) headers. Implement HTTP-only and Secure flags on cookies. Use modern frameworks that automatically escape output (React, Vue, Angular).

---
*Generated automatically on 2026-06-26 as part of the CyberSec Daily Streak project.*

**Category:** Vulnerabilities
**Security Status:** ✅ Content validated and sanitized
