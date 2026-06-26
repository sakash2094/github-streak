# 🛡️ CyberSec Daily Streak

[![Daily CyberSec Streak & Deploy](https://github.com/sakash2094/github-streak/actions/workflows/daily-cybersec.yml/badge.svg)](https://github.com/sakash2094/github-streak/actions/workflows/daily-cybersec.yml)
[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-222222?style=flat&logo=github)](https://sakash2094.github.io/github-streak/)
[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> An automated, security-first cybersecurity knowledge base that publishes daily insights while building a 365-day GitHub contribution streak.

🔗 Live Dashboard:https://sakash2094.github.io/github-streak/

---

## 🚀 About The Project

**CyberSec Daily Streak** is a fully automated GitHub repository that generates and publishes daily cybersecurity content. It combines a curated local database with live API fetching to provide fresh, real-world security insights every single day. 

Built with a **security-first mindset**, the project demonstrates how automation, CI/CD, and secure coding practices can work together to create a zero-maintenance, continuously updating knowledge base.

## ✨ Key Features

- 🤖 **Fully Automated:** Runs daily via GitHub Actions with zero manual intervention.
-  **Live Data Fetching:** Integrates with the **GitHub Security Advisories API** to pull real-time, reviewed vulnerabilities.
-  **Curated Knowledge Base:** Features a robust local database of security tips, classic vulnerabilities, and essential tools.
- 📊 **Live Dashboard:** Auto-deploys to GitHub Pages, displaying real-time streak stats and daily insights.
- 🔒 **Security-First Design:** Implements strict input sanitization, XSS prevention, Content Security Policy (CSP), and Principle of Least Privilege (PoLP) in workflows.
-  **Streak Tracking:** Automatically calculates and displays current and longest contribution streaks.

## ️ Tech Stack

- **Language:** Python 3.11
- **Automation:** GitHub Actions (YAML)
- **Hosting:** GitHub Pages
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **APIs:** GitHub Security Advisories API

## ⚙️ How It Works

1. **Trigger:** Every day at 10:00 AM UTC, the GitHub Action workflow is triggered.
2. **Fetch & Generate:** The Python script (`generate_content.py`) fetches live advisories and randomly selects a topic (Tip, Vulnerability, or Tool).
3. **Sanitize & Save:** Content is rigorously sanitized to prevent XSS/injection, then saved as a Markdown file in the appropriate directory.
4. **Update Dashboard:** The `dashboard_data.json` file is updated with the new streak statistics.
5. **Commit & Deploy:** The changes are committed to the `main` branch, and GitHub Pages automatically redeploys the live dashboard.

## 📂 Project Structure

```text
github-streak/
├── .github/workflows/      # GitHub Actions automation scripts
├── 01-Security-Tips/       # Daily generated security tips
── 02-Vulnerabilities/     # Daily generated vulnerability spotlights
├── 03-Tools/               # Daily generated tool guides
├── dashboard_data.json     # JSON data powering the live dashboard
├── generate_content.py     # The core Python engine
└── index.html              # The live dashboard frontend
```
🛡️ Security Highlights
This project was built with security as a top priority:
Input Sanitization: All generated content is scrubbed of malicious scripts and event handlers.
XSS Prevention: The frontend uses safe DOM manipulation and strict Content Security Policies.
Least Privilege: GitHub Actions are scoped with minimal read-all permissions, granting write access only to the specific job that needs it.
Targeted Commits: The workflow only stages specific directories, preventing accidental commits of temporary files.

📈 Roadmap
Add integration with CISA (Cybersecurity and Infrastructure Security Agency) alerts.
Implement a "History" page to browse all past daily posts.
Add AI-generated summaries for complex CVEs using GitHub Copilot API.
Implement email notifications for critical severity vulnerabilities.

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

📄 License
Distributed under the MIT License. See LICENSE for more information.
<p align="center">
Made with ❤️ and ☕ by <a href="https://github.com/sakash2094">sakash2094</a>
</p>
