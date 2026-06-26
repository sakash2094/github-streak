#!/usr/bin/env python3
"""
Daily Cybersecurity Content Generator
Securely generates daily security tips, vulnerability spotlights, and tool guides.
Includes input sanitization and output validation.
"""

import json
import os
import re
import datetime
import random
import html

# --- 1. SECURITY SANITIZATION FUNCTIONS ---

def sanitize_text(text):
    """
    Remove potentially dangerous content from text.
    Prevents XSS, path traversal, and injection attacks.
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove script tags and event handlers
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<iframe[^>]*>.*?</iframe>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<object[^>]*>.*?</object>', '', text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r'<embed[^>]*>', '', text, flags=re.IGNORECASE)
    
    # Remove javascript: and data: URIs
    text = re.sub(r'javascript:', '', text, flags=re.IGNORECASE)
    text = re.sub(r'data:text/html', '', text, flags=re.IGNORECASE)
    text = re.sub(r'vbscript:', '', text, flags=re.IGNORECASE)
    
    # Remove event handlers (onclick, onerror, onload, etc.)
    text = re.sub(r'\s*on\w+\s*=\s*["\'][^"\']*["\']', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s*on\w+\s*=[^\s>]+', '', text, flags=re.IGNORECASE)
    
    # Remove path traversal attempts
    text = re.sub(r'\.\./', '', text)
    text = re.sub(r'\.\.\\', '', text)
    
    # Limit length to prevent DoS
    if len(text) > 5000:
        text = text[:5000]
    
    return text.strip()

def validate_filename(name):
    """Ensure filename is safe and doesn't contain path traversal or special chars."""
    if not name:
        return "untitled"
    
    # Remove dangerous characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\.\./', '', name)
    name = re.sub(r'\.\.\\', '', name)
    name = name.replace('\x00', '')
    
    # Limit length
    if len(name) > 100:
        name = name[:100]
    
    # Convert to lowercase and replace spaces with hyphens
    name = name.lower().strip().replace(' ', '-')
    
    # Remove consecutive hyphens
    name = re.sub(r'-+', '-', name)
    
    return name if name else "content"

def escape_html(text):
    """Properly escape HTML special characters."""
    if not text:
        return ""
    return html.escape(str(text), quote=True)

# --- 2. CURATED CYBERSECURITY CONTENT DATABASE ---
# All content is pre-validated and sanitized

TIPS = [
    {
        "title": "Password Hygiene Best Practices",
        "content": "Never reuse passwords across different sites. Use a password manager like **Bitwarden** or **1Password** to generate and store complex, unique passwords (at least 16 characters) for every account. Enable breach monitoring to get alerts if your credentials appear in data breaches."
    },
    {
        "title": "Phishing Attack Recognition",
        "content": "Always verify the sender's email address carefully and hover over links before clicking. Attackers often use urgent language like 'Account Suspended' or 'Immediate Action Required' to bypass critical thinking. Check for spelling errors, mismatched URLs, and suspicious sender domains."
    },
    {
        "title": "Multi-Factor Authentication (MFA)",
        "content": "Enable MFA/2FA on all critical accounts (email, banking, GitHub). Use an authenticator app (**Google Authenticator**, **Authy**, **Microsoft Authenticator**) or hardware security key (**YubiKey**) instead of SMS, which is vulnerable to SIM swapping attacks."
    },
    {
        "title": "Software Update Management",
        "content": "Enable automatic updates for your operating system, browser, and all applications. Updates frequently contain patches for zero-day vulnerabilities that hackers actively exploit. Don't delay updates - many breaches exploit known vulnerabilities that were patched months ago."
    },
    {
        "title": "Secure Wi-Fi Practices",
        "content": "Use WPA3 encryption on your home router (or WPA2 if WPA3 unavailable). Change default router credentials immediately. Create a separate guest network for visitors. Never use public Wi-Fi for sensitive transactions without a VPN. Disable WPS as it has known security flaws."
    },
    {
        "title": "Data Backup Strategy",
        "content": "Follow the **3-2-1 backup rule**: Keep 3 copies of important data, on 2 different media types, with 1 copy stored offsite (cloud). Test your backups regularly by restoring files. Use encrypted backups and enable versioning to protect against ransomware."
    }
]

