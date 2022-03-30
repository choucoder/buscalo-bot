import datetime
from typing import Dict
from venv import create

from emoji import emojize
from geopy.distance import geodesic
from telegram import (
    InlineKeyboardMarkup, InputMediaPhoto, Update, ParseMode
)
import requests
from decouple import config
from modules.feed.keyboards.list import get_feed_inline_keyboard_markup, get_feed_report_inline_keyboard_markup

from utils.helpers import get_time_ago


API_URL = config('API_URL')

def render_feed(update: Update, feed: Dict, markup=None) -> None:
    post = feed['post']
    user = post['user']
    shop = post['shop']

    current_date = datetime.datetime.today()
    created_at = datetime.datetime.strptime(post['created_at'].split('.')[0], "%Y-%m-%dT%H:%M:%S")

    ago = get_time_ago(created_at, current_date)

    if post['text']:
        text = post['text'] + "\n\n"
    else:
        text = "\n\n"
    
    if shop:
        text += f":department_store: {shop['name']} {post['ago']}\n"
    else:
        text += f":bust_in_silhouette: {user['first_name']} {user['last_name']} {post['ago']}\n"

    if post['views'] == 1:
        text += f":eye: Visto por: {post['views']} usuario"
    else:
        text += f":eye: Visto por: {post['views']} usuarios"

    text += f"\n\n:heart: {post['reactions']}"

    response = requests.get(f"{API_URL}{post['photo']}")

    if markup:
        update.message.reply_photo(
            caption=emojize(text, use_aliases=True),
            photo=response.content,
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        update.message.reply_photo(
            caption=emojize(text, use_aliases=True),
            photo=response.content,
            parse_mode=ParseMode.MARKDOWN
        )


def render_report_options_feed_inline(update: Update, feed: Dict):
    text = "*Seleccione un problema*\n\n"
    text += "1. Desnudos\n"
    text += "2. Violencia\n"
    text += "3. Suicidio\n"
    text += "4. Informacion Falsa\n"
    text += "5. Spam\n"
    text += "6. Lenguaje que incita al odio\n"
    text += "7. Terrorismo\n"
    text += "8. Otro\n"

    update.callback_query.edit_message_caption(
        text,
        parse_mode=ParseMode.MARKDOWN
    )
    update.callback_query.edit_message_reply_markup(
        get_feed_report_inline_keyboard_markup(feed)
    )


def render_feed_back(update: Update, feed: Dict, user_data):
    post = feed['post']
    user = post['user']
    shop = post['shop']

    current_date = datetime.datetime.today()
    created_at = datetime.datetime.strptime(post['created_at'].split('.')[0], "%Y-%m-%dT%H:%M:%S")

    ago = get_time_ago(created_at, current_date)

    if post['text']:
        text = post['text'] + "\n\n"
    else:
        text = "\n\n"
    
    if shop:
        text += f":department_store: {shop['name']} {post['ago']}\n"
    else:
        text += f":bust_in_silhouette: {user['first_name']} {user['last_name']} {post['ago']}\n"

    if post['views'] == 1:
        text += f":eye: Visto por: {post['views']} usuario"
    else:
        text += f":eye: Visto por: {post['views']} usuarios"

    text += f"\n\n:heart: {post['reactions']}"

    response = requests.get(f"{API_URL}{post['photo']}")

    update.callback_query.edit_message_media(
        InputMediaPhoto(
            response.content,
            caption=emojize(text, use_aliases=True),
            parse_mode=ParseMode.MARKDOWN
        )
    )

    update.callback_query.edit_message_reply_markup(
        get_feed_inline_keyboard_markup(feed, user_data)
    )

    print("feed back")