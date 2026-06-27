#!/usr/bin/env python3
"""
CyberSec Daily Generator - Simple 3-Folder System
"""

import json
import os
import re
import datetime
import random
import urllib.request

# --- SECURITY SANITIZATION ---
def sanitize_text(text):
    if not text or not isinstance(text, str):
        return ""
    text = text.replace('\x00', '')
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
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

# --- CONTENT DATABASE ---
TIPS = [
    {
        "title": "Password Hygiene Best Practices",
        "content": "Never reuse passwords across different sites. Use a password manager like Bitwarden or 1Password to generate and store complex, unique passwords for every account.\n\n**Best Practices:**\n- Use at least 16 characters\n- Mix uppercase, lowercase, numbers, and symbols\n- Enable breach monitoring\n- Change passwords immediately if a service is breached"
    },
    {
        "title": "Multi-Factor Authentication (MFA)",
        "content": "Enable MFA on all critical accounts. Use an authenticator app or hardware key instead of SMS.\n\n**Why MFA Matters:**\n- Adds an extra layer of security\n- Prevents 99.9% of automated attacks\n- Even if password is stolen, account remains secure\n\n**Recommended Methods:**\n1. Hardware keys (YubiKey)\n2. Authenticator apps (Google Authenticator, Authy)\n3. Avoid SMS when possible"
    },
    {
        "title": "Phishing Attack Recognition",
        "content": "Always verify sender email addresses and hover over links before clicking.\n\n**Red Flags:**\n- Urgent language (Account Suspended, Immediate Action Required)\n- Spelling and grammar errors\n- Mismatched URLs\n- Suspicious sender domains\n- Requests for sensitive information\n\n**What to Do:**\n- Verify through official channels\n- Never click suspicious links\n- Report phishing attempts"
    }
]

VULNS = [
    {
        "title": "SQL Injection (SQLi)",
        "content": "Occurs when untrusted user input is concatenated into database queries.\n\n**Impact:**\n- Data theft\n- Data modification\n- Authentication bypass\n- Remote code execution\n\n**Prevention:**\n- Use parameterized queries (prepared statements)\n- Implement input validation\n- Apply least privilege to database accounts\n- Use ORM frameworks\n\n**Example:**\n```python\n# Vulnerable\ncursor.execute(f\"SELECT * FROM users WHERE id = {user_id}\")\n\n# Safe\ncursor.execute(\"SELECT * FROM users WHERE id = %s\", (user_id,))\n```"
    },
    {
        "title": "Cross-Site Scripting (XSS)",
        "content": "Happens when untrusted data is included in web pages without proper escaping.\n\n**Types:**\n1. Reflected XSS - Malicious script reflected in error messages\n2. Stored XSS - Script stored in database\n3. DOM-based XSS - Client-side script execution\n\n**Prevention:**\n- Escape all user input\n- Use Content Security Policy (CSP)\n- Implement HTTP-only cookies\n- Use modern frameworks that auto-escape output"
    },
    {
        "title": "Broken Authentication",
        "content": "Flaws in authentication allowing attackers to compromise credentials.\n\n**Common Issues:**\n- Weak password policies\n- No rate limiting\n- Session fixation\n- Exposed session IDs\n\n**Prevention:**\n- Implement MFA\n- Enforce strong passwords\n- Account lockout after failed attempts\n- Secure session management\n- Rotate session IDs after login"
    }
]

