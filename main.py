import telebot
from telebot import types


from config import *
from models import session, Tribe, Sigil, Card


bot = telebot.TeleBot(token)


cards = session.query(Card).all()
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


@bot.message_handler(func=lambda message: message.text in [card.name for card in cards])
def card_info(message):
    card_name = message.text
    send_card_info(message, card_name)


@bot.message_handler(func=lambda message: message.text in [f'/{card.name}' for card in cards])
def slash_card_info(message):
    card_name = message.text[1:]
    send_card_info(message, card_name)


def send_card_info(message, card_name):
    card = next((card for card in cards if card.name == card_name), None)
    image_path = card.image
    with open(image_path, 'rb') as photo:
        bot.send_photo(chat_id=message.chat.id, photo=photo)
    response = f'Name: {card.name}\n'
    if card.grown:
        response += f'Grown: /{card.grown.name}\n'
    if card.fledgling:
        response += f'Fledgling: {card.fledgling[0].name}\n'
    if card.traits:
        response += f'Traits: {card.traits}\n'
    if card.tribes:
        if len(card.tribes) > 1:
            response += f"Tribes: "
            for tribe in card.tribes:
                response += f"/{tribe.name}, "
            response = response[:-2]
            response += '\n'
        else:
            response += f"Tribe: /{card.tribes[0].name}\n"
    if card.sigils:
        if len(card.sigils) > 1:
            response += f"Sigils: "
            for sigil in card.sigils:
                response += f"{sigil.name}, "
            response = response[:-2]
        else:
            response += f'Sigil: {card.sigils[0].name}'
    bot.send_message(chat_id=message.chat.id, text=response)


@bot.message_handler(func=lambda message: message.text in [card.name for card in cards])
def card_info(message):
    card_name = message.text
    send_card_info(message, card_name)


@bot.message_handler(func=lambda message: message.text in [tribe.name for tribe in tribes])
def tribe_cards(message):
    tribe_name = message.text
    send_tribe_cards(message, tribe_name)


@bot.message_handler(func=lambda message: message.text in [f'/{tribe.name}' for tribe in tribes])
def slash_tribe_cards(message):
    tribe_name = message.text[1:]
    send_tribe_cards(message, tribe_name)


def send_tribe_cards(message, tribe_name):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    tribe = next(tribe for tribe in tribes if tribe.name == tribe_name)
    tribe_cards = session.query(Card).join(Card.tribes).filter(Tribe.id == tribe.id).all()
    for card in tribe_cards:
        buttons.append(types.KeyboardButton(text=f'{card.name}'))
    buttons.append(types.KeyboardButton(text='Main menu'))
    markup.add(*buttons)
    bot.send_message(message.chat.id, 'Choose a card:', reply_markup=markup)

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
    for tribe in tribes:
        buttons.append(types.KeyboardButton(text=f'{tribe.name}'))
    markup.add(*buttons)
    buttons.append(types.KeyboardButton(text='Main menu'))
    bot.send_message(chat_id, 'Choose a tribe:', reply_markup=markup)


bot.polling()
