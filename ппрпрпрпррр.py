import telebot

bot = telebot.TeleBot("Your Bot token")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "*ИМЯ ЮЗЕРА* присоединился к чату", parse_mode='Markdown')

bot.polling()
