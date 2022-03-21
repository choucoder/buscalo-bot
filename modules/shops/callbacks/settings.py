import pprint

from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext
from modules.base.render import get_shop_section_help, get_shop_settings_section_help

from modules.base.requests import get_token_or_refresh
from modules.base.states import BACK
from modules.shops.requests import base
from modules.shops import keyboards, callbacks
from modules import welcome
from ..states import *


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    # token = get_token_or_refresh(user_data)

    markup = ReplyKeyboardMarkup(
        keyboards.settings.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    update.message.reply_text(
        get_shop_settings_section_help(),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SHOP_SETTINGS


def back(update: Update, context: CallbackContext) -> str:
    callbacks.main.navigate_to_self(update, context)
    return SHOP_SETTINGS_BACK