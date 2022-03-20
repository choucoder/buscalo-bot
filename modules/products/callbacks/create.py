from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext
from modules.base.requests import get_token_or_refresh

from modules.products import keyboards
from modules import shops
from modules.base.states import BACK
from modules.products.requests.create import do_product_register
from modules.shops import render
from utils.helpers import get_unique_filename
from ..states import *
from ..requests.create import do_product_register
from ..render import render_product


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['product_cache'] = {}

    markup = ReplyKeyboardMarkup(
        keyboards.create.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        'Registra tus productos en este apartado\n\n'
        'Ingresa el nombre de tu producto: ',
        reply_markup=markup
    )

    return PRODUCT_CREATE


def name(update: Update, context: CallbackContext) -> str:

    user_data = context.user_data
    name = update.message.text
    user_data['product_cache']['name'] = name

    update.message.reply_text(
        "Detalles del producto: "
    )

    return PRODUCT_DETAILS


def details(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    details = update.message.text

    user_data['product_cache']['details'] = details

    update.message.reply_text(
        'Ingresa el precio en $ del producto: \n'
        'Use `,` para separar los decimales. Ejemplo: 450,18.\n'
    )

    return PRODUCT_PRICE


def price(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    price = update.message.text
    price = price.replace(',', '.')

    try:
        user_data['product_cache']['price'] = float(price)

        markup = ReplyKeyboardMarkup(
            keyboards.create.reply_keyboard_skip,
            resize_keyboard=True,
            one_time_keyboard=False,
        )
        update.message.reply_text(
            'Ingresa una foto para tu producto\n'
            'O puedes darle /omitir para ingresarla luego.',
            reply_markup=markup
        )

        return PRODUCT_PHOTO

    except (TypeError, ValueError) as e:
        print(f"E: {e}")
        
        update.message.reply_text(
            'Ups, has ingresado el precio en un formato incorrecto\n\n'
            'Ingresa el precio en $ del producto:\n'
            'Por favor utiliza el siguiente formato 550,19. La `,` separa los decimales',
        )

        return PRODUCT_PRICE


def photo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    photo_path = get_unique_filename()
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(photo_path)

    user_data['product_cache']['photo'] = photo_path

    token = get_token_or_refresh(user_data)
    product = do_product_register(
        token,
        user_data['product_cache'].copy(),
        user_data['shop']['id']
    )
    render_product(update, product)
    update.message.reply_text(
        'El producto ha sido registrado exitosamente'
    )
    shops.callbacks.main.navigate_to_self(update, context, show=False)

    return PRODUCT_END_REGISTRATION


def photo_attach(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    photo_path = get_unique_filename()
    file = context.bot.getFile(update.message.document.file_id)
    file.download(photo_path)
    user_data['product_cache']['photo'] = photo_path

    token = get_token_or_refresh(user_data)
    product = do_product_register(
        token,
        user_data['product_cache'].copy(),
        user_data['shop']['id']
    )
    render_product(update, product)
    update.message.reply_text(
        'El producto ha sido registrado exitosamente'
    )
    shops.callbacks.main.navigate_to_self(update, context, show=False)

    return PRODUCT_END_REGISTRATION


def skip_photo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    token = get_token_or_refresh(user_data)
    product = do_product_register(
        token,
        user_data['product_cache'].copy(),
        user_data['shop']['id']
    )
    render_product(update, product)

    update.message.reply_text(
        'El producto ha sido registrado sin foto exitosamente.'
    )
    shops.callbacks.main.navigate_to_self(update, context, show=False)

    return PRODUCT_END_REGISTRATION


def back(update: Update, context: CallbackContext) -> str:
    shops.callbacks.main.navigate_to_self(update, context)
    return PRODUCT_CREATE_BACK