from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext
from modules.base.requests import get_token_or_refresh

from modules.products import keyboards, callbacks
from modules import shops
from utils.helpers import get_text_validated, get_unique_filename
from ..states import *
from ..requests.edit import do_update, do_photo_update
from ..render import render_product


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    # obtener el producto de mi tienda y guardarlo

    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    update.message.reply_text(
        'Selecciona una opción 👇',
        reply_markup=markup
    )

    return PRODUCT_EDIT


def back(update: Update, context: CallbackContext) -> str:
    callbacks.list.navigate_to_self(update, context)
    return PRODUCT_EDIT_BACK


def name(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['product_edit_field'] = 'name'

    update.message.reply_text(
        'Escribe el nombre del producto 👇',
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN
    )

    return PRODUCT_EDIT_TYPING


def details(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['product_edit_field'] = 'details'

    update.message.reply_text(
        "Escribe los detalles acerca del producto 👇",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN
    )

    return PRODUCT_EDIT_TYPING


def price(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['product_edit_field'] = 'price'

    update.message.reply_text(
        "Ingresa el precio del producto en tu moneda local o en $ 👇\n\n"
        "👉 Usa la coma ',' para separar los decimales\n",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN
    )

    return PRODUCT_EDIT_TYPING


def photo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['product_edit_field'] = 'photo'

    update.message.reply_text(
        "¡Agrega una foto de tu producto!\n\n"
        "👇 Presiona el boton en forma de clip📎 y selecciona una foto",
        reply_markup=ReplyKeyboardRemove(),
        parse_mode=ParseMode.MARKDOWN
    )

    return PRODUCT_EDIT_TYPING


def update_product(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    field = user_data.pop('product_edit_field')
    value = update.message.text

    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    payload = {}

    if field == 'name':
        payload['name'] = get_text_validated(value, max_length=256)

    elif field == 'details':
        payload['details'] = get_text_validated(value, max_length=512)
    else:
        price = value.replace(',', '.')
        try:
            payload['price'] = float(price)
        except:
            pass

    if payload:
        token = get_token_or_refresh(user_data)
        product_id = user_data['current_product']['id']

        product = do_update(token, payload, product_id)
    
        if product:
            user_data['current_product'] = product

        render_product(update, user_data['current_product'], markup=markup)
    else:
        update.message.reply_text(
            "El formato del precio del producto no es valido."
        )
        render_product(update, user_data['current_product'], markup=markup)

    return PRODUCT_EDIT_CHOOSING


def update_photo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    photo_path = get_unique_filename()
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(photo_path)

    _ = user_data.pop('product_edit_field')
    token = get_token_or_refresh(user_data)
    product_id = user_data['current_product']['id']

    product = do_photo_update(token, photo_path, product_id)
    
    if product:
        user_data['current_product'] = product

    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    render_product(update, user_data['current_product'], markup=markup)

    return PRODUCT_EDIT_CHOOSING


def update_photo_attach(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        f"Debes subir una foto!\n\n"
        f"Asegurate de estar enviando la foto como imagen y no como archivo adjunto",
        parse_mode=ParseMode.MARKDOWN,
    )