#!/usr/bin/env python3
"""
CyberSec Daily Portfolio Generator (Phase 1 - Professional Edition)
Themed daily content with organized folder structure and auto-updating README.
"""

import json
import os
import re
import datetime
import random
import html
import urllib.request

# --- 1. SECURITY SANITIZATION ---
def sanitize_text(text):
    if not text or not isinstance(text, str): 
        return ""
    text = text.replace('\x00', '')
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*on\w+\s*=\s*["\'][^"\']*["\']', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\.\./', '', text)
    return text.strip()[:5000]

def validate_filename(name):
    if not name: 
        return "untitled"
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\.\./', '', name)
    if len(name) > 100: 
        name = name[:100]
    return name.lower().strip().replace(' ', '-')

# --- 2. THEMED DAY SCHEDULING ---
def get_today_theme():
    """Returns the theme for today based on day of week."""
    day_of_week = datetime.datetime.now().weekday()  # 0=Monday, 6=Sunday
    
    themes = {
        0: {"name": "Networking", "folder": "04-Networking", "icon": "🌐", "category": "networking"},
        1: {"name": "Web Security", "folder": "05-Web-Security", "icon": "🕸️", "category": "web-security"},
        2: {"name": "Malware Analysis", "folder": "06-Malware-Analysis", "icon": "🦠", "category": "malware"},
        3: {"name": "Digital Forensics", "folder": "07-Forensics", "icon": "🔍", "category": "forensics"},
        4: {"name": "Python Automation", "folder": "08-Python", "icon": "🐍", "category": "python"},
        5: {"name": "CTF Challenges", "folder": "09-CTF", "icon": "🏆", "category": "ctf"},
        6: {"name": "Weekly News", "folder": "10-News", "icon": "📰", "category": "news"}
    }
    
    return themes[day_of_week]

# --- 3. EXPANDED CONTENT DATABASE ---
NETWORKING = [
    {
        "title": "DNS Cache Poisoning", 
        "content": "**What it is:** Attackers inject fake DNS records into a resolver's cache, redirecting users to malicious sites.\n\n**Attack Process:**\n1. Identify target DNS server\n2. Send forged DNS responses with incorrect IP mappings\n3. Wait for cache to be poisoned\n4. Victims are redirected to attacker-controlled sites\n\n**Mitigation:** Use DNSSEC, disable open recursion, implement source port randomization.\n\n**Commands:**\n```bash\n# Check DNS cache\nipconfig /displaydns  # Windows\nsudo systemd-resolve --statistics  # Linux\n\n# Flush DNS cache\nipconfig /flushdns  # Windows\nsudo systemd-resolve --flush-caches  # Linux\n```"
    },
    {
        "title": "TCP/IP Protocol Stack", 
        "content": "**Overview:** The foundation of internet communication.\n\n**Layers:**\n- **Application:** HTTP, FTP, SMTP\n- **Transport:** TCP (reliable), UDP (fast)\n- **Internet:** IP addressing and routing\n- **Network Access:** Ethernet, Wi-Fi\n\n**Key Commands:**\n```bash\n# View routing table\nnetstat -r\n\n# Trace packet path\ntraceroute example.com\n\n# Capture packets\ntcpdump -i eth0\n\n# Check open ports\nnetstat -tuln\n```"
    },
    {
        "title": "Network Segmentation", 
        "content": "**What it is:** Dividing a network into smaller subnets to limit lateral movement.\n\n**Benefits:**\n- Contains breaches to single segment\n- Reduces attack surface\n- Improves performance\n- Simplifies access control\n\n**Implementation:** Use VLANs, firewalls, and microsegmentation. Apply Zero Trust principles.\n\n**Example:**\n```bash\n# Create VLAN\nvconfig add eth0 10\n\n# Assign IP\nifconfig eth0.10 192.168.10.1/24 up\n```"
    }
]

WEB_SECURITY = [
    {
        "title": "Cross-Site Request Forgery (CSRF)", 
        "content": "**What it is:** Attacker tricks authenticated user into performing unwanted actions.\n\n**Attack Example:**\n```html\n<img src=\"http://bank.com/transfer?to=attacker&amount=1000\">\n```\n\n**Prevention:**\n- Use anti-CSRF tokens\n- Implement SameSite cookie attribute\n- Verify Origin/Referer headers\n- Require re-authentication for sensitive actions\n\n**Testing:**\n```bash\n# Check for CSRF tokens\ncurl -X POST https://target.com/transfer \\\n  -H \"Cookie: session=abc123\" \\\n  -d \"to=attacker&amount=1000\"\n```"
    },
    {
        "title": "HTTP Security Headers", 
        "content": "**Essential Headers:**\n\n```http\nContent-Security-Policy: default-src 'self'\nX-Frame-Options: DENY\nX-Content-Type-Options: nosniff\nStrict-Transport-Security: max-age=31536000\nX-XSS-Protection: 1; mode=block\nReferrer-Policy: strict-origin-when-cross-origin\n```\n\n**Implementation (Nginx):**\n```nginx\nadd_header Content-Security-Policy \"default-src 'self'\";\nadd_header X-Frame-Options \"DENY\";\nadd_header X-Content-Type-Options \"nosniff\";\n```"
    },
    {
        "title": "SQL Injection Deep Dive", 
        "content": "**Types:**\n1. **In-band:** UNION-based, Error-based\n2. **Blind:** Boolean-based, Time-based\n3. **Out-of-band:** DNS/HTTP exfiltration\n\n**Detection:**\n```sql\n' OR '1'='1\n' UNION SELECT NULL--\n' AND SLEEP(5)--\n```\n\n**Prevention:**\n- Use parameterized queries\n- Implement input validation\n- Apply least privilege to DB accounts\n- Use ORM frameworks\n\n**Example (Python):**\n```python\n# ❌ VULNERABLE\ncursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")\n\n# ✅ SAFE\ncursor.execute(\"SELECT * FROM users WHERE id = %s\", (user_id,))\n```"
    }
]

