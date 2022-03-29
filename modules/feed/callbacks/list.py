from pprint import pprint
from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext

from modules.base import states as base_states
from modules.base.render import get_start_message
from modules.base.requests import get_token_or_refresh
from modules.feed.requests.list import get_feed_single, post_react, do_feed_report
from modules.posts.requests.create import get_feed
from modules.shops.states import SHOP_DETAILS
from modules import shops
from modules.welcome import keyboards as welcome_keyboards
from modules.welcome import states as welcome_states
from ..keyboards.list import reply_keyboard, get_feed_inline_keyboard_markup
from ..states import *
from ..render import render_feed, render_feed_back, render_report_options_feed_inline


report_options = [
    (1, 'Desnudos'),
    (2, 'Violencia'),
    (3, 'Suicidio'),
    (4, 'Informacion Falsa'),
    (5, 'Spam'),
    (6, 'Lenguaje que incita al odio'),
    (7, 'Terrorismo'),
    (8, 'Otro'),
]

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


def post_report(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    feed_id = query.data.split('-')[-1]
    update.callback_query.answer()
    
    feed = {'id': feed_id}
    render_report_options_feed_inline(update, feed)


def post_report_back(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    feed_id = query.data.split('-')[-1]

    token = get_token_or_refresh(context.user_data)
    feed = get_feed_single(token, feed_id)
    
    if feed:
        update.callback_query.answer()
        render_feed_back(update, feed)
    else:
        update.callback_query.answer(
            text="Este post no esta disponible"
        )


def report(update: Update, context: CallbackContext):
    query = update.callback_query.data
    query = query.split('-')

    report_option = int(query[-1])
    feed_id = query[-2]

    token = get_token_or_refresh(context.user_data)
    response = do_feed_report(token, feed_id, report_option)

    if response.status_code in (200, 201):
        response = response.json()
        if response['deleted'] == 0:
            feed = response['data']
            render_feed_back(update, feed)

            update.callback_query.answer(
                text=response['msg'],
            )
        else:
            update.callback_query.answer(
                text=response['msg']
            )
    else:
        update.callback_query.answer(
            text="Este post no puede ser reportado porque no esta disponible"
        )