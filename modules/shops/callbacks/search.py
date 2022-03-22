import pprint

from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext
from modules.base.render import get_shop_section_help, get_shop_settings_section_help

from modules.base.requests import get_token_or_refresh
from modules.base.states import BACK
from modules.products.render import render_product
from modules.products.requests.list import get_products
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

    shop = user_data.pop('qs_shop', None)
    
    if not shop:
        token = get_token_or_refresh(user_data)
        shop = base.get_shop(token, shop_id)

    if shop:
        user_data['qs_shop'] = shop
        markup = ReplyKeyboardMarkup(
            keyboards.search.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )
        update.message.reply_text(
            "Resultados de busqueda",
            reply_markup=markup
        )
        markup = keyboards.search.get_shop_contact_inline_markup(shop)
        show_shop(update, shop, markup=markup, hidden_ws=True)
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
    user_data = context.user_data

    shop = user_data['qs_shop']
    token = get_token_or_refresh(user_data)

    products, count = get_products(token, shop['id'], page=1)

    if count > 0:
        user_data['qs_current_product'] = products[0]
        user_data['qs_current_product_page'] = 1
        user_data['qs_count_products'] = count

        markup = ReplyKeyboardMarkup(
            keyboards.search.reply_keyboard_view_products,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        render_product(
            update, products[0], markup=markup,
            current_page=user_data['qs_current_product_page'],
            pages=user_data['qs_count_products']
        )

    else:
        user_data['qs_count_products'] = 0

        markup = ReplyKeyboardMarkup(
            keyboards.search.reply_keyboard_view_products_empty,
            resize_keyboard=True,
            one_time_keyboard=False
        )
        update.message.reply_text(
            'No hay productos que mostrar\n',
            reply_markup=markup
        )

    return SHOP_SEARCH_VIEW_PRODUCTS


def back_to_shop_search(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    shop = user_data['qs_shop']
    navigate_to_self(update, context, shop_id=shop['id'])
    return SHOP_SEARCH_VIEW_PRODUCTS_BACK


def prev_product(update: Update, context: CallbackContext):
    user_data = context.user_data

    if user_data['qs_count_products'] == 0:
        update.message.reply_text(
            "Estas en la primera pagina y al parecer no has registrado productos"
        )
    elif user_data['qs_current_product_page'] == 1:
        render_product(
            update, user_data['qs_current_product'],
            current_page=user_data['qs_current_product_page'],
            pages=user_data['qs_count_products']
        )
    else:
        token = get_token_or_refresh(user_data)
        shop_id = user_data['qs_shop']['id']
        current_page = user_data['qs_current_product_page']

        products, count = get_products(token, shop_id, page=current_page - 1)

        user_data['qs_current_product'] = products[0]
        user_data['qs_current_product_page'] -= 1
        user_data['qs_count_products'] = count

        render_product(
            update, products[0], markup=None,
            current_page=user_data['qs_current_product_page'],
            pages=user_data['qs_count_products']
        )


def next_product(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    if user_data['qs_count_products'] == 0:
        update.message.reply_text(
            "Estas en la primera pagina y al parecer no has registrado productos"
        )
    elif user_data['qs_current_product_page'] == user_data['qs_count_products']:
        render_product(
            update, user_data['qs_current_product'],
            current_page=user_data['qs_current_product_page'],
            pages=user_data['qs_count_products']
        )
    else:
        token = get_token_or_refresh(user_data)
        shop_id = user_data['qs_shop']['id']
        current_page = user_data['qs_current_product_page']

        products, count = get_products(token, shop_id, page=current_page + 1)

        user_data['qs_current_product'] = products[0]
        user_data['qs_current_product_page'] += 1
        user_data['qs_count_products'] = count

        render_product(
            update, products[0],
            current_page=user_data['qs_current_product_page'],
            pages=user_data['qs_count_products']
        )