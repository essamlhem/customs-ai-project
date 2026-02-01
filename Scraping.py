import requests
import pandas as pd
import re
import os
from datetime import datetime

# إعدادات الـ API
api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

# إعدادات الإشعارات (ضع بياناتك هنا)
TELEGRAM_TOKEN = "8419864931:AAHr8_PZwl5C1B0MLbc4qP6h4VFqBQWN220"
CHAT_ID = "460803708"

def send_notification(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={msg}"
    try: requests.get(url)
    except: pass

def process_and_notify():
    headers = {'apikey': api_key.strip(), 'Authorization': f'Bearer {api_key.strip()}'}
    
    try:
        # سحب البيانات الجديدة
        response = requests.get(api_url, headers=headers)
        if response.status_code != 200: return
        
        new_df = pd.DataFrame(response.json())
        
        # قراءة البيانات القديمة (إذا كانت موجودة) للمقارنة
        old_count = 0
        if os.path.exists("customs_full_data.xlsx"):
            old_df = pd.read_excel("customs_full_data.xlsx")
            old_count = len(old_df)

        # عمليات التنظيف
        if 'band' in new_df.columns: new_df.drop(columns=['band'], inplace=True)
        new_df['band'] = new_df['material'].str.extract(r'(\d{4,})')
        new_df['material'] = new_df['material'].str.replace(r'\[.*?\]|\d+', '', regex=True).str.strip()
        new_df['fetch_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # مقارنة: هل زاد عدد الأسطر؟
        new_count = len(new_df)
        if new_count > old_count and old_count != 0:
            diff = new_count - old_count
            send_notification(f"🔔 تحديث جديد! تم إضافة {diff} بند جديد في موقع الجمارك. الإجمالي الحالي: {new_count}")

        # حفظ النسخة الجديدة
        new_df.to_excel("customs_full_data.xlsx", index=False)
        print(f"✅ تم الفحص. الإجمالي: {new_count}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    process_and_notify()
