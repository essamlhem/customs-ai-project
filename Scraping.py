import requests
import pandas as pd
import re
import os
import json
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

def send_telegram_file(file_path, caption):
    if TELEGRAM_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
        try:
            with open(file_path, 'rb') as file:
                requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'document': file})
        except Exception as e: print(f"Error: {e}")

def get_global_info(hs6):
    """دالة تجريبية لجلب الوصف العالمي (يمكن تطويرها لربطها بـ API عالمي لاحقاً)"""
    # حالياً سنضع رابطاً بحثياً للمودل ليستخدمه في التحقق
    return f"https://www.foreign-trade.com/reference/hscode.htm?code={hs6}"

def run_global_sync():
    api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
    headers = {'apikey': api_key.strip(), 'Authorization': f'Bearer {api_key.strip()}'}

    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            
            # تنظيف البيانات السورية
            df['band_syria'] = df['material'].str.extract(r'(\d{4,})')
            df['material_clean'] = df['material'].str.replace(r'\[.*?\]|\d+', '', regex=True).str.strip()
            
            # استخراج الرمز الدولي HS6
            df['hs6_global'] = df['band_syria'].str[:6]
            
            # إضافة رابط التحقق العالمي لكل بند
            df['global_verification_link'] = df['hs6_global'].apply(get_global_info)
            
            sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df['last_updated'] = sync_time

            # حفظ الملفات
            file_excel = "customs_global_brain.xlsx"
            df.to_excel(file_excel, index=False)
            
            # تحديث ذاكرة المودل JSON
            knowledge_base = df.to_json(orient="records", force_ascii=False)
            with open("knowledge_base.json", "w", encoding="utf-8") as f:
                f.write(knowledge_base)

            send_telegram_file(file_excel, f"🌍 تم ربط البيانات السورية بالروابط العالمية!\n📦 جاهز للمرحلة القادمة.")
            
    except Exception as e: print(f"Exception: {e}")

if __name__ == "__main__":
    run_global_sync()