MALWARE = [
    {
        "title": "Ransomware Analysis Basics", 
        "content": "**Static Analysis:**\n```bash\n# Check file type\nfile malware.exe\n\n# Extract strings\nstrings malware.exe | grep -i \"bitcoin\"\n\n# Check imports\nobjdump -p malware.exe | grep DLL\n\n# Calculate hash\nsha256sum malware.exe\n```\n\n**Dynamic Analysis:**\n- Run in isolated VM (REMnux, FLARE VM)\n- Monitor network traffic with Wireshark\n- Track file system changes with Process Monitor\n- Analyze registry modifications\n\n**Indicators:** Encryption routines, C2 communication, ransom notes"
    },
    {
        "title": "YARA Rules for Malware Detection", 
        "content": "**What is YARA:** Pattern matching tool for malware identification.\n\n**Example Rule:**\n```yara\nrule Suspicious_PowerShell {\n    meta:\n        description = \"Detects encoded PowerShell\"\n        author = \"CyberSec Daily\"\n    strings:\n        $ps1 = \"powershell\" nocase\n        $encoded = \"-enc\" nocase\n        $b64 = /[A-Za-z0-9+\\/]{50,}={0,2}/\n    condition:\n        $ps1 and $encoded and $b64\n}\n```\n\n**Usage:**\n```bash\nyara rule.yar suspicious_file.exe\n\n# Scan directory\nyara -r rule.yar /path/to/files\n```"
    },
    {
        "title": "Memory Forensics with Volatility", 
        "content": "**Basic Commands:**\n```bash\n# Identify OS profile\nvolatility -f memory.dmp imageinfo\n\n# List processes\nvolatility -f memory.dmp --profile=Win10x64 pslist\n\n# Check network connections\nvolatility -f memory.dmp --profile=Win10x64 netscan\n\n# Dump suspicious process\nvolatility -f memory.dmp --profile=Win10x64 procdump -p 1234 -D output/\n\n# Scan for malware\nvolatility -f memory.dmp --profile=Win10x64 malfind\n```\n\n**What to look for:** Injected code, hidden processes, unusual network connections"
    }
]

