import requests
import pandas as pd
import os
import json
import hashlib
from datetime import datetime

# إعدادات الربط (تأكد من وجودها في Secrets على GitHub)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

def send_telegram_msg(message):
    """إرسال رسائل نصية لتليجرام"""
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

def send_telegram_file(file_path, caption):
    """إرسال ملفات لتليجرام"""
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
        try:
            with open(file_path, 'rb') as file:
                requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'document': file})
        except Exception as e: print(f"Error sending file: {e}")

def get_training_ref(hs6):
    """مرجع تدريب المودل - Global Trade Helpdesk"""
    if pd.isna(hs6) or hs6 == "": return ""
    return f"https://globaltradehelpdesk.org/ar/resources/search-hs-code?productCode={hs6}"

def run_smart_sync():
    api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
    headers = {'apikey': API_KEY.strip(), 'Authorization': f'Bearer {API_KEY.strip()}'}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            raw_data = response.json()
            
            # إنشاء بصمة للبيانات الحالية لمقارنتها لاحقاً
            current_hash = hashlib.md5(json.dumps(raw_data, sort_keys=True).encode()).hexdigest()
            
            last_hash = ""
            if os.path.exists("last_hash.txt"):
                with open("last_hash.txt", "r") as f: last_hash = f.read()

            now = datetime.now()
            # تقرير نهاية اليوم الساعة 11 مساءً
            is_end_of_day = now.hour == 23 and now.minute < 10 

            # الحالة 1: وجود تحديث فعلي
            if current_hash != last_hash:
                df = pd.DataFrame(raw_data)
                
                # معالجة البيانات وتحسينها
                df['band_syria'] = df['material'].str.extract(r'(\d{4,})')
                df['material_clean'] = df['material'].str.replace(r'\[.*?\]|\d+', '', regex=True).str.strip()
                df['hs6_global'] = df['band_syria'].str[:6]
                
                # إضافة مرجع التدريب (الموقع العالمي)
                df['training_ref'] = df['hs6_global'].apply(get_training_ref)
                
                sync_time = now.strftime("%Y-%m-%d %H:%M:%S")
                df['last_updated'] = sync_time

                # حفظ الملفات
                file_excel = "customs_global_brain.xlsx"
                file_json = "knowledge_base.json"
                
                df.to_excel(file_excel, index=False)
                with open(file_json, "w", encoding="utf-8") as f:
                    f.write(df.to_json(orient="records", force_ascii=False))
                
                with open("last_hash.txt", "w") as f:
                    f.write(current_hash)

                # إرسال التحديث لتليجرام
                send_telegram_file(file_excel, f"🆕 تحديث بيانات جديد!\n📅 {sync_time}\n✅ تم ربط المراجع العالمية للتدريب.")
                send_telegram_file(file_json, "🧠 ملف الذاكرة المحدث (JSON)")

            # الحالة 2: لا يوجد تحديث وهي نهاية اليوم
            elif is_end_of_day:
                send_telegram_msg("🌙 تقرير Across MENA: لا يوجد تحديثات جديدة اليوم. تم الاعتماد على آخر بصمة بيانات.")

    except Exception as e:
        print(f"حدث خطأ أثناء التشغيل: {e}")

if __name__ == "__main__":
    run_smart_sync()
