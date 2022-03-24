from pprint import pprint
from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext

from modules.base import states as base_states
from modules.base.render import get_start_message
from modules.base.requests import get_token_or_refresh
from modules.feed.requests.list import post_react
from modules.posts.requests.create import get_feed
from modules.shops.states import SHOP_DETAILS
from modules import shops
from modules.welcome import keyboards as welcome_keyboards
from modules.welcome import states as welcome_states
from ..keyboards.list import reply_keyboard, get_feed_inline_keyboard_markup
from ..states import *
from ..render import render_feed


def navigate_to_self(update: Update, context: CallbackContext, swipe_down=True) -> str:
    user_data =context.user_data

    markup = ReplyKeyboardMarkup(
        reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    if swipe_down:
        token = get_token_or_refresh(user_data)
        update.message.reply_text(
            "Aqui puedes deslizar para ver estados y postearlos subiendo "
            "una foto con subtítulo o selecionando la opción ➕ Nuevo estado",
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN
        )

        response = get_feed(token)

        if response:
            feed = response[0]
            user_data['post'] = feed['post']
            user_data['feed'] = feed
            markup = get_feed_inline_keyboard_markup(feed)
            render_feed(update, feed, markup=markup)
        else:
            user_data.pop('post', None)
            user_data.pop('feed', None)
            update.message.reply_text(
                'No hay estados disponibles para mostrar'
            )
    else:
        shop_back = user_data.pop('shop_back', False)
        if shop_back:
            update.message.reply_text(
                "Aqui puedes deslizar para ver estados y postearlos subiendo "
                "una foto con subtítulo o selecionando la opción ➕ Nuevo estado",
                reply_markup=markup,
                parse_mode=ParseMode.MARKDOWN
            )
            feed = user_data['feed']
            markup = get_feed_inline_keyboard_markup(feed)
            render_feed(update, feed, markup=markup)

    return FEED


def swipe_down(update: Update, context: CallbackContext):
    user_data =context.user_data
    token = get_token_or_refresh(user_data)

    response = get_feed(token)

    if response:
        feed = response[0]
        user_data['post'] = feed['post']
        user_data['feed'] = feed
        markup = get_feed_inline_keyboard_markup(feed)
        render_feed(update, feed, markup=markup)
    else:
        user_data.pop('post', None)
        user_data.pop('feed', None)
        update.message.reply_text(
            'No hay estados disponibles para mostrar'
        )


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

    return FEED_BACK


def post_like(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    token = get_token_or_refresh(user_data)

    query = update.callback_query
    post_id = query.data.split('-')[-1]

    message = post_react(token, post_id)

    query.answer(text=message)


def navigate_to_shop_details(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    post = user_data.get('post', None)

    if post and post['shop']:
        shops.callbacks.details.navigate_to_self(update, context, show_contact_keyboard=True)
        return SHOP_DETAILS
    else:
        update.message.reply_text(
            'El estado no fue publicado por una tienda'
        )