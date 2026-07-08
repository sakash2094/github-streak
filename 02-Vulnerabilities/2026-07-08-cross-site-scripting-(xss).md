# Cross-Site Scripting (XSS)

Happens when untrusted data is included in web pages without proper escaping.

**Types:**
1. Reflected XSS - Malicious script reflected in error messages
2. Stored XSS - Script stored in database
3. DOM-based XSS - Client-side script execution

**Prevention:**
- Escape all user input
- Use Content Security Policy (CSP)
- Implement HTTP-only cookies
- Use modern frameworks that auto-escape output

---
*Generated on 2026-07-08*