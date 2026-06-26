import json
import os
import datetime
import random

# --- 1. YOUR CYBERSECURITY DATABASE ---
TIPS = [
    {"title": "Password Hygiene", "content": "Never reuse passwords across different sites. Use a password manager like **Bitwarden** or **1Password** to generate and store complex, unique passwords for every account."},
    {"title": "Phishing Awareness", "content": "Always verify the sender's email address and hover over links before clicking. Attackers often use urgent language to make you bypass critical thinking."},
    {"title": "Multi-Factor Authentication", "content": "Enable MFA/2FA on all critical accounts. Use an Authenticator app or hardware key (**YubiKey**) instead of SMS, which is vulnerable to SIM swapping."}
]

VULNS = [
    {"title": "SQL Injection (SQLi)", "content": "Occurs when untrusted user input is directly concatenated into a database query. **Prevention:** Always use parameterized queries (prepared statements) and ORMs."},
    {"title": "Cross-Site Scripting (XSS)", "content": "Happens when an app includes untrusted data in a web page without proper escaping, allowing attackers to run malicious JavaScript. **Prevention:** Sanitize input and use Content Security Policy (CSP) headers."},
    {"title": "Insecure Direct Object References (IDOR)", "content": "Occurs when an app provides direct access to objects (like database records) based on user input without checking authorization. **Prevention:** Always verify that the logged-in user owns the resource."}
]

TOOLS = [
    {"title": "Nmap", "content": "The industry standard for network discovery and security auditing. Use it to find open ports, detect service versions, and map out a target's network surface.\n\n**Quick command:** `nmap -sC -sV -p- <target_ip>`"},
    {"title": "Burp Suite", "content": "An integrated platform for web security testing. Its intercepting proxy allows you to pause, inspect, and modify HTTP/S requests between your browser and the server."},
    {"title": "Wireshark", "content": "The world's foremost network protocol analyzer. It lets you capture and interactively browse traffic running on a network to find unencrypted credentials or malware beaconing."}
]

# --- 2. GENERATE TODAY'S CONTENT ---
categories = ['tips', 'vulnerabilities', 'tools']
category = random.choice(categories)

if category == 'tips':
    item = random.choice(TIPS)
    folder = "01-Security-Tips"
elif category == 'vulnerabilities':
    item = random.choice(VULNS)
    folder = "02-Vulnerabilities"
else:
    item = random.choice(TOOLS)
    folder = "03-Tools"

today_str = datetime.datetime.now().strftime("%Y-%m-%d")
filename = f"{today_str}-{item['title'].lower().replace(' ', '-')}.md"
os.makedirs(folder, exist_ok=True)

with open(f"{folder}/{filename}", "w", encoding="utf-8") as f:
    f.write(f"# {item['title']}\n\n{item['content']}\n\n---\n*Generated automatically on {today_str}.*")

# --- 3. UPDATE THE DASHBOARD DATA (JSON) ---
json_file = 'dashboard_data.json'
if os.path.exists(json_file):
    with open(json_file, 'r') as f:
        data = json.load(f)
else:
    data = {'dates': [], 'latest_content': {}}

if today_str not in data['dates']:
    data['dates'].append(today_str)
    data['dates'].sort()

# Calculate Streaks
dates_set = set(data['dates'])
current_streak = 0
d = datetime.datetime.now()
while d.strftime("%Y-%m-%d") in dates_set:
    current_streak += 1
    d -= datetime.timedelta(days=1)

longest_streak = 0
temp_streak = 1
sorted_dates = sorted(data['dates'])
if len(sorted_dates) > 0:
    longest_streak = 1
    for i in range(1, len(sorted_dates)):
        prev = datetime.datetime.strptime(sorted_dates[i-1], "%Y-%m-%d")
        curr = datetime.datetime.strptime(sorted_dates[i], "%Y-%m-%d")
        if (curr - prev).days == 1:
            temp_streak += 1
            longest_streak = max(longest_streak, temp_streak)
        else:
            temp_streak = 1

data['current_streak'] = current_streak
data['longest_streak'] = longest_streak
data['total_contributions'] = len(data['dates'])
data['latest_content'] = {
    'title': item['title'],
    'category': category,
    'content': item['content'],
    'date': today_str
}

with open(json_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Generated {filename} and updated dashboard data!")
