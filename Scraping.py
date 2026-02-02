import requests
import json
import os
import csv
import telebot

# سحب البيانات من بيئة GitHub (Security Friendly)
TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

DATA_FILE_JSON = "knowledge_base.json"
DATA_FILE_CSV = "knowledge_base.csv"

# تأكد إن البيانات وصلت قبل تشغيل البوت
if not TOKEN or not CHAT_ID:
    print("❌ خطأ: التوكن أو الـ ID مو موجودين في إعدادات GitHub!")
    exit(1)

bot = telebot.TeleBot(TOKEN)

def scrape_data():
    # كود السكرابينج تبعك هون
    new_data = [{"material_clean": "سمك تونة", "hs6_global": "160414", "price": "100"}] 
    return new_data

def save_as_csv(data, filename):
    if not data: return
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def run_sync():
    print("🔄 جاري سحب البيانات...")
    new_scraped_data = scrape_data()
    
    # حفظ وإرسال
    with open(DATA_FILE_JSON, 'w', encoding='utf-8') as f:
        json.dump(new_scraped_data, f, ensure_ascii=False, indent=4)
    save_as_csv(new_scraped_data, DATA_FILE_CSV)
    
    with open(DATA_FILE_JSON, 'rb') as f_json:
        bot.send_document(CHAT_ID, f_json, caption="📄 نسخة JSON")
    with open(DATA_FILE_CSV, 'rb') as f_csv:
        bot.send_document(CHAT_ID, f_csv, caption="📊 نسخة Excel")
    print("✅ تم الإرسال بنجاح!")

if __name__ == "__main__":
    run_sync()