FORENSICS = [
    {
        "title": "File Carving with Foremost", 
        "content": "**What it is:** Extracting files from disk images based on headers/footers.\n\n**Usage:**\n```bash\n# Carve all file types\nforemost -i disk.img -o output/\n\n# Carve specific types\nforemost -i disk.img -t jpg,pdf,doc -o output/\n\n# Verbose mode\nforemost -i disk.img -v -o output/\n```\n\n**Supported formats:** jpg, gif, png, bmp, pdf, doc, zip, exe, and 20+ more\n\n**Alternative Tools:**\n- PhotoRec (more file types)\n- Scalpel (faster)\n- Autopsy (GUI)"
    },
    {
        "title": "Timeline Analysis", 
        "content": "**Creating a Timeline:**\n```bash\n# Extract file system metadata\nfls -r -m C:/ disk.img > bodyfile\n\n# Create timeline\nmactime -b bodyfile -y 2024-01-01 > timeline.csv\n\n# Filter by date range\ngrep \"2024-01-15\" timeline.csv\n\n# View in text format\nmactime -b bodyfile -d\n```\n\n**What to analyze:**\n- File creation/modification times\n- Registry key changes\n- Log file timestamps
- Browser history entries"
    },
    {
        "title": "Log Analysis Essentials", 
        "content": "**Windows Event Logs:**\n```powershell\n# Failed logons\nGet-WinEvent -FilterHashtable @{LogName='Security';Id=4625}\n\n# Privilege escalation\nGet-WinEvent -FilterHashtable @{LogName='Security';Id=4672}\n\n# Process creation\nGet-WinEvent -FilterHashtable @{LogName='Security';Id=4688}\n```\n\n**Linux Logs:**\n```bash\n# Search auth logs\ngrep \"Failed password\" /var/log/auth.log\n\n# Find sudo usage\ngrep sudo /var/log/auth.log\n\n# Check SSH logins\ngrep \"Accepted\" /var/log/auth.log\n\n# View syslog\ntail -f /var/log/syslog\n```"
    }
]

PYTHON = [
    {
        "title": "Port Scanner in Python", 
        "content": "**Simple Port Scanner:**\n```python\nimport socket\n\ndef scan_port(host, port):\n    try:\n        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\n        sock.settimeout(1)\n        result = sock.connect_ex((host, port))\n        sock.close()\n        return result == 0\n    except:\n        return False\n\n# Scan common ports\nports = [21, 22, 23, 80, 443, 3389]\nfor port in ports:\n    if scan_port('192.168.1.1', port):\n        print(f'Port {port}: OPEN')\n```\n\n**Usage:** `python port_scanner.py`"
    },
    {
        "title": "Network Packet Sniffer", 
        "content": "**Basic Packet Capture:**\n```python\nfrom scapy.all import *\n\ndef packet_callback(packet):\n    if packet.haslayer(TCP):\n        print(f\"{packet[IP].src} -> {packet[IP].dst}:{packet[TCP].dport}\")\n\n# Capture 100 packets\nsniff(prn=packet_callback, count=100)\n\n# Save to file\nsniff(count=100).wrpcap('capture.pcap')\n```\n\n**Requires:** `pip install scapy` and root/admin privileges\n\n**Advanced:**\n```python\n# Filter HTTP traffic\nsniff(filter=\"tcp port 80\", prn=packet_callback, count=50)\n```"
    },
    {
        "title": "Hash Cracker with Dictionary", 
        "content": "**MD5 Cracker:**\n```python\nimport hashlib\n\ndef crack_md5(hash_to_crack, wordlist):\n    with open(wordlist, 'r') as f:
        for word in f:
            word = word.strip()
            word_hash = hashlib.md5(word.encode()).hexdigest()
            if word_hash == hash_to_crack:
                return word
    return None\n\n# Usage\nresult = crack_md5('5f4dcc3b5aa765d61d8327deb882cf99', 'rockyou.txt')\nprint(f'Password: {result}')  # Output: password\n```\n\n**Supports:** MD5, SHA1, SHA256 (change hashlib function)"
    }
]