TOOLS = [
    {
        "title": "Nmap (Network Mapper)",
        "content": "Industry-standard network discovery and security auditing tool.\n\n**Essential Commands:**\n```bash\n# Basic scan\nnmap 192.168.1.1\n\n# Service version detection\nnmap -sV 192.168.1.1\n\n# Aggressive scan\nnmap -A 192.168.1.1\n\n# All ports\nnmap -p- 192.168.1.1\n\n# Save output\nnmap -oN scan.txt 192.168.1.1\n```\n\n**Use Cases:**\n- Network inventory\n- Service version detection\n- Security auditing\n- Port scanning"
    },
    {
        "title": "Wireshark",
        "content": "Network protocol analyzer for capturing and browsing network traffic.\n\n**Basic Usage:**\n```bash\n# Capture on interface\nsudo wireshark -i eth0\n\n# Command-line capture\ntshark -i eth0 -w capture.pcap\n\n# Filter by IP\ntshark -r capture.pcap -Y \"ip.addr == 192.168.1.1\"\n\n# Filter by protocol\ntshark -r capture.pcap -Y \"http or dns\"\n```\n\n**Use Cases:**\n- Network troubleshooting\n- Malware analysis\n- Protocol analysis\n- Security auditing"
    },
    {
        "title": "Burp Suite",
        "content": "Integrated platform for web application security testing.\n\n**Key Features:**\n- Intercepting proxy\n- Vulnerability scanner\n- Repeater for manual testing\n- Intruder for automated attacks\n\n**Getting Started:**\n1. Configure browser proxy to 127.0.0.1:8080\n2. Install Burp CA certificate\n3. Intercept requests in Proxy tab\n4. Send to Repeater for testing\n5. Use Intruder for automation"
    }
]

# --- FETCH LIVE ADVISORIES ---
def fetch_live_advisories():
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
                desc = sanitize_text(adv.get('description', 'No description.')[:400])
                
                live_vulns.append({
                    "title": f"[LIVE] {summary[:60]}",
                    "content": f"**Severity:** {severity}\n\n**Description:** {desc}\n\n**Source:** GitHub Security Advisories\n**CVE:** {adv.get('cve_id', 'N/A')}"
                })
            print(f"✅ Fetched {len(live_vulns)} live advisories!")
            return live_vulns
    except Exception as e:
        print(f"⚠️ API fetch failed: {e}")
        return []

# --- MAIN LOGIC ---
def main():
    try:
        today = datetime.datetime.now()
        date_str = today.strftime("%Y-%m-%d")
        
        print(f"🛡️ CyberSec Generator - {date_str}")
        print("=" * 50)
        
        # Fetch live advisories and mix with local vulns
        live_vulns = fetch_live_advisories()
        all_vulns = VULNS + live_vulns
        
        # Random selection
        category = random.choice(['tips', 'vulns', 'tools'])
        
        if category == 'tips':
            item = random.choice(TIPS)
            folder = "01-Security-Tips"
        elif category == 'vulns':
            item = random.choice(all_vulns)
            folder = "02-Vulnerabilities"
        else:
            item = random.choice(TOOLS)
            folder = "03-Tools"
        
        print(f"📝 Topic: {item['title']}")
        
        # Create file
        os.makedirs(folder, exist_ok=True)
        safe_title = validate_filename(item['title'])
        filename = f"{date_str}-{safe_title}.md"
        filepath = os.path.join(folder, filename)
        
        content = f"# {item['title']}\n\n{item['content']}\n\n---\n*Generated on {date_str}*"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created: {filepath}")
        
        # Update dashboard data
        json_file = 'dashboard_data.json'
        if os.path.exists(json_file):
            try:
                with open(json_file, 'r') as f:
                    data = json.load(f)
            except:
                data = {'dates': [], 'latest_content': {}}
        else:
            data = {'dates': [], 'latest_content': {}}
        
        if date_str not in data['dates']:
            data['dates'].append(date_str)
            data['dates'].sort()
        
        # Calculate streak
        dates_set = set(data['dates'])
        current_streak = 0
        check_date = datetime.datetime.now()
        while check_date.strftime("%Y-%m-%d") in dates_set:
            current_streak += 1
            check_date -= datetime.timedelta(days=1)
        
        data['current_streak'] = current_streak
        data['total_contributions'] = len(data['dates'])
        data['latest_content'] = {
            'title': item['title'],
            'category': folder,
            'content': item['content'][:200],
            'date': date_str
        }
        
        with open(json_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"🔥 Streak: {current_streak} days")
        print("✅ Done!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()
