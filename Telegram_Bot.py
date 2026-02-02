import telebot
from Brain import AcrossMenaBrain

# استبدل النص التالي بالتوكن الذي حصلت عليه من BotFather
TOKEN = "8532723888:AAF9Gte5QfKRPMSM1DE_9aH1fDibArzU708"
 

bot = telebot.TeleBot(TOKEN)
brain = AcrossMenaBrain()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا عيسى في Across MENA! 🌍\nأنا جاهز لتحليل أي منتج تريد استيراده، شو ببالك اليوم؟")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_query = message.text
    # نمرر السؤال لـ "العقل" الذي بنيناه
    response = brain.ask(user_query)
    bot.reply_to(message, response)

print("Bot is alive...")
bot.infinity_polling()
