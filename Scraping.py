import requests
import pandas as pd
import re
import os
from datetime import datetime

# إعدادات الأمان
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

def send_telegram_file(file_path, caption):
    """إرسال ملف الإكسل مباشرة إلى تليجرام"""
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
        try:
            with open(file_path, 'rb') as file:
                payload = {'chat_id': CHAT_ID, 'caption': caption}
                files = {'document': file}
                requests.post(url, data=payload, files=files)
        except Exception as e:
            print(f"خطأ في إرسال الملف: {e}")

def run_scraping_task():
    api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
    headers = {
        'apikey': api_key.strip(),
        'Authorization': f'Bearer {api_key.strip()}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            
            # معالجة البيانات
            df['band'] = df['material'].str.extract(r'(\d{4,})')
            df['material'] = df['material'].str.replace(r'\[.*?\]|\d+', '', regex=True).str.strip()
            sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df['last_sync'] = sync_time

            # حفظ الملف
            file_name = "customs_full_data.xlsx"
            df.to_excel(file_name, index=False)
            
            # إرسال الملف بدلاً من النص فقط
            caption = f"✅ تحديث جديد لبيانات الجمارك\n📅 {sync_time}"
            send_telegram_file(file_name, caption)
            
            print("Done! Excel file sent to Telegram.")
        else:
            print(f"Error: {response.status_code}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    run_scraping_task()
