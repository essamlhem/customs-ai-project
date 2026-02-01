import requests
import pandas as pd
import re
import os
from datetime import datetime

# 1. إعدادات الأمان (تذكّر أنك وضعت هذه الأسماء في GitHub Secrets)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# مفتاح API الخاص بموقع الجمارك (مدمج في الكود لأنه ثابت)
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

def send_telegram_notification(message):
    """إرسال رسالة إلى تليجرام في حال توفر التوكن والآيدي"""
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        params = {"chat_id": CHAT_ID, "text": message}
        try:
            requests.get(url, params=params)
        except Exception as e:
            print(f"خطأ في إرسال رسالة تليجرام: {e}")

def run_scraping_task():
    api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
    headers = {
        'apikey': api_key.strip(),
        'Authorization': f'Bearer {api_key.strip()}',
        'Content-Type': 'application/json'
    }

    try:
        # 2. سحب البيانات من الموقع الأصلي
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)

            # 3. تنظيف البيانات ومعالجتها
            # استخراج رقم البند الجمركي (أول 4 أرقام أو أكثر) من نص material
            df['band'] = df['material'].str.extract(r'(\d{4,})')

            # تنظيف عمود material من الأرقام والأقواس المربعة
            df['material'] = df['material'].str.replace(r'\[.*?\]|\d+', '', regex=True).str.strip()

            # إضافة توقيت السحب الحالي
            sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df['last_sync'] = sync_time

            # 4. إعادة ترتيب الأعمدة ليظهر البند أولاً
            cols = ['band', 'material', 'last_sync'] + [c for c in df.columns if c not in ['band', 'material', 'last_sync']]
            df = df[cols]

            # 5. حفظ الملف النهائي بصيغة إكسل
            df.to_excel("customs_full_data.xlsx", index=False)
            
            # 6. إرسال الإشعار النهائي
            success_msg = f"✅ تم تحديث بيانات الجمارك!\n📅 التوقيت: {sync_time}\n📊 عدد السجلات: {len(df)}"
            send_telegram_notification(success_msg)
            print("Done! Excel file updated and notification sent.")
            
        else:
            error_msg = f"❌ فشل السحب. كود الخطأ: {response.status_code}"
            send_telegram_notification(error_msg)
            print(error_msg)

    except Exception as e:
        error_msg = f"⚠️ حدث خطأ غير متوقع: {str(e)}"
        send_telegram_notification(error_msg)
        print(error_msg)

if __name__ == "__main__":
    run_scraping_task()
