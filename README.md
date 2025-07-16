# 📊 Automated Marketing Report Generator

This project is a Python-based automation tool that:

✅ Pulls ad performance data (clicks & conversions) from a PostgreSQL database  
✅ Detects trends and anomalies in campaign performance  
✅ Generates Excel reports and PDF charts  
✅ Optionally sends the reports to a Slack channel  
✅ Can be scheduled to run automatically every day

> Ideal for marketing analysts, data engineers, and business teams looking to automate daily reporting and highlight unusual activity in their data.

---

## 🚀 What the Script Does

### ➤ Step-by-Step Workflow

1. **Connects to your PostgreSQL database**  
   - Pulls the past 7 days of data from a table called `ad_performance`  
   - You can connect to any hosted database like Neon, Supabase, RDS, or local PostgreSQL

2. **OR uses built-in mock sample data**  
   - If no DB is available or connection fails, mock data is automatically used  
   - You can toggle this fallback with `USE_MOCK_DATA` in the code

3. **Performs basic anomaly detection**  
   - Calculates a clicks threshold based on 2 standard deviations above the mean  
   - Flags any campaigns that exceed this threshold

4. **Generates a line chart and report**  
   - Saves a PNG and PDF line chart of campaign clicks over time  
   - Exports the full data as an Excel (.xlsx) report

5. **Optionally uploads both to Slack**  
   - Uses Slack’s API to send the files to a configured channel  
   - Requires a bot token and channel name in `.env`

6. **Can run on a schedule**  
   - You can set it to run every day at 8 AM using the `schedule` library

---

## 🔧 Setup Guide

### 1. Clone the Repo

git clone https://github.com/your-username/automated-marketing-report-generator.git
cd automated-marketing-report-generator

### 2. Install Python Dependencies

pip install -r requirements.txt

### 3. Create a .env File

cp .env.example .env

  Edit the .env with your PostgreSQL credentials (e.g. Neon, Supabase, or local DB) and optional Slack token:


  DB_NAME=your_database
  DB_USER=your_user
  DB_PASSWORD=your_password
  DB_HOST=your_host_url_or_ip
  DB_PORT=5432
  DB_SSLMODE=require

  SLACK_TOKEN=xoxb-your-slack-bot-token
  SLACK_CHANNEL=#your-channel
  
### 🧪 How to Run

python marketing_report_generator.py

The script will either:

Use your real database connection to pull ad_performance data

OR automatically fall back to mock sample data for testing

### 🕐 Optional: Daily Automation

To run the report automatically every day at 8AM:

Uncomment these lines at the bottom of the script:

schedule.every().day.at("08:00").do(job)

while True:
    schedule.run_pending()
    time.sleep(60)
### 🧾 Example Table Schema
Here’s the structure your ad_performance table should follow:

CREATE TABLE ad_performance (
    date DATE,
    campaign_name TEXT,
    clicks INT,
    conversions INT
);
You can import your own data into this table from CSVs, ETLs, or marketing APIs.

### 🔐 .env Reference
  # PostgreSQL DB config
  DB_NAME=neondb
  DB_USER=neondb_owner
  DB_PASSWORD=yourpassword
  DB_HOST=your-db.neon.tech
  DB_PORT=5432
  DB_SSLMODE=require

  # Slack config (optional)
  SLACK_TOKEN=xoxb-your-bot-token
  SLACK_CHANNEL=#marketing-reports

### 📸 Sample Output
Here’s a snapshot of the output this tool produces:

✅ ad_report_chart.png / ad_report_chart.pdf:
Line chart showing campaign clicks over time with anomaly threshold

✅ marketing_report_YYYY-MM-DD.xlsx:
Spreadsheet of campaign-level click/conversion data with anomaly flags
