import pprint
from threading import local
import time

from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext
from modules.base.render import get_start_message

from modules.base.requests import get_token_or_refresh
from modules.shops.render import show_shop
from modules.shops.requests import base
from modules.shops import keyboards
from modules.welcome import keyboards as welcome_keyboards
from ..states import *
from modules.base import states as base_states


def navigate_to_self(update: Update, context: CallbackContext, show=True) -> str:
    user_data = context.user_data

    token = get_token_or_refresh(user_data)    
    shop = base.is_shop_created(token['access'])

    if not shop:
        markup = ReplyKeyboardMarkup(
            keyboards.create.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
            input_field_placeholder='Escribe el nombre de tu tienda'
        )
        update.message.reply_text(
            'Empecemos registrando tu tienda'
        )
        update.message.reply_text(
            "Cual es el nombre de tu tienda?",
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN
        )
        user_data["shop"] = {}

        return SHOP_CREATE

    else:
        user_data['shop'] = shop
        local_logo = user_data["shop"].get("local_logo", None)
        
        if local_logo:
            user_data['shop']['local_logo'] = local_logo
        
        markup = ReplyKeyboardMarkup(
            keyboards.main.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        if show:
            show_shop(update, user_data['shop'])
            update.message.reply_text(
                "Bienvenido a la seccion de tu tienda",
                reply_markup=markup
            )
        else:
            update.message.reply_text(
                'Seccion de tu tienda',
                reply_markup=markup
            )

        return SHOP_MAIN


def description(update: Update, context: CallbackContext) -> str:
    pass

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

    # token = get_token_or_refresh(user_data)

    return base_states.BACK
