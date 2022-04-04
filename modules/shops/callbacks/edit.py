import pprint
from emoji import emojize
import flag

from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext

from modules.base.requests import get_token_or_refresh
from modules.base.states import BACK
from modules.base.render import render_send_location_help
from modules.shops import keyboards, callbacks
from utils.helpers import get_text_validated, get_unique_filename
from ..states import *
from ..requests.base import do_shop_logo_update, do_shop_update
from ..render import show_shop


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    show_shop(update, user_data['shop'], markup=markup)

    return SHOP_EDIT


def navigate_to_edit_currency(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    currencies = [
        (':ar:', 'ARS'),
        (':bo:', 'BOB'),
        (':br:', 'BRL'),
        (':cl:', 'CLP'),
        (':co:', 'COP'),
        (':cr:', 'CRC'),
        (':cu:', 'CUP'),
        (':do:', 'DOP'),
        (':sv:', 'SVC'),
        (':gt:', 'GTQ'),
        (':ht:', 'HTG'),
        (':hn:', 'HNL'),
        (':mx:', 'MXN'),
        (':ni:', 'NIO'),
        (':pa:', 'PAB'),
        (':py:', 'PYG'),
        (':pe:', 'PEN'),
        (':uy:', 'UYU'),
        (':ve:', 'VES'),
        (':us:', 'USD'),
        (':cn:', 'CNY')
    ]

    currencies_text = "*Monedas disponibles*\n"

    for country_code, code in currencies:
        currencies_text += emojize(f":point_right: ", use_aliases=True) + flag.flag(country_code) + f"{code}\n"
    
    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard_currency,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    text = "\nEscribe el codigo de la moneda en la cual estaran basados los precios de tus productos :point_down:"
    text = emojize(text, use_aliases=True)

    update.message.reply_text(
        currencies_text + text,
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SHOP_EDIT_CURRENCY


def back(update: Update, context: CallbackContext) -> str:
    callbacks.settings.navigate_to_self(update, context)
    return SHOP_EDIT_BACK


def back_currency(update: Update, context: CallbackContext) -> str:
    callbacks.settings.navigate_to_self(update, context)
    return SHOP_EDIT_CURRENCY_BACK


def back_to_edit_choosing(update: Update, context: CallbackContext) -> str:
    navigate_to_self(update, context)
    return SHOP_EDIT_CHOOSING


def name(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['shop_edit_field'] = 'name'

    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard_back,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    update.message.reply_text(
        'Escriba el nombre de tu tienda 👇',
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SHOP_EDIT_TYPING


def description(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['shop_edit_field'] = 'description'

    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard_back,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    update.message.reply_text(
        'Escribe una descripción para tu tienda 👇',
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SHOP_EDIT_TYPING


def logo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['shop_edit_field'] = 'logo'
    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard_back,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    update.message.reply_text(
        "¡Agrega una foto al perfil de tu tienda!\n\n"
        "👇 Presiona el boton en forma de clip📎 y selecciona una foto",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SHOP_EDIT_TYPING


def location(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['shop_edit_field'] = 'location'

    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard_back,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    update.message.reply_text(
        "¿Donde esta ubicada tu tienda?!\n\n"
        "👇 Presiona el botón en forma de clip📎, selecciona ubicación 📍y envia la ubicación de tu tienda",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=markup
    )

    return SHOP_EDIT_TYPING


def phone_number(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['shop_edit_field'] = 'phone_number'
    
    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard_back,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    update.message.reply_text(
        "Escribe el número de teléfono tu tienda 👇\n\n"
        "El número debe estar en el formato internacional: +(código de país) (código de área) (número de teléfono)\n",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SHOP_EDIT_TYPING


def update_shop(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    field = user_data.pop('shop_edit_field')

    if field == 'name':
        value = get_text_validated(update.message.text, max_length=64)
    else:
        value = get_text_validated(update.message.text, max_length=512)

    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    payload = {field: value}

    token = get_token_or_refresh(user_data)
    shop_id = user_data['shop']['id']

    shop = do_shop_update(token, shop_id, payload)
    
    if shop:
        user_data['shop'] = shop
        show_shop(update, shop, markup=markup)
    else:
        show_shop(update, user_data['shop'], markup=markup)
        update.message.reply_text(
            'El formato del número de teléfono no es valido\n',
        )

    return SHOP_EDIT_CHOOSING


def update_logo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    _ = user_data.pop('shop_edit_field', None)

    logo_path = get_unique_filename()
    logo_file = update.message.photo[-1].get_file()
    logo_file.download(logo_path)

    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    token = get_token_or_refresh(user_data)
    shop_id = user_data['shop']['id']

    response = do_shop_logo_update(shop_id, logo_path, token)
    shop = response['data']
    user_data['shop'] = shop
    show_shop(update, shop, markup=markup)

    return SHOP_EDIT_CHOOSING


def update_logo_attach(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        f"Debes subir una foto!\n\n"
        f"Asegurate de estar enviando la foto como imagen y no como archivo adjunto",
        parse_mode=ParseMode.MARKDOWN,
    )


def update_location(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    _ = user_data.pop('shop_edit_field', None)
    location = update.message.location
    location = [location.latitude, location.longitude]

    location = {
        "type": "Point",
        "coordinates": location
    }

    payload = {'location': location}
    markup = ReplyKeyboardMarkup(
        keyboards.edit.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    token = get_token_or_refresh(user_data)
    shop_id = user_data['shop']['id']

    shop = do_shop_update(token, shop_id, payload)
    user_data['shop'] = shop
    show_shop(update, shop, markup=markup)

    return SHOP_EDIT_CHOOSING


def update_currency(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    token = get_token_or_refresh(user_data)

    currencies = [
        (':ar:', 'ARS'),
        (':bo:', 'BOB'),
        (':br:', 'BRL'),
        (':cl:', 'CLP'),
        (':co:', 'COP'),
        (':cr:', 'CRC'),
        (':cu:', 'CUP'),
        (':do:', 'DOP'),
        (':sv:', 'SVC'),
        (':gt:', 'GTQ'),
        (':ht:', 'HTG'),
        (':hn:', 'HNL'),
        (':mx:', 'MXN'),
        (':ni:', 'NIO'),
        (':pa:', 'PAB'),
        (':py:', 'PYG'),
        (':pe:', 'PEN'),
        (':uy:', 'UYU'),
        (':ve:', 'VES'),
        (':us:', 'USD'),
        (':cn:', 'CNY')
    ]

    currency = update.message.text
    currency = currency.upper()

    if currency in [curr[1] for curr in currencies]:
        shop_id = user_data['shop']['id']
        shop = do_shop_update(token, shop_id, {'currency': currency})
        user_data['shop'] = shop

        show_shop(update, shop)
        callbacks.settings.navigate_to_self(update, context)
        return SHOP_EDIT_CURRENCY_BACK
    
    else:
        currencies_text = "*Monedas disponibles*\n"

        for country_code, code in currencies:
            currencies_text += emojize(f":point_right: ", use_aliases=True) + flag.flag(country_code) + f"{code}\n"

        text = "\nEscribe el codigo de la moneda en la cual estaran basados los precios de tus productos :point_down:"
        text = emojize(text, use_aliases=True)
        
        update.message.reply_text(
            currencies_text + text,
            parse_mode=ParseMode.MARKDOWN
        )
