import telebot
from telebot import types


from config import token
from models import session, Tribe, Sigil, Card


bot = telebot.TeleBot(token)


cards = session.query(Card).all()
tribes = session.query(Tribe).all()
sigils = session.query(Sigil).all()


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome, Challenger. I was waiting for you.")
    bot.send_message(message.chat.id, "You can simply send card, tribe or sigil name to me and I'll give you all the "
                                      "information I have about it. Or you can try my buttons.")
    main_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Main menu')
def handle_back(message):
    main_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Tribes')
def handle_back(message):
    tribes_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Sigils')
def handle_back(message):
    sigils_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Find Card via stats')
def handle_back(message):
    find_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'No Power')
def handle_back(message):
    find_by_power(message)


@bot.message_handler(func=lambda message: message.text == 'No Health')
def handle_back(message):
    find_by_health(message)


@bot.message_handler(func=lambda message: message.text == 'Power')
def power_buttons(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(text='No Power'),
               types.KeyboardButton(text='⚔'),
               types.KeyboardButton(text='⚔⚔'),
               types.KeyboardButton(text='⚔⚔⚔'),
               types.KeyboardButton(text='⚔⚔⚔⚔'),
               types.KeyboardButton(text='⚔⚔⚔⚔⚔+'),
               types.KeyboardButton(text='Main menu')]
    markup.add(*buttons)
    bot.send_message(message.chat.id, 'Press key for correct search.', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Health')
def health_buttons(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(text='No Health'),
               types.KeyboardButton(text='❤'),
               types.KeyboardButton(text='❤❤'),
               types.KeyboardButton(text='❤❤❤'),
               types.KeyboardButton(text='❤❤❤❤'),
               types.KeyboardButton(text='❤❤❤❤❤+'),
               types.KeyboardButton(text='Main menu')]
    markup.add(*buttons)
    bot.send_message(message.chat.id, 'Press key for correct search.', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Cost')
def cost_buttons(message):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(text='🩸'),
               types.KeyboardButton(text='🦴🦴'),
               types.KeyboardButton(text='🩸🩸'),
               types.KeyboardButton(text='🦴🦴🦴🦴'),
               types.KeyboardButton(text='🩸🩸🩸+'),
               types.KeyboardButton(text='🦴🦴🦴🦴🦴+'),
               types.KeyboardButton(text='No Cost'),
               types.KeyboardButton(text='Main menu')]
    markup.add(*buttons)
    bot.send_message(message.chat.id, 'Click the key or send cost with emojis (you can add +)', reply_markup=markup)


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
        response += f'Fledgling: /{card.fledgling[0].name}\n'
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
                response += f"/{sigil.name}, "
            response = response[:-2]
        else:
            response += f'Sigil: /{card.sigils[0].name}'
    bot.send_message(chat_id=message.chat.id, text=response)


@bot.message_handler(func=lambda message: message.text in [tribe.name for tribe in tribes])
def tribe_cards(message):
    tribe_name = message.text
    send_tribe_cards(message, tribe_name)


@bot.message_handler(func=lambda message: message.text in [f'/{tribe.name}' for tribe in tribes])
def slash_tribe_cards(message):
    tribe_name = message.text[1:]
    send_tribe_cards(message, tribe_name)


def send_tribe_cards(message, tribe_name):
    tribe = next(tribe for tribe in tribes if tribe.name == tribe_name)
    msg = f'Cards in {tribe.name}:\n'
    cards_in_tribe = session.query(Card).join(Card.tribes).filter(Tribe.id == tribe.id).all()
    for card in cards_in_tribe:
        msg += f'/{card.name}\n'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: message.text in [sigil.name for sigil in sigils])
def sigil_cards(message):
    sigil_name = message.text
    send_sigil_cards(message, sigil_name)


@bot.message_handler(func=lambda message: message.text in [f'/{sigil.name}' for sigil in sigils])
def slash_sigil_cards(message):
    sigil_name = message.text[1:]
    send_sigil_cards(message, sigil_name)


def send_sigil_cards(message, sigil_name):
    sigil = next(sigil for sigil in sigils if sigil.name == sigil_name)
    msg = f'{sigil.name} - {sigil.description}\n\nCards with {sigil.name}:\n'
    cards_with_sigil = session.query(Card).join(Card.sigils).filter(Sigil.id == sigil.id).all()
    for card in cards_with_sigil:
        msg += f'/{card.name}\n'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: message.text[0] == '⚔')
def handle_back(message):
    if len(message.text) <= 10:
        for symbol in message.text[:-1]:
            if symbol != '⚔':
                return True
        if message.text[-1] == '⚔' or message.text[-1] == '+':
            find_by_power(message)


def find_by_power(message):
    power = 0
    if message.text[0] == '⚔':
        power = len(message.text)
    if message.text[-1] != '+':
        founded_cards = [card.name for card in cards if card.power == power]
    else:
        power -= 1
        founded_cards = [card.name for card in cards if card.power >= power]
    msg = f'Cards with {message.text}:\n\n'
    for name in founded_cards:
        msg += f'/{name}\n'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: message.text[0] == '❤')
def handle_back(message):
    if len(message.text) <= 10:
        for symbol in message.text[:-1]:
            if symbol != '❤':
                return True
        if message.text[-1] == '❤' or message.text[-1] == '+':
            find_by_health(message)