VULNS = [
    {
        "title": "SQL Injection (SQLi)",
        "content": "**What it is:** Occurs when untrusted user input is directly concatenated into database queries without proper sanitization.\n\n**Impact:** Attackers can read, modify, or delete database contents, execute administrative operations, or even issue commands to the operating system.\n\n**Prevention:** Always use parameterized queries (prepared statements) and ORMs. Never concatenate user input directly into SQL queries. Apply the principle of least privilege to database accounts. Use stored procedures with parameterized inputs."
    },
    {
        "title": "Cross-Site Scripting (XSS)",
        "content": "**What it is:** Happens when an application includes untrusted data in web pages without proper escaping, allowing attackers to inject malicious JavaScript.\n\n**Impact:** Session hijacking, credential theft, website defacement, malware distribution, and unauthorized actions on behalf of users.\n\n**Prevention:** Sanitize and escape all user input before rendering. Use Content Security Policy (CSP) headers. Implement HTTP-only and Secure flags on cookies. Use modern frameworks that automatically escape output (React, Vue, Angular)."
    },
    {
        "title": "Broken Authentication",
        "content": "**What it is:** Flaws in authentication and session management that allow attackers to compromise passwords, keys, or session tokens.\n\n**Impact:** Account takeover, unauthorized access to sensitive data, privilege escalation.\n\n**Prevention:** Implement multi-factor authentication. Enforce strong password policies (minimum 12 characters, complexity requirements). Implement account lockout after 5 failed attempts. Use secure session management with HTTP-only, Secure, and SameSite cookies. Rotate session IDs after login."
    },
    {
        "title": "Sensitive Data Exposure",
        "content": "**What it is:** Failure to protect sensitive data such as financial records, healthcare information, and credentials.\n\n**Impact:** Identity theft, credit card fraud, regulatory fines (GDPR, HIPAA), reputational damage.\n\n**Prevention:** Encrypt all sensitive data at rest (AES-256) and in transit (TLS 1.3). Use strong hashing algorithms like **bcrypt**, **scrypt**, or **Argon2** for passwords. Implement proper key management. Classify data and apply controls accordingly. Never store sensitive data in logs."
    },
    {
        "title": "Security Misconfiguration",
        "content": "**What it is:** Insecure default configurations, incomplete configurations, open cloud storage, misconfigured HTTP headers, and verbose error messages.\n\n**Impact:** Unauthorized access to systems, data leakage, complete system compromise.\n\n**Prevention:** Implement a repeatable hardening process. Remove or disable unnecessary features, frameworks, and services. Review and update configurations regularly. Automate configuration verification. Disable detailed error messages in production. Use security scanning tools."
    },
    {
        "title": "Insecure Direct Object References (IDOR)",
        "content": "**What it is:** Occurs when an application provides direct access to objects (database records, files) based on user-supplied input without authorization checks.\n\n**Impact:** Unauthorized access to other users' data, privacy violations, data theft.\n\n**Prevention:** Always verify that the logged-in user owns or has permission to access the requested resource. Use indirect reference maps (randomized IDs). Implement proper access control checks on every request. Never expose internal identifiers directly in URLs."
    }
]

