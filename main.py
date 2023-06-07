import telebot
from telebot import types


from config import *
from models import session, Tribe, Sigil, Card


bot = telebot.TeleBot(token)


tribes = session.query(Tribe).all()
sigils = session.query(Sigil).all()


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome, Challenger. I was waiting for you.")
    main_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Main menu')
def handle_back(message):
    main_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Tribes')
def handle_back(message):
    tribes_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text in [card.name for card in session.query(Card).all()])
def card_info(message):
    card_name = message.text
    card = session.query(Card).filter(Card.name == card_name).first()
    image_path = card.image
    with open(image_path, 'rb') as photo:
        bot.send_photo(chat_id=message.chat.id, photo=photo)
    response = f'Card: {card.name}\n'
    if card.traits:
        response += f'Traits: {card.traits}\n'
    if card.tribes:
        response += f"Tribes: {str([tribe.name for tribe in card.tribes])}\n"
    if card.sigils:
        response += f"Sigils: {str([sigil.name for sigil in card.sigils])}"
    bot.send_message(chat_id=message.chat.id, text=response)


for t in tribes:
    tribe_name = t.name
    @bot.message_handler(func=lambda message, tribe=tribe_name: message.text == tribe)
    def handle_back(message, tribe=tribe_name):
        call_tribe(message.chat.id, tribe)


'''
@bot.message_handler(func=lambda message: message.text == 'Sigils')
def handle_back(message):
    sigils_menu(message.chat.id)
'''

def main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(text='Tribes'),
               types.KeyboardButton(text='Sigils')]
    markup.add(*buttons)
    bot.send_message(chat_id, 'Choose an option:', reply_markup=markup)


def tribes_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    for t in tribes:
        buttons.append(types.KeyboardButton(text=f'{t.name}'))
    markup.add(*buttons)
    buttons.append(types.KeyboardButton(text='Main menu'))
    bot.send_message(chat_id, 'Choose a tribe:', reply_markup=markup)


def call_tribe(chat_id, tribe_name):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    tribe = session.query(Tribe).filter(Tribe.name == tribe_name).first()
    cards = session.query(Card).join(Card.tribes).filter(Tribe.id == tribe.id).all()
    buttons = []
    for card in cards:
        buttons.append(types.KeyboardButton(text=f'{card.name}'))
    buttons.append(types.KeyboardButton(text='Main menu'))
    markup.add(*buttons)
    bot.send_message(chat_id, 'Choose a card:', reply_markup=markup)


bot.polling()
