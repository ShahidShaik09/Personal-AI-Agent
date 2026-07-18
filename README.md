# 🤖 Personal AI Agent

> An agentic AI system that automates daily tasks — file organization, email management, job searching, and WhatsApp notifications.

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Playwright](https://img.shields.io/badge/Playwright-1.61-green)
![Gmail API](https://img.shields.io/badge/Gmail-API-red)
![Automation](https://img.shields.io/badge/Automation-Daily-orange)

---

## 🎯 What it does

Every morning at **8:00 AM**, this agent automatically:

- 📁 **Organizes files** on Desktop and Downloads
- 📧 **Monitors 4 Gmail accounts** and filters spam
- 💼 **Finds LinkedIn jobs** matching your profile
- 📱 **Sends WhatsApp summary** with all updates

---

## 🛠️ Modules

### 📁 Module 1 — File Organizer
Automatically scans Desktop and Downloads folders and organizes files into categorized folders.

| Category | Extensions |
|---|---|
| PDFs | .pdf |
| Images | .jpg, .jpeg, .png, .gif |
| Documents | .doc, .docx, .pptx, .xlsx |
| Code | .py, .js, .html, .ipynb |
| Archives | .zip, .rar, .tar |
| Videos | .mp4, .mkv, .avi |

**Result:** 141 files organized in seconds! ⚡

---

### 📧 Module 2 — Email Manager
Connects to multiple Gmail accounts using Gmail API and:
- Reads unread emails
- Detects important emails (job related)
- Identifies and deletes spam
- Generates summary report

---

### 💼 Module 3 — LinkedIn Job Finder
Uses Playwright to automatically search LinkedIn for:
- Data Analyst Fresher roles
- Data Scientist Fresher roles
- Business Analyst roles
- Filters by location: Hyderabad, Bangalore, Remote

---

### 📱 Module 4 — WhatsApp Notifier
Sends a daily WhatsApp summary including:
- Email counts and important highlights
- New job listings with direct links
- File organization status

---

## ⚙️ Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.14 | Core language |
| Playwright | Browser automation |
| Gmail API | Email management |
| pywhatkit | WhatsApp automation |
| Windows Task Scheduler | Daily scheduling |

---

## 🚀 Setup

### 1. Install dependencies
```bash
pip install playwright pywhatkit google-auth-oauthlib google-api-python-client beautifulsoup4
python -m playwright install chromium
```

### 2. Gmail API setup
- Create project on Google Cloud Console
- Enable Gmail API
- Download `credentials.json`
- Place in project folder

### 3. Run individual modules
```bash
# File Organizer
python file_organizer.py

# Email Manager
python email_manager.py

# Job Finder
python job_finder.py

# WhatsApp Notifier
python whatsapp_notifier.py
```

### 4. Run all modules
```bash
python master_agent.py
```

### 5. Schedule daily (Windows)
Use Windows Task Scheduler to run `master_agent.py` daily at 8:00 AM.

---

## 📊 Results

| Module | Result |
|---|---|
| File Organizer | 141 files organized |
| Email Manager | 4 accounts, 80 emails analyzed |
| Job Finder | 6+ DA/DS jobs found daily |
| WhatsApp | Daily summary delivered |

---

## ⚠️ Security Note

Never upload these files to GitHub:
- `credentials.json`
- `token_*.json`

These are already added to `.gitignore` ✅

---

## 👨‍💻 Author

**Shahid Shaik** — BTech AI&DS Graduate
- 🔗 [LinkedIn](https://www.linkedin.com/in/shahid-shaik-a71978265/)
- 🐙 [GitHub](https://github.com/ShahidShaik09)
- 📧 theshahidprofessional@gmail.com
