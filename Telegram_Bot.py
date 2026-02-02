import telebot
import json
import csv
import os

# 1. إعدادات البوت (أدخل التوكن والـ ID الخاص بك)
TOKEN = "YOUR_BOT_TOKEN_HERE" 
CHAT_ID = "YOUR_CHAT_ID_HERE" 
bot = telebot.TeleBot(TOKEN)

def send_data_as_csv():
    json_path = "knowledge_base.json"
    csv_path = "scraped_data.csv"
    
    if os.path.exists(json_path):
        try:
            # قراءة البيانات من JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data:
                print("الملف فارغ.")
                return

            # تحويل البيانات إلى CSV مع دعم اللغة العربية للإكسل
            keys = data[0].keys()
            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            
            # إرسال ملف CSV إلى التليجرام
            with open(csv_path, 'rb') as f:
                bot.send_document(CHAT_ID, f, caption="📊 إليك بيانات السكرابينج الأخيرة بصيغة CSV (Excel)")
            
            # حذف الملف المؤقت بعد الإرسال
            os.remove(csv_path)
            
        except Exception as e:
            print(f"حدث خطأ: {e}")
    else:
        print("ملف البيانات غير موجود.")

# تنفيذ الإرسال لمرة واحدة عند بداية التشغيل
print("جاري تحويل البيانات وإرسال ملف Excel...")
send_data_as_csv()

# بقاء البوت متاحاً للرد على الرسائل الأخرى
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    bot.reply_to(message, "البوت شغال. تم إرسال ملف البيانات في الأعلى 👆")

bot.infinity_polling()
