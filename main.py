import telebot
from telebot import types


from config import *


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Welcome, Challenger. I was waiting for you.")
    send_main_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Characters')
def handle_characters(message):
    bot.send_message(message.chat.id, "In developing")
    send_main_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Cards')
def handle_cards(message):
    bot.send_message(message.chat.id, "You can find a card and get information about it by the following parameters.")
    send_card_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Stickers')
def handle_stickers(message):
    bot.send_message(message.chat.id, "In developing")
    send_main_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Personality test')
def handle_personality_test(message):
    bot.send_message(message.chat.id, "In developing")
    send_main_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Main menu')
def handle_back(message):
    send_main_menu(message.chat.id)


def send_main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [types.KeyboardButton(text='Characters'),
               types.KeyboardButton(text='Cards'),
               types.KeyboardButton(text='Stickers'),
               types.KeyboardButton(text='Personality test')]
    markup.add(*buttons)
    bot.send_message(chat_id, 'Choose an option:', reply_markup=markup)


def send_card_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [types.KeyboardButton(text='Family'),
               types.KeyboardButton(text='Abilities'),
               types.KeyboardButton(text='Cost'),
               types.KeyboardButton(text='Attack'),
               types.KeyboardButton(text='Health'),
               types.KeyboardButton(text='Main menu')]
    markup.add(*buttons)
    bot.send_message(chat_id, 'Choose the parameter:', reply_markup=markup)


#########

@bot.message_handler(func=lambda message: message.text == 'Family')
def handle_card_family(message):
    bot.send_message(message.chat.id, "You selected 'Family'")
    send_family_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Abilities')
def handle_card_abilities(message):
    bot.send_message(message.chat.id, "You selected 'Abilities'")
    send_abilities_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Cost')
def handle_card_cost(message):
    bot.send_message(message.chat.id, "You selected 'Cost'")
    send_cost_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Attack')
def handle_card_attack(message):
    bot.send_message(message.chat.id, "You selected 'Attack'")
    send_attack_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Health')
def handle_card_health(message):
    bot.send_message(message.chat.id, "You selected 'Health'")
    send_health_menu(message.chat.id)


@bot.message_handler(func=lambda message: message.text == 'Main menu')
def handle_main_menu(message):
    send_main_menu(message.chat.id)


def send_family_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [types.KeyboardButton(text='Avian'),
               types.KeyboardButton(text='Canine'),
               types.KeyboardButton(text='Hooved'),
               types.KeyboardButton(text='Insect'),
               types.KeyboardButton(text='Reptile'),
               types.KeyboardButton(text='Pelts'),
               types.KeyboardButton(text='Miscellaneous'),
               types.KeyboardButton(text='Spawned / Given'),
               types.KeyboardButton(text='Non-obtainable / Boss exclusive'),
               types.KeyboardButton(text='Main menu')]
    markup.add(*buttons)
    bot.send_message(chat_id, 'Choose the Family parameter:', reply_markup=markup)


def send_abilities_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [types.KeyboardButton(text='Ability 1'),
               types.KeyboardButton(text='Ability 2'),
               types.KeyboardButton(text='Ability 3'),
               types.KeyboardButton(text='Main menu')]
    markup.add(*buttons)
    bot.send_message(chat_id, 'Choose the Abilities parameter:', reply_markup=markup)


def send_cost_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [types.KeyboardButton(text=' '),
               types.KeyboardButton(text='🩸'),
               types.KeyboardButton(text='🦴'),
               types.KeyboardButton(text='Main menu')]
    markup.add(*buttons)
    bot.send_message(chat_id, 'Choose the Cost parameter:', reply_markup=markup)


def send_attack_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [types.KeyboardButton(text=' '),
               types.KeyboardButton(text='0'),
               types.KeyboardButton(text='1'),
               types.KeyboardButton(text='2'),
               types.KeyboardButton(text='3'),
               types.KeyboardButton(text='4+'),
               types.KeyboardButton(text='Main menu')]
    markup.add(*buttons)
    bot.send_message(chat_id, 'Choose the Attack parameter:', reply_markup=markup)


def send_health_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    buttons = [types.KeyboardButton(text='1'),
               types.KeyboardButton(text='2'),
               types.KeyboardButton(text='3+'),
               types.KeyboardButton(text='Main menu')]
    markup.add(*buttons)
    bot.send_message(chat_id, 'Choose the Health parameter:', reply_markup=markup)


bot.polling()
