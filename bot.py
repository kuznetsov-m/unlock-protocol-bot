import os
import time
import telebot
from telebot.apihelper import ApiTelegramException
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import User
import text

bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'))
engine = create_engine(f'{ os.environ.get("DATABASE_URL")}'.replace('postgres://', 'postgresql://'))

def send_message(chat_id: int, text: str, reply_markup=None):
    try:
        return bot.send_message(chat_id, text, reply_markup=reply_markup)
    except ApiTelegramException as e:
        if e.error_code == 403:
            with Session(engine) as session:
                user = session.query(User).filter(User.id==chat_id).with_for_update().first()
                if user:
                    user.is_stopped = 1
                    session.commit()

def choose_role(message):
    keyboard = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=False)
    keyboard.row('⭐️ Author','📥 Subscriber')
    message = send_message(message.chat.id, 'Choose your role', reply_markup=keyboard)
    bot.register_next_step_handler(message, choose_role_handler)

def author(message):
    send_message(message.chat.id, 'dev status: in progress')
    bot.register_next_step_handler(message, choose_role_handler)

def subscriber(message):
    url = f'{os.environ.get("SIGN_URL")}'
    url += f'?user_id={message.chat.id}'
    url += f'&token_address={os.environ.get("TOKEN_ADDRESS")}'
    
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='🖋 Sing message for invite', url=url))
    send_message(message.chat.id, text.need_to_check_token, reply_markup=markup)
    bot.register_next_step_handler(message, choose_role_handler)

def choose_role_handler(message):
    if 'author' in message.text.lower():
        author(message)
    elif 'subscriber' in message.text.lower():
        subscriber(message)
    else:
        choose_role(message)

@bot.message_handler(commands=['start'])
def start(message):
    with Session(engine) as session:
        user = session.query(User).filter(User.id==message.chat.id).with_for_update().first()
        if not user:
            u = User(id=message.chat.id, first_name=message.chat.first_name, last_name=message.chat.last_name)
            session.add(u) 
            session.commit()
    choose_role(message)

@bot.message_handler(content_types="text")
def handler_text(message):
    send_message(message.chat.id, message.text)

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f'{e}')
        time.sleep(1)