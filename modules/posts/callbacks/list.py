from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext
from modules.base.render import get_start_message
from modules.base.requests import get_token_or_refresh

from modules.posts import keyboards
from modules.welcome import keyboards as welcome_keyboards
from ..states import *
from ..requests.list import get_posts
from ..render import render_post


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    token = get_token_or_refresh(user_data)

    posts, count = get_posts(token, page=1)

    if count > 0:
        user_data['current_post'] = posts[0]
        user_data['current_post_page'] = 1
        user_data['count_posts'] = count

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        render_post(
            update, posts[0], markup=markup,
            current_page=user_data['current_post_page'],
            pages=count
        )
    else:
        user_data['count_posts'] = 0
        user_data.pop('current_post', '')

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard_empty,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        update.message.reply_text(
            'No hay estados que mostrar',
            reply_markup=markup
        )

    return POST_LIST


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
    return POST_LIST_BACK


def prev(update: Update, context: CallbackContext):
    user_data = context.user_data

    
    if user_data['count_posts'] == 0:
        update.message.reply_text(
            "Estas en la primera pagina y al parecer no has hecho posts"
        )
    elif user_data['current_post_page'] == 1:
        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )
        render_post(
            update, user_data['current_post'],
            markup=markup,
            current_page=user_data['current_post_page'],
            pages=user_data['count_posts']
        )
    else:
        token = get_token_or_refresh(user_data)
        current_page = user_data['current_post_page']

        posts, count = get_posts(token, page=current_page - 1)

        user_data['current_post'] = posts[0]
        user_data['current_post_page'] -= 1
        user_data['count_posts'] = count

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        render_post(
            update, posts[0], markup=markup,
            current_page=user_data['current_post_page'],
            pages=count
        )


def next(update: Update, context: CallbackContext):
    user_data = context.user_data

    if user_data['count_posts'] == 0:
        update.message.reply_text(
            "Estas en la primera pagina y al parecer no has posteado nada"
        )
    elif user_data['current_post_page'] == user_data['count_posts']:
        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )
        render_post(
            update, user_data['current_post'],
            markup=markup,
            current_page=user_data['current_post_page'],
            pages=user_data['count_posts']
        )
    else:
        token = get_token_or_refresh(user_data)
        current_page = user_data['current_post_page']

        posts, count = get_posts(token, page=current_page + 1)

        user_data['current_post'] = posts[0]
        user_data['current_post_page'] += 1
        user_data['count_posts'] = count

        markup = ReplyKeyboardMarkup(
            keyboards.list.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        render_post(
            update, posts[0], markup=markup,
            current_page=user_data['current_post_page'],
            pages=count
        )