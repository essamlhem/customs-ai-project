import requests
import pandas as pd
import re
import os
import json
from datetime import datetime

# التعديل هنا ليتوافق مع أسماء الـ Secrets في GitHub
BOT_TOKEN = os.getenv("BOT_TOKEN") 
CHAT_ID = os.getenv("CHAT_ID")
api_key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

def send_telegram(message=None, file_path=None, caption=None):
    """دالة شاملة للإرسال"""
    if not BOT_TOKEN or not CHAT_ID: 
        print("❌ نقص في الإعدادات: تأكد من BOT_TOKEN و CHAT_ID")
        return
        
    if file_path:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
        with open(file_path, 'rb') as f:
            requests.post(url, data={'chat_id': CHAT_ID, 'caption': caption}, files={'document': f})
    elif message:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

def run_global_sync():
    api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
    headers = {'apikey': api_key.strip(), 'Authorization': f'Bearer {api_key.strip()}'}
    try:
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            new_data = response.json()
            file_json = "knowledge_base.json"
            sync_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            is_updated = True
            if os.path.exists(file_json):
                with open(file_json, "r", encoding="utf-8") as f:
                    old_data = json.load(f)
                if len(old_data) == len(new_data):
                    is_updated = False

            if is_updated:
                df = pd.DataFrame(new_data)
                df['band_syria'] = df['material'].str.extract(r'(\d{4,})')
                df['material_clean'] = df['material'].str.replace(r'\[.*?\]|\d+', '', regex=True).str.strip()
                df['hs6_global'] = df['band_syria'].str[:6]
                df['global_verification_link'] = "https://globaltradehelpdesk.org/ar/resources/search-hs-code"
                df['last_updated'] = sync_time

                with open(file_json, "w", encoding="utf-8") as f:
                    json.dump(new_data, f, ensure_ascii=False)
                
                df.to_excel("customs_global_brain.xlsx", index=False)
                df.to_csv("customs_global_brain.csv", index=False, encoding='utf-8-sig')

                send_telegram(message=f"⚠️ تم رصد تحديث جديد! عدد المنتجات: {len(new_data)}")
                send_telegram(file_path="customs_global_brain.xlsx", caption="📊 إكسل المحدث")
                send_telegram(file_path="customs_global_brain.csv", caption="📑 CSV المحدث")
            else:
                send_telegram(message=f"✅ فحص يومي: لا يوجد تعديلات جديدة.\n📦 عدد المنتجات: {len(new_data)}\n⏰ {sync_time}")
    except Exception as e:
        send_telegram(message=f"❌ خطأ في السكربت: {e}")

if __name__ == "__main__":
    run_global_sync()
