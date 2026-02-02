import requests
import json
import os
import telebot

# إعدادات البوت والملفات
TOKEN = "YOUR_BOT_TOKEN_HERE"
CHAT_ID = "YOUR_CHAT_ID_HERE"
DATA_FILE = "knowledge_base.json"
bot = telebot.TeleBot(TOKEN)

def scrape_data():
    # --- هون بتحط كود السكرابينج اللي سويناه أول مرة ---
    # مثال بسيط (استبدله بكود السحب الحقيقي تبعك):
    new_data = [{"material_clean": "سمك تونة", "hs6_global": "160414"}] 
    return new_data

def run_sync():
    print("🔄 بدأت عملية سحب البيانات...")
    new_scraped_data = scrape_data()
    
    # 1. فحص إذا في ملف قديم للمقارنة
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        
        # 2. المقارنة (إذا تغيرت الداتا عن القديمة)
        if new_scraped_data != old_data:
            print("⚠️ تم كشف تحديث في البيانات!")
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(new_scraped_data, f, ensure_ascii=False, indent=4)
            
            # إرسال تنبيه للمدير ولإلك
            bot.send_message(CHAT_ID, "📢 تحديث جديد! تم رصد تغييرات في أسعار أو مواد الموقع.")
            with open(DATA_FILE, 'rb') as f:
                bot.send_document(CHAT_ID, f, caption="📊 ملف البيانات المحدث (JSON)")
        else:
            print("✅ لا يوجد تغيير في البيانات اليوم.")
            # اختياري: bot.send_message(CHAT_ID, "✅ تم الفحص اليومي: لا يوجد تحديثات.")
    else:
        # 3. أول مرة تشغيل (سحب نسخة أولية)
        print("📥 أول تشغيل: سحب النسخة الأولية...")
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(new_scraped_data, f, ensure_ascii=False, indent=4)
        
        with open(DATA_FILE, 'rb') as f:
            bot.send_document(CHAT_ID, f, caption="✅ النسخة الأولية من البيانات")

if __name__ == "__main__":
    run_sync()
