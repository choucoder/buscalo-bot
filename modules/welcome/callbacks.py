from urllib.parse import uses_relative
from emoji import emojize

from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode
)
from telegram.ext import CallbackContext
from modules.base.render import get_start_message

from modules.base.requests import get_token_or_refresh, get_user
from .keyboards import welcome_reply_keyboard
from modules.base.states import WELCOME
from .states import *

# External Keyboard imports
from modules.feed.keyboards.list import reply_keyboard as feed_reply_keyboard


def start_app(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    markup = ReplyKeyboardMarkup(
        welcome_reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        get_start_message(),
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    token = get_token_or_refresh(user_data)
    user_data['user'] = get_user(token)

    return WELCOME