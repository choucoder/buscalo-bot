from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode
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
        'Escribe el nombre del producto 👇',
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return PRODUCT_CREATE


def name(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    name = update.message.text
    user_data['product_cache']['name'] = name

    update.message.reply_text(
        "Escribe los detalles acerca del producto 👇",
        parse_mode=ParseMode.MARKDOWN
    )

    return PRODUCT_DETAILS


def details(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    details = update.message.text

    user_data['product_cache']['details'] = details

    update.message.reply_text(
        'Ingresa el precio del producto en tu moneda local o en $ 👇\n\n'
        "👉 Usa la coma ',' para separar los decimales\n",
        parse_mode=ParseMode.MARKDOWN
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
            "¡Agrega una foto de tu producto!\n\n"
            "👇 Presiona el boton en forma de clip📎 y selecciona una foto",
            reply_markup=markup
        )

        return PRODUCT_PHOTO

    except (TypeError, ValueError) as e:        
        update.message.reply_text(
            'Ingresa el precio del producto en tu moneda local o en $ 👇\n\n'
            "👉 Usa la coma ',' para separar los decimales\n",
            parse_mode=ParseMode.MARKDOWN
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
        '¡Producto registrado exitosamente!'
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
        '¡Producto registrado exitosamente!'
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
        '¡Producto registrado exitosamente!'
    )
    shops.callbacks.main.navigate_to_self(update, context, show=False)

    return PRODUCT_END_REGISTRATION


def back(update: Update, context: CallbackContext) -> str:
    shops.callbacks.main.navigate_to_self(update, context)
    return PRODUCT_CREATE_BACK