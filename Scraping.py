import requests
import pandas as pd
import re
import os
from datetime import datetime

# استدعاء الأسرار من خزنة GitHub (نفس الأسماء التي وضعتها في الـ Secrets)
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_msg(message):
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
        try:
            requests.get(url)
        except Exception as e:
            print(f"Telegram error: {e}")

def clean_and_update():
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
            
            # تنظيف البيانات واستخراج البند
            if 'band' in df.columns: df.drop(columns=['band'], inplace=True)
            df['band'] = df['material'].str.extract(r'(\d{4,})')
            df['material'] = df['material'].str.replace(r'\[.*?\]|\d+', '', regex=True).str.strip()
            df['fetch_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # ترتيب الأعمدة وحفظ الملف
            cols = ['band', 'material', 'fetch_time'] + [c for c in df.columns if c not in ['band', 'material', 'fetch_time']]
            df = df[cols]
            df.to_excel("customs_full_data.xlsx", index=False)
            
            print("✅ Data Updated Successfully")
            # إرسال إشعار تليجرام عند النجاح
            send_telegram_msg(f"🔔 تم تحديث بيانات الجمارك بنجاح! الوقت: {df['fetch_time'].iloc[0]}")
        else:
            print(f"❌ Error: {response.status_code}")
    except Exception as e:
        print(f"⚠️ Exception: {e}")

if __name__ == "__main__":
    clean_and_update()
