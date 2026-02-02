import os
import telebot
import json

# هون الكود "بيطلب" البيانات من الـ Secrets تبعت غيت هوب
TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

bot = telebot.TeleBot(TOKEN)

def run_scraper():
    # كود البيانات
    data = [{"material_clean": "سمك تونة", "hs6_global": "160414"}]
    
    filename = "knowledge_base.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    # الإرسال
    with open(filename, 'rb') as f:
        bot.send_document(CHAT_ID, f, caption="✅ تم السحب باستخدام الـ Secrets")

if __name__ == "__main__":
    run_scraper()
