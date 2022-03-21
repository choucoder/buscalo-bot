from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext

from modules import feed
from modules.base.requests import get_token_or_refresh
from modules.posts import keyboards
from modules.base.states import BACK
from utils.helpers import get_unique_filename
from ..states import *
from ..requests.create import do_post_create
from ..render import render_post


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['post_create'] = {}

    markup = ReplyKeyboardMarkup(
        keyboards.create.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        "¡Sube una foto para publicar un estado!\n\n"
        "👇 Presiona el botón en forma de clip📎, selecciona una foto y agregale un comentario",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return POST_CREATE


def back(update: Update, context: CallbackContext) -> str:
    feed.callbacks.list.navigate_to_self(update, context)
    return POST_CREATE_BACK


def photo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    caption = update.message.caption
    photo_path = get_unique_filename()
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(photo_path)

    user_data['post_create']['text'] = caption
    user_data['post_create']['photo'] = photo_path

    markup = ReplyKeyboardMarkup(
        keyboards.create.publisher_type_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        'Selecciona con que perfil publicar tu estado 👇',
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return POST_CREATE_PUBLISHER_TYPE


def photo_attach(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    caption = update.message.caption
    
    photo_path = get_unique_filename()
    file = context.bot.getFile(update.message.document.file_id)
    file.download(photo_path)

    user_data['post_create']['text'] = caption
    user_data['post_create']['photo'] = photo_path

    markup = ReplyKeyboardMarkup(
        keyboards.create.publisher_type_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        'Selecciona con que perfil publicar tu estado 👇',
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )
    
    return POST_CREATE_PUBLISHER_TYPE


def publisher_type(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    token = user_data['token']

    type = update.message.text
    if "Usuario" in type:
        user_data['post_create']['as_shop'] = False
    else:
        user_data['post_create']['as_shop'] = True

    response = do_post_create(token, user_data['post_create'])

    post = response['data']
    markup = ReplyKeyboardMarkup(
        feed.keyboards.list.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    render_post(update, post)
    update.message.reply_text(
        'El estado ha sido publicado correctamente\n',
        reply_markup=markup
    )

    feed.callbacks.list.navigate_to_self(update, context, swipe_down=False)
    
    return POST_CREATE_BACK


def fast_post_text(update: Update, context: CallbackContext) -> None:
    user_data = context.user_data
    user_data['text'] = update.message.text


def fast_post(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    caption = update.message.caption
    if not caption:
        caption = user_data.pop('text', '')

    photo_path = get_unique_filename()
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(photo_path)

    payload = {
        'text': caption,
        'photo': photo_path,
        'as_shop': False,
    }

    token = get_token_or_refresh(user_data)
    response = do_post_create(token, payload)
    post = response['data']

    render_post(update, post)
    update.message.reply_text(
        'El estado ha sido subido correctamente\n',
    )


def fast_post_attach(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    photo_path = get_unique_filename()
    file = context.bot.getFile(update.message.document.file_id)
    file.download(photo_path)

    caption = update.message.caption
    if not caption:
        caption = user_data.pop('text', '')

    payload = {
        'text': caption,
        'photo': photo_path,
        'as_shop': False,
    }

    token = get_token_or_refresh(user_data)
    response = do_post_create(token, payload)
    post = response['data']

    render_post(update, post)
    update.message.reply_text(
        'El estado ha sido subido correctamente\n',
    )