# Wireshark

Network protocol analyzer for capturing and browsing network traffic.

**Basic Usage:**
```bash
# Capture on interface
sudo wireshark -i eth0

# Command-line capture
tshark -i eth0 -w capture.pcap

# Filter by IP
tshark -r capture.pcap -Y "ip.addr == 192.168.1.1"

# Filter by protocol
tshark -r capture.pcap -Y "http or dns"
```

**Use Cases:**
- Network troubleshooting
- Malware analysis
- Protocol analysis
- Security auditing

---
*Generated on 2026-07-16*