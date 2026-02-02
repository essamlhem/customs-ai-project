import requests
import pandas as pd
import os
import json
from datetime import datetime

# استلام المفاتيح
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

def send_telegram(message=None, file_path=None, caption=None):
    if not BOT_TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
    if file_path and os.path.exists(file_path):
        requests.post(url + "sendDocument", data={'chat_id': CHAT_ID, 'caption': caption}, files={'document': open(file_path, 'rb')})
    elif message:
        requests.post(url + "sendMessage", data={'chat_id': CHAT_ID, 'text': message})

def run_sync():
    api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
    headers = {'apikey': API_KEY.strip(), 'Authorization': f'Bearer {API_KEY.strip()}'}
    try:
        res = requests.get(api_url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            sync_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # معالجة وحفظ
            df = pd.DataFrame(data)
            df['last_updated'] = sync_time
            df.to_excel("customs_data.xlsx", index=False)
            with open("knowledge_base.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            # إرسال أول مرة
            send_telegram(message=f"🚀 تم تشغيل النظام بنجاح!\n📦 عدد السجلات: {len(data)}")
            send_telegram(file_path="customs_data.xlsx", caption=f"📊 ملف البيانات المحدث | {sync_time}")
    except Exception as e:
        send_telegram(message=f"❌ خطأ: {str(e)}")

if __name__ == "__main__":
    run_sync()
