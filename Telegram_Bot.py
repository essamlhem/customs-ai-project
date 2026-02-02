import telebot
import json
import csv
import os

# 1. إعداداتك (تأكد من وضع التوكن والـ ID)
TOKEN = "YOUR_BOT_TOKEN_HERE" 
CHAT_ID = "YOUR_CHAT_ID_HERE" 
bot = telebot.TeleBot(TOKEN)

def send_data_as_csv():
    json_path = "knowledge_base.json"
    csv_path = "latest_scraped_data.csv"
    
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not data:
                bot.send_message(CHAT_ID, "⚠️ ملف البيانات فارغ حالياً.")
                return

            # تحويل البيانات لـ CSV مرتب للإكسل
            keys = data[0].keys()
            with open(csv_path, 'w', newline='', encoding='utf-8-sig') as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(data)
            
            # إرسال الملف
            with open(csv_path, 'rb') as f:
                bot.send_document(CHAT_ID, f, caption="📊 إليك آخر نسخة من البيانات بصيغة إكسل (CSV)")
            
            os.remove(csv_path) # تنظيف
            print("CSV Sent Successfully!")
            
        except Exception as e:
            bot.send_message(CHAT_ID, f"❌ حدث خطأ أثناء تحويل الملف: {str(e)}")
    else:
        bot.send_message(CHAT_ID, "❌ لم يتم العثور على ملف الـ JSON. تأكد أن السكرابينج اكتمل.")

# الإرسال فوراً عند التشغيل
send_data_as_csv()

# تشغيل البوت للاستقبال العادي
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.reply_to(message, "البوت شغال، والملف انبعت فوق 👆")

bot.infinity_polling()
