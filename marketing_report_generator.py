import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from slack_sdk import WebClient
from datetime import datetime, timedelta
import schedule
import time
import psycopg2
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ========== CONFIG ==========
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "sslmode": os.getenv("DB_SSLMODE", "require")
}

SLACK_TOKEN = os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL")
USE_MOCK_DATA = False  # Set to True if you want to test without a database
# ============================

# 1. Get data from PostgreSQL or use mock
def get_data():
    if USE_MOCK_DATA:
        print("🔁 Using mock data...")
        return generate_mock_data()
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        query = """
            SELECT date, campaign_name, clicks, conversions
            FROM ad_performance
            WHERE date >= CURRENT_DATE - INTERVAL '7 days'
        """
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print("❌ Failed to connect to database:", e)
        print("🔁 Falling back to mock data.")
        return generate_mock_data()

# 1a. Mock fallback
def generate_mock_data():
    import random
    campaigns = ['Spring Sale', 'Summer Launch', 'Holiday Promo']
    dates = [datetime.today() - timedelta(days=i) for i in range(7)]
    data = []
    for date in dates:
        for campaign in campaigns:
            data.append({
                'date': date.strftime('%Y-%m-%d'),
                'campaign_name': campaign,
                'clicks': random.randint(100, 1000),
                'conversions': random.randint(10, 100)
            })
    return pd.DataFrame(data)

# 2. Anomaly detection
def detect_anomalies(df):
    df['anomaly'] = False
    threshold = df['clicks'].mean() + 2 * df['clicks'].std()
    df.loc[df['clicks'] > threshold, 'anomaly'] = True
    return df, threshold

# 3. Chart generation
def create_chart(df, threshold):
    df['date'] = pd.to_datetime(df['date'])
    plt.figure(figsize=(10,6))
    for campaign in df['campaign_name'].unique():
        sub = df[df['campaign_name'] == campaign]
        plt.plot(sub['date'], sub['clicks'], label=campaign, marker='o')

    plt.axhline(y=threshold, color='red', linestyle='--', label='Anomaly Threshold')
    plt.title("Ad Performance - Clicks Over Time")
    plt.xlabel("Date")
    plt.ylabel("Clicks")
    plt.legend()
    plt.tight_layout()
    plt.savefig("ad_report_chart.png")

    with PdfPages("ad_report_chart.pdf") as pdf:
        pdf.savefig()
    plt.close()
    print("📊 Chart saved as PNG and PDF")

# 4. Excel export
def export_excel(df):
    today = datetime.today().strftime('%Y-%m-%d')
    filename = f"marketing_report_{today}.xlsx"
    df.to_excel(filename, index=False)
    print(f"📁 Excel report saved: {filename}")
    return filename

# 5. Slack report upload
def send_slack_report(excel_path, pdf_path):
    if not SLACK_TOKEN or not SLACK_CHANNEL:
        print("⚠️ Slack token/channel not configured. Skipping Slack upload.")
        return

    try:
        client = WebClient(token=SLACK_TOKEN)
        client.files_upload(channels=SLACK_CHANNEL, file=excel_path, title="📊 Marketing Report (Excel)")
        client.files_upload(channels=SLACK_CHANNEL, file=pdf_path, title="📈 Report Chart (PDF)")
        print("✅ Report sent to Slack.")
    except Exception as e:
        print("❌ Slack upload failed:", e)

# 6. Main job
def job():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running marketing report job...")
    df = get_data()
    df, threshold = detect_anomalies(df)
    create_chart(df, threshold)
    excel_path = export_excel(df)
    pdf_path = "ad_report_chart.pdf"
    send_slack_report(excel_path, pdf_path)
    print("✅ Job complete.\n")

# 7. Manual run
if __name__ == "__main__":
    job()

    # Uncomment for daily scheduling
    # schedule.every().day.at("08:00").do(job)
    # while True:
    #     schedule.run_pending()
    #     time.sleep(60)
