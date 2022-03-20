from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext

from modules.products import keyboards, callbacks
from modules import shops
from utils.helpers import get_unique_filename
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
        'Seleccione el campo a editar del producto: ',
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
        'Escriba el nuevo nombre del producto: ',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PRODUCT_EDIT_TYPING


def details(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['product_edit_field'] = 'details'

    update.message.reply_text(
        'Ingrese los detalles del producto: ',
        reply_markup=ReplyKeyboardRemove()
    )

    return PRODUCT_EDIT_TYPING


def price(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['product_edit_field'] = 'price'

    update.message.reply_text(
        'Ingrese el nuevo precio del producto: ',
        reply_markup=ReplyKeyboardRemove()
    )

    return PRODUCT_EDIT_TYPING


def photo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['product_edit_field'] = 'photo'

    update.message.reply_text(
        'Suba la nueva foto del producto: ',
        reply_markup=ReplyKeyboardRemove()
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
        payload['name'] = value

    elif field == 'details':
        payload['details'] = value
    else:
        price = value.replace(',', '.')
        payload['price'] = price

    token = user_data['token']
    product_id = user_data['current_product']['id']

    product = do_update(token, payload, product_id)
    
    if product:
        user_data['current_product'] = product

    render_product(update, user_data['current_product'], markup=markup)

    return PRODUCT_EDIT_CHOOSING


def update_photo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    photo_path = get_unique_filename()
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(photo_path)

    _ = user_data.pop('product_edit_field')
    token = user_data['token']
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
    user_data = context.user_data

    photo_path = get_unique_filename()
    file = context.bot.getFile(update.message.document.file_id)
    file.download(photo_path)

    _ = user_data.pop('product_edit_field')
    token = user_data['token']
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