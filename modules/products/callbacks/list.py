from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext
from modules.base.render import get_product_list_section_help

from modules.products import keyboards
from modules import shops
from ..states import *
from ..requests.list import get_products
from ..render import render_product


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    token = user_data['token']
    shop_id = user_data['shop']['id']

    products, count = get_products(token, shop_id, page=1)

    if count > 0:
        user_data['current_product'] = products[0]
        user_data['current_product_page'] = 1
        user_data['count_products'] = count

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        render_product(
            update, products[0], markup=markup,
            current_page=user_data['current_product_page'],
            pages=user_data['count_products']
        )
        update.message.reply_text(
            get_product_list_section_help(),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        user_data['count_products'] = 0

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard_empty,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        update.message.reply_text(
            'Parece que aun no has agregado productos a tu tienda\n',
            reply_markup=markup
        )

    return PRODUCT_LIST


def navigate_to_self_non_owner(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    token = user_data['token']
    user_data['shop'] = user_data['post']['shop']
    shop_id = user_data['post']['shop']['id']

    products, count = get_products(token, shop_id, page=1)

    if count > 0:
        user_data['current_product'] = products[0]
        user_data['current_product_page'] = 1
        user_data['count_products'] = count

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard_non_owner,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        render_product(
            update, products[0], markup=markup,
            current_page=user_data['current_product_page'],
            pages=user_data['count_products']
        )
    else:
        user_data['count_products'] = 0

        update.message.reply_text(
            'No hay productos que mostrar\n',
            reply_markup=markup
        )

    return PRODUCT_LIST


def back(update: Update, context: CallbackContext) -> str:
    shops.callbacks.main.navigate_to_self(update, context)
    return PRODUCT_LIST_BACK


def back_non_owner(update: Update, context: CallbackContext) -> str:
    shops.callbacks.details.navigate_to_self(update, context)
    return PRODUCT_LIST_BACK


def prev(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    
    if user_data['count_products'] == 0:
        update.message.reply_text(
            "Estas en la primera pagina y al parecer no has registrado productos"
        )
    elif user_data['current_product_page'] == 1:
        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )
        render_product(
            update, user_data['current_product'],
            markup=markup,
            current_page=user_data['current_product_page'],
            pages=user_data['count_products']
        )
    else:
        token = user_data['token']
        shop_id = user_data['shop']['id']
        current_page = user_data['current_product_page']

        products, count = get_products(token, shop_id, page=current_page - 1)

        user_data['current_product'] = products[0]
        user_data['current_product_page'] -= 1
        user_data['count_products'] = count

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        render_product(
            update, products[0], markup=markup,
            current_page=user_data['current_product_page'],
            pages=user_data['count_products']
        )


def prev_non_owner(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    
    if user_data['count_products'] == 0:
        update.message.reply_text(
            "Estas en la primera pagina y al parecer no has registrado productos"
        )
    elif user_data['current_product_page'] == 1:
        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard_non_owner,
            resize_keyboard=True,
            one_time_keyboard=False
        )
        render_product(
            update, user_data['current_product'], markup=markup,
            current_page=user_data['current_product_page'],
            pages=user_data['count_products']
        )

    else:
        token = user_data['token']
        shop_id = user_data['shop']['id']
        current_page = user_data['current_product_page']

        products, count = get_products(token, shop_id, page=current_page - 1)

        user_data['current_product'] = products[0]
        user_data['current_product_page'] -= 1
        user_data['count_products'] = count

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard_non_owner,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        render_product(
            update, products[0], markup=markup,
            current_page=user_data['current_product_page'],
            pages=user_data['count_products']
        )


def next(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    if user_data['count_products'] == 0:
        update.message.reply_text(
            "Estas en la primera pagina y al parecer no has registrado productos"
        )
    elif user_data['current_product_page'] == user_data['count_products']:
        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )
        render_product(
            update, user_data['current_product'],
            markup=markup,
            current_page=user_data['current_product_page'],
            pages=user_data['count_products']
        )
    else:
        token = user_data['token']
        shop_id = user_data['shop']['id']
        current_page = user_data['current_product_page']

        products, count = get_products(token, shop_id, page=current_page + 1)

        user_data['current_product'] = products[0]
        user_data['current_product_page'] += 1
        user_data['count_products'] = count

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        render_product(
            update, products[0], markup=markup,
            current_page=user_data['current_product_page'],
            pages=user_data['count_products']
        )


def next_non_owner(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    if user_data['count_products'] == 0:
        update.message.reply_text(
            "Estas en la primera pagina y al parecer no has registrado productos"
        )
    elif user_data['current_product_page'] == user_data['count_products']:
        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard_non_owner,
            resize_keyboard=True,
            one_time_keyboard=False
        )
        render_product(
            update, user_data['current_product'], markup=markup,
            current_page=user_data['current_product_page'],
            pages=user_data['count_products']
        )

    else:
        token = user_data['token']
        shop_id = user_data['shop']['id']
        current_page = user_data['current_product_page']

        products, count = get_products(token, shop_id, page=current_page + 1)

        user_data['current_product'] = products[0]
        user_data['current_product_page'] += 1
        user_data['count_products'] = count

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard_non_owner,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        render_product(
            update, products[0], markup=markup,
            current_page=user_data['current_product_page'],
            pages=user_data['count_products']
        )