TOOLS = [
    {
        "title": "Nmap (Network Mapper)",
        "content": "**Purpose:** Industry-standard network discovery and security auditing tool.\n\n**Key Features:**\n- Host discovery and port scanning\n- Service and version detection\n- Operating system fingerprinting\n- Scriptable interaction (NSE scripts)\n- Flexible output options\n\n**Essential Commands:**\n```bash\n# Basic scan\nnmap 192.168.1.1\n\n# Aggressive scan with version detection\nnmap -A -sV 192.168.1.1\n\n# Scan specific ports\nnmap -p 80,443,8080 target.com\n\n# Stealth SYN scan\nsudo nmap -sS target.com\n\n# Save output\nnmap -oN results.txt target.com\n```\n\n**Learn More:** [nmap.org](https://nmap.org)"
    },
    {
        "title": "Wireshark (Network Protocol Analyzer)",
        "content": "**Purpose:** World's foremost network protocol analyzer for capturing and interactively browsing network traffic.\n\n**Key Features:**\n- Deep inspection of hundreds of protocols\n- Live capture and offline analysis\n- Rich VoIP analysis\n- Decryption support for many protocols\n- Powerful display filters\n\n**Essential Commands:**\n```bash\n# Capture on specific interface\nsudo wireshark -i eth0\n\n# Command-line capture\ntshark -i eth0 -w capture.pcap\n\n# Filter by IP\ntshark -r capture.pcap -Y \"ip.addr == 192.168.1.1\"\n\n# Filter by protocol\ntshark -r capture.pcap -Y \"http or dns\"\n```\n\n**Learn More:** [wireshark.org](https://www.wireshark.org)"
    },
    {
        "title": "Burp Suite (Web Security Testing)",
        "content": "**Purpose:** Integrated platform for performing security testing of web applications.\n\n**Key Features:**\n- Intercepting proxy to examine/modify traffic\n- Automated vulnerability scanning (Professional)\n- Manual testing tools (Repeater, Intruder, Decoder)\n- Extensible with BApp Store plugins\n- Collaboration features\n\n**Getting Started:**\n```bash\n# Configure browser proxy to 127.0.0.1:8080\n# Install Burp CA certificate for HTTPS interception\n# Visit http://burpsuite in browser to download cert\n\n# Common workflow:\n# 1. Intercept requests in Proxy tab\n# 2. Send to Repeater for manual testing\n# 3. Use Intruder for automated attacks\n# 4. Run Scanner for automated vuln detection\n```\n\n**Learn More:** [portswigger.net/burp](https://portswigger.net/burp)"
    },
    {
        "title": "Metasploit Framework",
        "content": "**Purpose:** Most popular penetration testing framework with extensive exploit database.\n\n**Key Features:**\n- Large database of exploits and payloads\n- Modular architecture\n- Automated exploitation\n- Post-exploitation modules\n- Integration with Nmap, Nessus\n\n**Essential Commands:**\n```bash\n# Start Metasploit console\nmsfconsole\n\n# Search for exploits\nmsf6 > search type:exploit platform:windows\n\n# Use an exploit\nmsf6 > use exploit/windows/smb/ms17_010_eternalblue\n\n# Set options\nmsf6 exploit(ms17_010_eternalblue) > set RHOSTS 192.168.1.100\nmsf6 exploit(ms17_010_eternalblue) > set LHOST 192.168.1.50\n\n# Exploit\nmsf6 exploit(ms17_010_eternalblue) > exploit\n```\n\n**Learn More:** [metasploit.com](https://www.metasploit.com)"
    },
    {
        "title": "John the Ripper (Password Cracker)",
        "content": "**Purpose:** Fast, open-source password cracker for detecting weak passwords.\n\n**Key Features:**\n- Supports hundreds of hash types\n- Dictionary, brute force, and rule-based attacks\n- Auto-detection of hash types\n- Distributed cracking support\n- Highly optimized performance\n\n**Essential Commands:**\n```bash\n# Dictionary attack\njohn --wordlist=/usr/share/wordlists/rockyou.txt hashes.txt\n\n# Show cracked passwords\njohn --show hash.txt\n\n# Brute force with pattern\njohn --incremental hashes.txt\n\n# Generate password hash for testing\nopenssl passwd -1 test123 > hash.txt\n\n# Benchmark performance\njohn --test\n```\n\n**Learn More:** [openwall.com/john](https://www.openwall.com/john)"
    },
    {
        "title": "SQLMap (SQL Injection Tool)",
        "content": "**Purpose:** Automated tool for detecting and exploiting SQL injection flaws.\n\n**Key Features:**\n- Automatic detection of SQL injection types\n- Database fingerprinting\n- Data extraction from databases\n- OS command execution (with proper privileges)\n- Supports MySQL, PostgreSQL, Oracle, MS SQL\n\n**Essential Commands:**\n```bash\n# Basic test for SQL injection\nsqlmap -u \"http://example.com/page?id=1\"\n\n# Enumerate databases\nsqlmap -u \"http://example.com/page?id=1\" --dbs\n\n# Enumerate tables in specific database\nsqlmap -u \"http://example.com/page?id=1\" -D dbname --tables\n\n# Dump specific table\nsqlmap -u \"http://example.com/page?id=1\" -D dbname -T users --dump\n\n# OS shell (advanced)\nsqlmap -u \"http://example.com/page?id=1\" --os-shell\n```\n\n**Learn More:** [sqlmap.org](http://sqlmap.org)"
    }
]

