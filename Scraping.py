import requests
import pandas as pd
import os
import json
from datetime import datetime

# استلام المفاتيح من الـ Secrets
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InhsdWdhdmhtdm5tYWdheHRjZHh5Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzk2ODkyNzQsImV4cCI6MjA1NTI2NTI3NH0.mCJzpoVbvGbkEwLPyaPcMZJGdaSOwaSEtav85rK-dWA"

def send_telegram(message=None, file_path=None, caption=None):
    if not BOT_TOKEN or not CHAT_ID: return
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/"
    try:
        if file_path and os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                requests.post(url + "sendDocument", data={'chat_id': CHAT_ID, 'caption': caption}, files={'document': f})
        elif message:
            requests.post(url + "sendMessage", data={'chat_id': CHAT_ID, 'text': message})
    except Exception as e: print(f"Error sending to Telegram: {e}")

def run_sync():
    api_url = "https://xlugavhmvnmagaxtcdxy.supabase.co/rest/v1/bands?select=%2A"
    headers = {'apikey': API_KEY.strip(), 'Authorization': f'Bearer {API_KEY.strip()}'}
    try:
        res = requests.get(api_url, headers=headers)
        if res.status_code == 200:
            data = res.json()
            sync_time = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            # معالجة وحفظ البيانات
            df = pd.DataFrame(data)
            # إضافة لمسة تنظيمية بسيطة
            df['last_updated'] = sync_time
            
            excel_file = "customs_data.xlsx"
            df.to_excel(excel_file, index=False)
            
            # حفظ النسخة المرجعية للمقارنة بكرة
            with open("knowledge_base.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False)

            # إرسال التقرير الأول
            send_telegram(message=f"🚀 تم إعادة تشغيل النظام بنجاح يا عيسى!\n📦 عدد السجلات المسحوبة: {len(data)}")
            send_telegram(file_path=excel_file, caption=f"📊 ملف البيانات الأساسي | {sync_time}")
        else:
            send_telegram(message=f"❌ خطأ في سحب البيانات: {res.status_code}")
    except Exception as e:
        send_telegram(message=f"❌ حدث خطأ فني: {str(e)}")

if __name__ == "__main__":
    run_sync()
