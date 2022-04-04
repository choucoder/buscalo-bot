from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext
from modules.base.requests import get_token_or_refresh

from modules.shops import keyboards
from modules.base.render import get_start_message
from modules.welcome import keyboards as welcome_keyboards
from ..states import *
from ..requests.list import get_shops
from ..render import render_shop_search


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    token = get_token_or_refresh(user_data)
    shops, count = get_shops(token, page=1)

    if count > 0:
        user_data['current_shop'] = shops[0]
        user_data['current_shop_page'] = 1
        user_data['count_shops'] = count

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )
        update.message.reply_text(
            "...",
            reply_markup=markup
        )

        markup = keyboards.search.get_shop_contact_inline_markup(shops[0])
        render_shop_search(
            update, shops[0], user_data['profile_data'],
            markup=markup,
            current_page=user_data['current_shop_page'],
            pages=user_data['count_shops']
        )
    else:
        user_data['count_shops'] = 0

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard_empty,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        update.message.reply_text(
            'No hay tiendas registradas aun.\n',
            reply_markup=markup
        )

    return SHOP_LIST_ALL


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
    return SHOP_LIST_ALL_BACK


def prev(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    if user_data['count_shops'] == 0:
        update.message.reply_text(
            "No hay tiendas que mostrar"
        )

    elif user_data['current_shop_page'] == 1:
        markup = keyboards.search.get_shop_contact_inline_markup(user_data['current_shop'])
        render_shop_search(
            update, user_data['current_shop'], user_data['profile_data'],
            markup=markup,
            current_page=user_data['current_shop_page'],
            pages=user_data['count_shops']
        )
    else:
        token = get_token_or_refresh(user_data)
        current_page = user_data['current_shop_page']

        shops, count = get_shops(token, page=current_page - 1)

        user_data['current_shop'] = shops[0]
        user_data['current_shop_page'] -= 1
        user_data['count_shops'] = count

        markup = keyboards.search.get_shop_contact_inline_markup(user_data['current_shop'])

        render_shop_search(
            update, shops[0], user_data['profile_data'],
            markup=markup,
            current_page=user_data['current_shop_page'],
            pages=user_data['count_shops']
        )


def next(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    if user_data['count_shops'] == 0:
        update.message.reply_text(
            "No hay tiendas que mostrar"
        )
    elif user_data['current_shop_page'] == user_data['count_shops']:
        markup = keyboards.search.get_shop_contact_inline_markup(user_data['current_shop'])

        render_shop_search(
            update, user_data['current_shop'], user_data['profile_data'],
            markup=markup,
            current_page=user_data['current_shop_page'],
            pages=user_data['count_shops']
        )
    else:
        token = get_token_or_refresh(user_data)
        current_page = user_data['current_shop_page']

        shops, count = get_shops(token, page=current_page + 1)

        user_data['current_shop'] = shops[0]
        user_data['current_shop_page'] += 1
        user_data['count_shops'] = count

        markup = keyboards.search.get_shop_contact_inline_markup(user_data['current_shop'])

        render_shop_search(
            update, shops[0], user_data['profile_data'],
            markup=markup,
            current_page=user_data['current_shop_page'],
            pages=user_data['count_shops']
        )