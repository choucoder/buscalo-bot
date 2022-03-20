import pprint

from telegram import (
    ReplyKeyboardMarkup, Update
)
from telegram.ext import CallbackContext

from modules.shops.render import render_shop
from modules.shops.requests import base
from modules.shops import keyboards
from modules import feed, products
from ..states import *


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    token = user_data['token']

    shop = user_data['post']['shop']
    shop_id = shop['id']
    
    shop = base.get_shop(token, shop_id)
    user_data['post']['shop'] = shop


    markup = ReplyKeyboardMarkup(
        keyboards.details.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    render_shop(update, shop, markup=markup)

    return SHOP_DETAILS


def back(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data['shop_back'] = True
    feed.callbacks.list.navigate_to_self(update, context, swipe_down=False)
    return SHOP_DETAILS_BACK


def view_products(update: Update, context: CallbackContext) -> str:
    products.callbacks.list.navigate_to_self_non_owner(update, context)
    return SHOP_DETAILS_VIEW_PRODUCTS
