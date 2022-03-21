from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext

from modules import feedback
from modules.base.render import get_start_message
from modules.feedback import keyboards
from modules.welcome import keyboards as welcome_keyboards
from utils.helpers import get_unique_filename
from ..states import *
from ..requests import *


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    markup = ReplyKeyboardMarkup(
        keyboards.create.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder='Escribe tu comentario'
    )

    update.message.reply_text(
        'Escribe tus sugerencia(s) 👇',
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return FEEDBACK


def send(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    text = update.message.text

    token = user_data['token']
    markup = ReplyKeyboardMarkup(
        welcome_keyboards.welcome_reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    response =  send_feedback(token, {"text": text})

    update.message.reply_text(
        "Tu mensaje ha sido enviado a nuestro buzón de sugerencias",
    )

    # return FEEDBACK_BACK


def back(update: Update, context: CallbackContext) -> str:
    markup = ReplyKeyboardMarkup(
        welcome_keyboards.welcome_reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        get_start_message(),
        reply_markup=markup
    )

    return FEEDBACK_BACK