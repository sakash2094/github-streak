# [LIVE] etcd: `tlsListener.acceptLoop` spawns unbounded handshake go

**Severity:** HIGH

**Description:** ### Impact
_What kind of vulnerability is it? Who is impacted?_

A network attacker who can reach an etcd TLS listener can open many TCP connections and never send a ClientHello. Each connection spawns a goroutine in the etcd server process that blocks indefinitely inside tls.Conn.Handshake(), and each is tracked in the pending map. Unbounded goroutine and map growth exhausts memory in the etcd pr

**Source:** GitHub Security Advisories
**CVE:** None

---
*Generated on 2026-07-26*