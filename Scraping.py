import requests
import json
import os
import csv
import telebot

# 1. إعدادات البوت (تأكد من وضع التوكن والـ ID)
TOKEN = "8419864931:AAHr8_PZwl5C1B0MLbc4qP6h4VFqBQWN220"
CHAT_ID = "460803708"
DATA_FILE_JSON = "knowledge_base.json"
DATA_FILE_CSV = "knowledge_base.csv"
bot = telebot.TeleBot(TOKEN)

def scrape_data():
    # --- هون كود السكرابينج الحقيقي تبعك ---
    # مثال (استبدله بالكود الخاص بك):
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
    print("🔄 جاري سحب البيانات ومقارنتها...")
    new_scraped_data = scrape_data()
    
    # التحقق من وجود تحديث
    has_update = False
    if os.path.exists(DATA_FILE_JSON):
        with open(DATA_FILE_JSON, 'r', encoding='utf-8') as f:
            old_data = json.load(f)
        if new_scraped_data != old_data:
            has_update = True
    else:
        has_update = True # أول مرة تشغيل

    if has_update:
        print("⚠️ تم رصد بيانات جديدة! جاري الإرسال...")
        
        # حفظ الملفات محلياً
        with open(DATA_FILE_JSON, 'w', encoding='utf-8') as f:
            json.dump(new_scraped_data, f, ensure_ascii=False, indent=4)
        save_as_csv(new_scraped_data, DATA_FILE_CSV)
        
        # إرسال الملفين للتليجرام
        with open(DATA_FILE_JSON, 'rb') as f_json:
            bot.send_document(CHAT_ID, f_json, caption="📄 نسخة JSON (للنظام)")
            
        with open(DATA_FILE_CSV, 'rb') as f_csv:
            bot.send_document(CHAT_ID, f_csv, caption="📊 نسخة Excel (للمراجعة)")
            
        bot.send_message(CHAT_ID, "✅ تم تحديث قاعدة البيانات بنجاح.")
    else:
        print("✅ البيانات مطابقة للنسخة الحالية، لا يوجد جديد.")

if __name__ == "__main__":
    run_sync()
