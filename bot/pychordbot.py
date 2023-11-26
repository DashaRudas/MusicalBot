import telebot
import pychord
import logging

from telebot import types
from .messages import *

BOT_TOKEN = '6819135404:AAFXDRXfyBjd0vrW24aPA0JthTY_ktaSWGU'

CHORD_REGEX = "\[\S+\]"
COMPOSE_REGEX = "\{([A-Z#b]|\s)+\}"


bot = telebot.TeleBot(BOT_TOKEN, parse_mode="MARKDOWN")
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)  # Outputs debug messages to console.


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    logger.info(f"/start command from {message.from_user.username}")
    bot.send_message(message.chat.id, WELCOME_MESSAGE)


@bot.message_handler(commands=['help'])
def send_help(message: types.Message):
    logger.info(f"/help command from {message.from_user.username}")
    bot.send_message(message.chat.id, HELP_MESSAGE)


@bot.message_handler(commands=['chord'])
def send_chord(message: types.Message):
    logger.info(f"/chord command from {message.from_user.username}")
    bot.send_message(message.chat.id, CHORD_MESSAGE)


@bot.message_handler(commands=['compose'])
def send_compose(message: types.Message):
    logger.info(f"/compose command from {message.from_user.username}")
    bot.send_message(message.chat.id, COMPOSE_MESSAGE)


@bot.message_handler(regexp=CHORD_REGEX)
def send_chord_analysis(message: types.Message):
    logger.info(f"Chord analysis request from {message.from_user.username}")
    try:
        ch = pychord.Chord(message.text[1:-1])
        text = get_chord_analysis_message(ch)
        url = get_chord_image_url(ch)
        bot.send_photo(message.chat.id, url, caption=text, parse_mode="MARKDOWN",
                       reply_to_message_id=message.message_id)
    except Exception as e:
        logger.exception(e)
        bot.reply_to(message, f"*{str(e)}*", parse_mode="MARKDOWN")


@bot.message_handler(regexp=COMPOSE_REGEX)
def send_compose_analysis(message: types.Message):
    logger.info(f"Compose analysis request from {message.from_user.username}")
    try:
        notes = message.text[1:-1].upper().split()
        text = get_compose_analysis_message(notes)
        bot.reply_to(message, text, parse_mode="MARKDOWN")
    except Exception as e:
        logger.exception(e)
        bot.reply_to(message, f"*{str(e)}*", parse_mode="MARKDOWN")


bot.infinity_polling(skip_pending=True)
