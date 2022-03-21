from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext

from modules import settings
from modules.base.render import get_start_message
from modules.welcome import keyboards as welcome_keyboards
from utils.helpers import get_unique_filename
from ..states import *


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    markup = ReplyKeyboardMarkup(
        settings.main.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        "Selecciona una opción 👇",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SETTINGS


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

    return SETTINGS_BACK