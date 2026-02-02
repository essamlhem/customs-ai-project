import requests
import json
import os
import csv
import telebot
from datetime import datetime

# سحب البيانات من السيكريت (عشان يضل شغال على GitHub)
TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

def scrape_data():
    # كود السحب تبعك
    data = [{"material_clean": "سمك تونة", "hs6_global": "160414", "price": "100"}]
    return data

def run_sync():
    # 1. تجهيز البصمة الزمنية
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"🔄 بدأت عملية السحب بتاريخ: {now}")
    
    new_scraped_data = scrape_data()
    
    # 2. إضافة البصمة داخل البيانات (عشان تظهر بالملف)
    result_with_fingerprint = {
        "last_update": now,
        "data": new_scraped_data
    }

    # حفظ ملف JSON
    with open("knowledge_base.json", "w", encoding="utf-8") as f:
        json.dump(result_with_fingerprint, f, ensure_ascii=False, indent=4)

    # حفظ ملف CSV (Excel) مع البصمة في الاسم
    csv_file = f"Data_Update_{datetime.now().strftime('%Y%m%d')}.csv"
    if new_scraped_data:
        keys = new_scraped_data[0].keys()
        with open(csv_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(new_scraped_data)

    # 3. إرسال الملفات مع رسالة فيها البصمة
    with open("knowledge_base.json", "rb") as f1:
        bot.send_document(CHAT_ID, f1, caption=f"📄 نسخة JSON\n⏰ البصمة: {now}")
    
    with open(csv_file, "rb") as f2:
        bot.send_document(CHAT_ID, f2, caption=f"📊 نسخة Excel\n📅 تحديث يوم: {now}")

if __name__ == "__main__":
    run_sync()
