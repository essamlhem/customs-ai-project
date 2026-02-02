import requests
import pandas as pd
import re
import os
import json
from datetime import datetime

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
# الكي الخاص بـ Supabase
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

def send_telegram_file(file_path, caption):
    """دالة لإرسال الملفات لتليجرام"""
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
            df = pd.DataFrame(response.json())
            
            # 1. معالجة البيانات
            df['band_syria'] = df['material'].str.extract(r'(\d{4,})')
            df['material_clean'] = df['material'].str.replace(r'\[.*?\]|\d+', '', regex=True).str.strip()
            df['hs6_global'] = df['band_syria'].str[:6]
            
            # 2. تعديل المرجع للرابط العالمي الجديد (باللغة العربية)
            df['global_verification_link'] = "https://globaltradehelpdesk.org/ar/resources/search-hs-code"
            
            sync_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            df['last_updated'] = sync_time

            # --- حفظ وإرسال الملفات الثلاثة ---

            # أ- ملف الإكسل (Excel)
            file_excel = "customs_global_brain.xlsx"
            df.to_excel(file_excel, index=False)
            send_telegram_file(file_excel, f"📊 ملف إكسل محدث\n🔗 المرجع: Global Trade\n📅 {sync_time}")

            # ب- ملف (CSV)
            file_csv = "customs_global_brain.csv"
            df.to_csv(file_csv, index=False, encoding='utf-8-sig') 
            send_telegram_file(file_csv, f"📑 ملف CSV محدث\n📅 {sync_time}")
            
            # ج- ملف الـ JSON (الذاكرة الجمركية)
            file_json = "knowledge_base.json"
            knowledge_base = df.to_json(orient="records", force_ascii=False)
            with open(file_json, "w", encoding="utf-8") as f:
                f.write(knowledge_base)
            
            send_telegram_file(file_json, f"🧠 ذاكرة المودل (JSON)\n📦 جاهزة للربط مع Across MENA")
            
    except Exception as e: print(f"Exception: {e}")

if __name__ == "__main__":
    run_global_sync()
