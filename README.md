# 📊 Automated Marketing Report Generator

A Python-based tool to automatically pull ad performance data from a PostgreSQL database (like Neon), detect anomalies, generate Excel + PDF charts, and send to Slack.

---

## 🚀 Features

- ✅ Fetches 7-day ad performance from PostgreSQL (Neon compatible)
- ✅ Detects click anomalies with standard deviation
- ✅ Generates Excel reports and PDF charts
- ✅ Sends reports to Slack (optional)
- ✅ Uses environment variables for security
- ✅ Mock data fallback for testing
- ✅ Schedule with `schedule` for daily automation

---

## 🧰 Tech Stack

- Python 🐍
- Pandas & Matplotlib
- PostgreSQL / Neon DB
- Slack SDK
- Schedule (job automation)
- `python-dotenv` (config management)

---

## 📁 Setup

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/automated-marketing-report-generator.git
cd automated-marketing-report-generator