CTF = [
    {
        "title": "CTF Enumeration Checklist", 
        "content": "**Web Challenges:**\n- [ ] Check robots.txt\n- [ ] View page source\n- [ ] Inspect HTTP headers\n- [ ] Check for hidden directories (/admin, /backup)\n- [ ] Test for SQLi, XSS, LFI\n- [ ] Check cookies and local storage\n- [ ] Use Dirb/Dirbuster/Gobuster\n\n**Binary Challenges:**\n- [ ] Run `strings` command\n- [ ] Check with `file` command\n- [ ] Open in Ghidra/IDA\n- [ ] Look for hardcoded flags\n- [ ] Check for buffer overflows\n\n**Crypto Challenges:**\n- [ ] Identify encoding (Base64, Hex, ROT13)\n- [ ] Check for weak algorithms\n- [ ] Look for padding oracle attacks"
    },
    {
        "title": "Base64 Encoding/Decoding", 
        "content": "**Common in CTFs:**\n\n```bash\n# Encode\necho \"flag{secret}\" | base64\n\n# Decode\necho \"ZmxhZ3tzZWNyZXR9\" | base64 -d\n\n# Multiple encodings\necho \"flag{nested}\" | base64 | base64 | base64\n\n# Decode multiple times\ncat encoded.txt | base64 -d | base64 -d | base64 -d\n```\n\n**Python:**\n```python\nimport base64\n\n# Encode\nencoded = base64.b64encode(b\"flag{secret}\")\n\n# Decode\ndecoded = base64.b64decode(\"ZmxhZ3tzZWNyZXR9\")\n```"
    },
    {
        "title": "Nmap for CTFs", 
        "content": "**Essential Scans:**\n\n```bash\n# Quick scan\nnmap -F 192.168.1.1\n\n# Service version detection\nnmap -sV 192.168.1.1\n\n# Aggressive scan\nnmap -A 192.168.1.1\n\n# All ports\nnmap -p- 192.168.1.1\n\n# UDP scan\nnmap -sU 192.168.1.1\n\n# Script scan\nnmap -sC 192.168.1.1\n\n# Vulnerability scan\nnmap --script vuln 192.168.1.1\n\n# Save output\nnmap -oN scan.txt 192.168.1.1\n```"
    }
]

NEWS = [
    {
        "title": "Latest CVE Highlights", 
        "content": "**This Week's Critical Vulnerabilities:**\n\n*Note: This will be auto-populated from GitHub Advisories API*\n\nCheck the `02-Vulnerabilities` folder for detailed analysis of:\n- Recent CVEs\n- Exploit availability\n- Mitigation strategies\n\n**Stay Updated:**\n- Follow CISA Known Exploited Vulnerabilities catalog\n- Monitor GitHub Security Advisories\n- Subscribe to vendor security bulletins"
    }
]

# --- 4. FETCH LIVE ADVISORIES ---
def fetch_live_advisories():
    """Fetches real vulnerabilities from GitHub Security Advisories API."""
    try:
        url = "https://api.github.com/advisories?per_page=3&type=reviewed"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0', 
            'Accept': 'application/vnd.github+json'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            live_vulns = []
            for adv in data:
                severity = adv.get('severity', 'unknown').upper()
                summary = sanitize_text(adv.get('summary', 'Security Advisory'))
                desc = sanitize_text(adv.get('description', 'No description available.')[:500])
                
                live_vulns.append({
                    "title": f"[LIVE] {summary[:80]}",
                    "content": f"**Severity:** {severity}\n\n**Description:** {desc}\n\n**Source:** GitHub Security Advisories\n**Published:** {adv.get('published_at', 'Recently')}\n\n**CVE:** {adv.get('cve_id', 'N/A')}"
                })
            print(f"✅ Successfully fetched {len(live_vulns)} live advisories!")
            return live_vulns
    except Exception as e:
        print(f"⚠️ API fetch failed ({e}). Using local database.")
        return []

# --- 5. MAIN GENERATION LOGIC ---
def get_content_for_theme(theme):
    """Returns appropriate content based on today's theme."""
    category = theme["category"]
    
    content_map = {
        "networking": NETWORKING,
        "web-security": WEB_SECURITY,
        "malware": MALWARE,
        "forensics": FORENSICS,
        "python": PYTHON,
        "ctf": CTF,
        "news": NEWS
    }
    
    # For news day, also fetch live advisories
    if category == "news":
        live_vulns = fetch_live_advisories()
        return live_vulns if live_vulns else NEWS
    
    return content_map.get(category, NETWORKING)

