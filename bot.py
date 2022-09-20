import os
import time
import telebot

bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'))

@bot.message_handler(content_types="text")
def handler_text(message):
    bot.send_message(message.chat.id, message.text)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f'{e}')
        time.sleep(1)