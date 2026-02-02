import requests
import pandas as pd
import re
import os
import json
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

def send_telegram_message(message):
    """دالة لإرسال رسالة نصية فقط"""
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        try:
            requests.post(url, data={'chat_id': CHAT_ID, 'text': message})
        except Exception as e: print(f"Error: {e}")

def send_telegram_file(file_path, caption):
    """دالة لإرسال الملفات"""
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
        try:
            with open(file_path, 'rb') as file:
                requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'document': file})
        except Exception as e: print(f"Error: {e}")

def run_global_sync():
    api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
    headers = {'apikey': api_key.strip(), 'Authorization': f'Bearer {api_key.strip()}'}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            new_data = response.json()
            file_json = "knowledge_base.json"
            sync_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # --- فحص التحديث ---
            is_updated = True
            if os.path.exists(file_json):
                with open(file_json, "r", encoding="utf-8") as f:
                    old_data = json.load(f)
                if old_data == new_data:
                    is_updated = False

            if is_updated:
                # في حال وجود تحديث: نجهز الملفات ونرسلها
                df = pd.DataFrame(new_data)
                df['band_syria'] = df['material'].str.extract(r'(\d{4,})')
                df['material_clean'] = df['material'].str.replace(r'\[.*?\]|\d+', '', regex=True).str.strip()
                df['hs6_global'] = df['band_syria'].str[:6]
                df['global_verification_link'] = "https://globaltradehelpdesk.org/ar/resources/search-hs-code"
                df['last_updated'] = sync_time

                # حفظ الملفات
                with open(file_json, "w", encoding="utf-8") as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=4)
                
                file_excel = "customs_global_brain.xlsx"
                df.to_excel(file_excel, index=False)
                
                file_csv = "customs_global_brain.csv"
                df.to_csv(file_csv, index=False, encoding='utf-8-sig')

                # إرسال التنبيه والملفات
                send_telegram_message(f"📢 تم رصد تحديث جديد اليوم! {sync_time}")
                send_telegram_file(file_excel, f"📊 ملف إكسل المحدث")
                send_telegram_file(file_csv, f"📑 ملف CSV المحدث")
                send_telegram_file(file_json, f"🧠 ذاكرة JSON المحدثة")
            else:
                # في حال لا يوجد تحديث: نرسل رسالة تطمين فقط
                send_telegram_message(f"✅ تم الفحص اليومي بنجاح: لا يوجد تعديلات جديدة في البيانات اليوم.\n📅 {sync_time}")
                
    except Exception as e: 
        send_telegram_message(f"❌ حدث خطأ أثناء محاولة الفحص اليومي: {e}")

if __name__ == "__main__":
    run_global_sync()