def create_markdown_file(theme, item, date_str):
    """Creates a markdown file with proper folder structure."""
    folder = theme["folder"]
    safe_title = validate_filename(item['title'])
    filename = f"{date_str}-{safe_title}.md"
    
    os.makedirs(folder, exist_ok=True)
    
    # Add theme icon and category
    markdown_content = f"""# {theme['icon']} {item['title']}

**Category:** {theme['name']}  
**Date:** {date_str}  
**Day of Week:** {datetime.datetime.now().strftime('%A')}

---

{item['content']}

---

*Generated automatically as part of the CyberSec Daily Portfolio project.*

**Topics Covered:** #{theme['name'].replace(' ', '')} #CyberSecurity #DailyLearning
"""
    
    filepath = os.path.join(folder, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return filepath

def update_dashboard_data(theme, item, date_str):
    """Updates the JSON dashboard data file."""
    json_file = 'dashboard_data.json'
    
    # Load existing data or create new
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {'dates': [], 'latest_content': {}, 'topics': {}}
    else:
        data = {'dates': [], 'latest_content': {}, 'topics': {}}
    
    # Ensure required fields exist
    if 'dates' not in data: data['dates'] = []
    if 'topics' not in data: data['topics'] = {}
    
    # Add today's date if not already present
    if date_str not in data['dates']:
        data['dates'].append(date_str)
        data['dates'].sort()
    
    # Track topic coverage
    topic = theme['category']
    if topic not in data['topics']:
        data['topics'][topic] = 0
    data['topics'][topic] += 1
    
    # Calculate streaks
    dates_set = set(data['dates'])
    current_streak = 0
    check_date = datetime.datetime.now()
    while check_date.strftime("%Y-%m-%d") in dates_set:
        current_streak += 1
        check_date -= datetime.timedelta(days=1)
    
    # Longest streak
    sorted_dates = sorted(data['dates'])
    longest_streak = 0
    if sorted_dates:
        temp_streak = 1
        longest_streak = 1
        for i in range(1, len(sorted_dates)):
            prev_date = datetime.datetime.strptime(sorted_dates[i-1], "%Y-%m-%d")
            curr_date = datetime.datetime.strptime(sorted_dates[i], "%Y-%m-%d")
            if (curr_date - prev_date).days == 1:
                temp_streak += 1
                longest_streak = max(longest_streak, temp_streak)
            else:
                temp_streak = 1
    
    # Update latest content
    data['latest_content'] = {
        'title': sanitize_text(item['title']),
        'category': theme['name'],
        'icon': theme['icon'],
        'content': sanitize_text(item['content']),
        'date': date_str,
        'folder': theme['folder']
    }
    
    # Update stats
    data['current_streak'] = current_streak
    data['longest_streak'] = longest_streak
    data['total_contributions'] = len(data['dates'])
    data['last_updated'] = datetime.datetime.now().isoformat()
    
    # Write data securely
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False, sort_keys=True)
    
    return data