# --- 3. CONTENT GENERATION LOGIC ---

def select_daily_content():
    """Randomly select content category and item."""
    categories = {
        'tips': TIPS,
        'vulnerabilities': VULNS,
        'tools': TOOLS
    }
    
    # Rotate through categories based on day of week for variety
    day_of_week = datetime.datetime.now().weekday()
    
    if day_of_week in [0, 3]:  # Monday, Thursday
        category = 'tips'
    elif day_of_week in [1, 4]:  # Tuesday, Friday
        category = 'vulnerabilities'
    else:  # Wednesday, Saturday, Sunday
        category = 'tools'
    
    # Select random item from chosen category
    selected = random.choice(categories[category])
    return category, selected

def create_markdown_file(category, item, date_str):
    """Create a sanitized markdown file with the content."""
    # Define folder names
    folders = {
        'tips': '01-Security-Tips',
        'vulnerabilities': '02-Vulnerabilities',
        'tools': '03-Tools'
    }
    
    folder = folders.get(category, '04-Content')
    
    # Sanitize and validate filename
    safe_title = validate_filename(item['title'])
    filename = f"{date_str}-{safe_title}.md"
    
    # Create directory if it doesn't exist
    os.makedirs(folder, exist_ok=True)
    
    # Sanitize content
    safe_title_display = sanitize_text(item['title'])
    safe_content = sanitize_text(item['content'])
    
    # Create markdown content
    markdown_content = f"""# {safe_title_display}

{safe_content}

---
*Generated automatically on {date_str} as part of the CyberSec Daily Streak project.*

**Category:** {category.title()}
**Security Status:** ✅ Content validated and sanitized
"""
    
    filepath = os.path.join(folder, filename)
    
    # Write file with UTF-8 encoding
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return filepath

def update_dashboard_data(category, item, date_str):
    """Update the JSON dashboard data file securely."""
    json_file = 'dashboard_data.json'
    
    # Load existing data or create new
    if os.path.exists(json_file):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError):
            data = {'dates': [], 'latest_content': {}}
    else:
        data = {'dates': [], 'latest_content': {}}
    
    # Ensure dates list exists
    if 'dates' not in data:
        data['dates'] = []
    
    # Add today's date if not already present
    if date_str not in data['dates']:
        data['dates'].append(date_str)
        data['dates'].sort()
    
    # Calculate streaks
    dates_set = set(data['dates'])
    
    # Current streak (consecutive days up to today)
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
    
    # Update latest content (sanitized)
    data['latest_content'] = {
        'title': sanitize_text(item['title']),
        'category': sanitize_text(category),
        'content': sanitize_text(item['content']),
        'date': date_str
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

def main():
    """Main execution function with error handling."""
    try:
        # Get today's date
        today = datetime.datetime.now()
        date_str = today.strftime("%Y-%m-%d")
        
        print(f"🛡️  CyberSec Daily Generator - {date_str}")
        print("=" * 50)
        
        # Select content
        category, item = select_daily_content()
        print(f"📝 Selected category: {category.title()}")
        print(f"📌 Topic: {item['title']}")
        
        # Create markdown file
        filepath = create_markdown_file(category, item, date_str)
        print(f"✅ Created: {filepath}")
        
        # Update dashboard data
        data = update_dashboard_data(category, item, date_str)
        print(f"📊 Updated dashboard data")
        print(f"🔥 Current streak: {data['current_streak']} days")
        print(f"🏆 Longest streak: {data['longest_streak']} days")
        print(f"📈 Total contributions: {data['total_contributions']}")
        
        print("=" * 50)
        print("✅ Daily content generation completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    main()
