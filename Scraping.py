import requests
import pandas as pd
import os
import json
import hashlib
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

def send_telegram_msg(message):
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

def send_telegram_file(file_path, caption):
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
        try:
            with open(file_path, 'rb') as file:
                requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'document': file})
        except Exception as e: print(f"Error: {e}")

def run_smart_sync():
    api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
    headers = {'apikey': api_key.strip(), 'Authorization': f'Bearer {api_key.strip()}'}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            raw_data = response.json()
            # إنشاء "بصمة" للبيانات الحالية للتأكد من التغيير
            current_hash = hashlib.md5(json.dumps(raw_data, sort_keys=True).encode()).hexdigest()
            
            # قراءة البصمة القديمة إذا وجدت
            last_hash = ""
            if os.path.exists("last_hash.txt"):
                with open("last_hash.txt", "r") as f: last_hash = f.read()

            now = datetime.now()
            is_end_of_day = now.hour == 23 and now.minute < 10 # تقرير نهاية اليوم (الساعة 11 مساءً)

            # الحالة 1: وجود تحديث فعلي في البيانات
            if current_hash != last_hash:
                df = pd.DataFrame(raw_data)
                df['band_syria'] = df['material'].str.extract(r'(\d{4,})')
                df['material_clean'] = df['material'].str.replace(r'\[.*?\]|\d+', '', regex=True).str.strip()
                df['hs6_global'] = df['band_syria'].str[:6]
                sync_time = now.strftime("%Y-%m-%d %H:%M:%S")
                
                # حفظ الملفات
                file_excel = "customs_global_brain.xlsx"
                df.to_excel(file_excel, index=False)
                with open("knowledge_base.json", "w", encoding="utf-8") as f:
                    f.write(df.to_json(orient="records", force_ascii=False))
                
                # تحديث ملف البصمة
                with open("last_hash.txt", "w") as f: f.write(current_hash)

                # إرسال الملفات لوجود تحديث
                send_telegram_file(file_excel, f"🆕 تحديث جديد تم رصده!\n📅 {sync_time}\n📊 تم تحليل {len(df)} مادة.")
                send_telegram_file("knowledge_base.json", "🧠 ذاكرة JSON المحدثة")

            # الحالة 2: لا يوجد تحديث وهي نهاية اليوم
            elif is_end_of_day:
                send_telegram_msg("🌙 تقرير نهاية اليوم: لم يتم تحديث أي بيانات جديدة اليوم.")

    except Exception as e: print(f"Exception: {e}")

if __name__ == "__main__":
    run_smart_sync()