def update_readme(data):
    """Auto-updates the README with current stats."""
    readme_file = 'README.md'
    
    # Get topic breakdown
    topics_html = ""
    if 'topics' in data and data['topics']:
        topic_items = sorted(data['topics'].items(), key=lambda x: x[1], reverse=True)
        for topic, count in topic_items[:10]:  # Top 10 topics
            topic_formatted = topic.replace('-', ' ').title()
            topics_html += f"- {topic_formatted}: {count} posts\n"
    
    # Get latest articles
    latest_html = ""
    if 'latest_content' in data and data['latest_content']:
        latest = data['latest_content']
        latest_html = f"- **{latest['title']}** ({latest['category']})\n"
    
    # Create stats section
    stats_section = f"""
## 📊 Project Statistics

| Metric | Value |
|--------|-------|
| 🔥 Current Streak | {data.get('current_streak', 0)} days |
| 🏆 Longest Streak | {data.get('longest_streak', 0)} days |
| 📈 Total Posts | {data.get('total_contributions', 0)} |
| 📅 Last Updated | {data.get('last_updated', 'N/A')[:10]} |

### Topics Covered

{topics_html if topics_html else "- Content being generated..."}

### Latest Article

{latest_html if latest_html else "- No articles yet"}

---
"""
    
    # Try to update existing README or create new one
    try:
        if os.path.exists(readme_file):
            with open(readme_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace stats section if it exists
            if '## 📊 Project Statistics' in content:
                # Find and replace the stats section
                import re
                pattern = r'## 📊 Project Statistics.*?(?=## |\Z)'
                content = re.sub(pattern, stats_section, content, flags=re.DOTALL)
            else:
                # Append to end
                content += "\n" + stats_section
            
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            # Create basic README
            basic_readme = f"""# 🛡️ CyberSec Daily Portfolio

[![Daily CyberSec Streak & Deploy](https://github.com/sakash2094/github-streak/actions/workflows/daily-cybersec.yml/badge.svg)](https://github.com/sakash2094/github-streak/actions/workflows/daily-cybersec.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-222222?style=flat&logo=github)](https://sakash2094.github.io/github-streak/)

> An automated cybersecurity knowledge repository with themed daily content.

🔗 **Live Dashboard:** [https://sakash2094.github.io/github-streak/](https://sakash2094.github.io/github-streak/)

## 📅 Weekly Schedule

| Day | Theme | Focus |
|-----|-------|-------|
| Monday | 🌐 Networking | Protocols, Infrastructure, Attacks |
| Tuesday | 🕸️ Web Security | OWASP Top 10, Headers, CSRF |
| Wednesday | 🦠 Malware Analysis | Reverse Engineering, YARA, Ransomware |
| Thursday | 🔍 Digital Forensics | Timeline Analysis, Log Analysis |
| Friday | 🐍 Python Automation | Security Tools, Scripts |
| Saturday | 🏆 CTF Challenges | Write-ups, Techniques |
| Sunday | 📰 Weekly News | CVE Highlights, Threat Intel |

{stats_section}
## 🚀 How It Works

This repository uses GitHub Actions to automatically generate and publish cybersecurity content every day at 10:00 AM UTC.

- **Themed Days:** Each day focuses on a different cybersecurity domain
- **Live Data:** Fetches real vulnerabilities from GitHub Security Advisories
- **Auto-Deploy:** Updates GitHub Pages dashboard automatically
- **Security-First:** All content is sanitized and validated

## 📂 Repository Structure
github-streak/
├── 01-Security-Tips/ # General security tips
├── 02-Vulnerabilities/ # Vulnerability analysis
├── 03-Tools/ # Security tools tutorials
├── 04-Networking/ # Network security
├── 05-Web-Security/ # Web application security
├── 06-Malware-Analysis/ # Malware reverse engineering
├── 07-Forensics/ # Digital forensics
├── 08-Python/ # Python security scripts
├── 09-CTF/ # CTF challenges & writeups
└── 10-News/ # Weekly security news

---

<p align="center">Made with ❤️ for cybersecurity education</p>
"""
            with open(readme_file, 'w', encoding='utf-8') as f:
                f.write(basic_readme)
        
        print("✅ README updated successfully!")
    except Exception as e:
        print(f"⚠️ Could not update README: {e}")

def main():
    """Main execution function."""
    try:
        today = datetime.datetime.now()
        date_str = today.strftime("%Y-%m-%d")
        
        print(f"🛡️  CyberSec Portfolio Generator - {date_str}")
        print("=" * 60)
        
        # Get today's theme
        theme = get_today_theme()
        print(f"📅 Today's Theme: {theme['icon']} {theme['name']}")
        
        # Get content for today's theme
        content_list = get_content_for_theme(theme)
        item = random.choice(content_list)
        
        print(f"📝 Topic: {item['title']}")
        
        # Create markdown file
        filepath = create_markdown_file(theme, item, date_str)
        print(f"✅ Created: {filepath}")
        
        # Update dashboard data
        data = update_dashboard_data(theme, item, date_str)
        print(f"📊 Dashboard data updated")
        print(f"🔥 Current streak: {data['current_streak']} days")
        print(f"🏆 Longest streak: {data['longest_streak']} days")
        print(f"📈 Total contributions: {data['total_contributions']}")
        
        # Update README
        update_readme(data)
        
        print("=" * 60)
        print("✅ Portfolio generation completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