def find_by_health(message):
    health = 0
    if message.text[0] == '❤':
        health = len(message.text)
    if message.text[-1] != '+':
        founded_cards = [card.name for card in cards if card.health == health]
    else:
        health -= 1
        founded_cards = [card.name for card in cards if card.health >= health]
    msg = f'Cards with {message.text}:\n\n'
    for name in founded_cards:
        msg += f'/{name}\n'
    bot.send_message(message.chat.id, msg)


@bot.message_handler(func=lambda message: message.text[0] == '🦴')
def handle_back(message):
    if len(message.text) <= 20:
        for symbol in message.text[:-1]:
            if symbol != '🦴':
                return True
        if message.text[-1] == '🦴' or message.text[-1] == '+':
            find_by_cost(message)


@bot.message_handler(func=lambda message: message.text[0] == '🩸')
def handle_back(message):
    if len(message.text) <= 10:
        for symbol in message.text[:-1]:
            if symbol != '🩸':
                return True
        if message.text[-1] == '🩸' or message.text[-1] == '+':
            find_by_cost(message)


@bot.message_handler(func=lambda message: message.text == 'No Cost')
def handle_back(message):
    find_by_cost(message)


def find_by_cost(message):
    cost = len(message.text)
    if message.text == 'No Cost':
        cost = 0
        founded_cards = [card.name for card in cards if card.cost == cost]
    if message.text[-1] == '+':
        cost -= 1
        filtered_cards = [card for card in cards if card.cost >= cost]
    else:
        filtered_cards = [card for card in cards if card.cost == cost]
    if message.text[0] == '🩸':
        founded_cards = [card.name for card in filtered_cards if card.cost_type == 'blood']
    if message.text[0] == '🦴':
        founded_cards = [card.name for card in filtered_cards if card.cost_type == 'bones']
    msg = f'Cards with {message.text}:\n\n'
    for name in founded_cards:
        msg += f'/{name}\n'
    bot.send_message(message.chat.id, msg)


def main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(text='Tribes'),
               types.KeyboardButton(text='Sigils'),
               types.KeyboardButton(text='Find Card via stats')]
    markup.add(*buttons)
    bot.send_message(chat_id, 'My buttons:', reply_markup=markup)


def find_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = [types.KeyboardButton(text='Power'),
               types.KeyboardButton(text='Health'),
               types.KeyboardButton(text='Cost'),
               types.KeyboardButton(text='Main menu')]
    markup.add(*buttons)
    bot.send_message(chat_id, 'Choose stat:', reply_markup=markup)


def tribes_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    for tribe in tribes:
        buttons.append(types.KeyboardButton(text=f'{tribe.name}'))
    buttons.append(types.KeyboardButton(text='Main menu'))
    markup.add(*buttons)
    bot.send_message(chat_id, 'Choose a tribe:', reply_markup=markup)


def sigils_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    buttons = []
    for sigil in sigils:
        buttons.append(types.KeyboardButton(text=f'{sigil.name}'))
    buttons.append(types.KeyboardButton(text='Main menu'))
    markup.add(*buttons)
    bot.send_message(chat_id, 'Pick a sigil:', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == '/Ant')
def trait(message):
    bot.send_message(message.chat.id, "Ants is a Special Behaviour, representing the Power of certain cards. "
                                      "A card with this trait has Power equal to the number of ants on their "
                                      "side of the board.")


@bot.message_handler(func=lambda message: message.text == '/Random_Card')
def trait(message):
    bot.send_message(message.chat.id, "While not in your hand or on the board the entire card image appears to be "
                                      "static. Upon drawing this card, it is temporarily replaced with a random card "
                                      "available from card choice nodes until the end of battle. You cannot add sigils "
                                      "to it, nor upgrade it through a Campfire.")


@bot.message_handler(func=lambda message: message.text == '/Ouroboros_trait')
def trait(message):
    bot.send_message(message.chat.id, "Every time Ouroboros dies, it returns to your hand with +1 Power and +1 Health. "
                                      "It will keep that stat boost throughout the entire game, even across chapters.")


@bot.message_handler(func=lambda message: message.text == '/Satisfies_Ring_Trial')
def trait(message):
    bot.send_message(message.chat.id, "When choosing a trial, if you choose the Trial of the Ring, you will pass if "
                                      "you have a Ring on your hand. If you do not have a Ring yet, 3 cards will be "
                                      "drawn from your main deck. You will pass if the Ouroboros or the Ring Worm is "
                                      "drawn.")


@bot.message_handler(func=lambda message: message.text == '/Kills_Survivors')
def trait(message):
    bot.send_message(message.chat.id, "If the Ring Worm, Adder, or Long Elk is eaten, the survivors will be poisoned. "
                                      "They will be absent from all future campfires during the rest of the run, "
                                      "allowing one to achieve the maximum of four upgrades at no risk. Using a Custom "
                                      "Deathcard with Touch of Death or transferring the Sigil to another card and "
                                      "allowing it to be eaten will not result in the survivors' deaths. However, in "
                                      "Kaycee's Mod, any card containing the Touch of Death sigil will poison the "
                                      "survivors.")


bot.polling()
