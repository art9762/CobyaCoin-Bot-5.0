import telebot

bot = telebot.TeleBot("6498087638:AAEoZ9gcto_yyxRo7q_rHaTjIpyMciGyXqI")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "*ИМЯ ЮЗЕРА* присоединился к чату", parse_mode='Markdown')

bot.polling()
