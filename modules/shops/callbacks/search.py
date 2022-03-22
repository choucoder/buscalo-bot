import pprint

from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext
from modules.base.render import get_shop_section_help, get_shop_settings_section_help

from modules.base.requests import get_token_or_refresh
from modules.base.states import BACK
from modules.shops.render import show_shop
from modules.shops.requests import base
from modules.shops import keyboards, callbacks
from modules import welcome
from modules import products
from ..states import *


def navigate_to_self(update: Update, context: CallbackContext, shop_id=None) -> str:
    user_data = context.user_data

    update.message.reply_text(
        "...",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardRemove()
    )

    token = get_token_or_refresh(user_data)
    shop = base.get_shop(token, shop_id)

    if shop:
        markup = ReplyKeyboardMarkup(
            keyboards.search.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )
        update.message.reply_text(
            "Tienda encontrada",
            reply_markup=markup
        )
        markup = keyboards.search.get_shop_contact_inline_markup(shop)
        show_shop(update, shop, markup=markup)
        return SHOP_SEARCH

    else:
        update.message.reply_text(
            f"La tienda con el id `{shop_id}` no existe",
            parse_mode=ParseMode.MARKDOWN
        )
        products.callbacks.search.navigate_to_self(update, context)


def back(update: Update, context: CallbackContext) -> str:
    products.callbacks.search.navigate_to_self(update, context)
    return SHOP_SEARCH_BACK


def navigate_to_view_products(update: Update, context: CallbackContext) -> str:
    pass