import pprint

from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode
)
from telegram.ext import CallbackContext

from modules.base.requests import get_token_or_refresh
from modules.base.states import BACK
from modules.base.render import render_send_location_help
from modules.shops.requests import base
from modules.shops import keyboards
from modules import welcome
from utils.helpers import get_unique_filename
from ..states import *
from ..requests.base import do_shop_register


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    token = get_token_or_refresh(user_data)

    if not base.is_shop_created(token['access']):
        markup = ReplyKeyboardMarkup(
            keyboards.create.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
        )
        update.message.reply_text(
            '¡Empecemos registrando tu tienda 🏬!',
            parse_mode=ParseMode.MARKDOWN
        )
        update.message.reply_text(
            "¿Cual es el nombre de tu tienda?",
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN
        )

        return SHOP_CREATE

    else:
        markup = ReplyKeyboardMarkup(
            keyboards.edit.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )

        update.message.reply_text(
            "Visualiza tu tienda desde aqui y cambia algunas cosas",
            reply_markup=markup
        )

        return SHOP_EDIT


def name(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    name = update.message.text
    user_data["shop"]["name"] = name

    update.message.reply_text(
        "Escribe una descripción para tu tienda 👇",
        parse_mode=ParseMode.MARKDOWN
    )

    return SHOP_DESCRIPTION


def description(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    description = update.message.text
    user_data["shop"]["description"] = description

    markup = ReplyKeyboardMarkup(
        keyboards.create.reply_keyboard_back,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    update.message.reply_text(
        "¡Agrega una foto al perfil de tu tienda!\n\n"
        "👇 Presiona el botón en forma de clip📎 y selecciona una foto",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return SHOP_LOGO


def logo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    
    logo_path = get_unique_filename()
    logo_file = update.message.photo[-1].get_file()
    logo_file.download(logo_path)

    user_data["shop"]["logo"] = logo_path

    update.message.reply_text(
        "¿Donde esta ubicada tu tienda?!\n\n"
        "\t\t\tLa ubicación es solicitada para que los usuarios cercanos puedan encontrar lo que vendes\n\n"
        "👇 Presiona el botón en forma de clip📎, selecciona ubicación 📍y envia la ubicación de tu tienda",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            keyboards.create.reply_keyboard_back,
            resize_keyboard=True,
            one_time_keyboard=False
        )
    )
    
    return SHOP_LOCATION


def logo_attach(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    logo_path = get_unique_filename()
    file = context.bot.getFile(update.message.document.file_id)
    file.download(logo_path)

    user_data["shop"]["logo"] = logo_path
    
    update.message.reply_text(
        "¿Donde esta ubicada tu tienda?!\n\n"
        "\t\t\tLa ubicación es solicitada para que los usuarios cercanos puedan encontrar lo que vendes\n\n"
        "👇 Presiona el botón en forma de clip📎, selecciona ubicación 📍y envia la ubicación de tu tienda",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            keyboards.create.reply_keyboard_back,
            resize_keyboard=True,
            one_time_keyboard=False
        )
    )
    
    return SHOP_LOCATION


def skip_logo(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        "No hay problema, puedes configurar la foto de tu tienda luego\n"
    )
    update.message.reply_text(
        "¿Donde esta ubicada tu tienda?!\n\n"
        "\t\t\tLa ubicación es solicitada para que los usuarios cercanos puedan encontrar tus productos\n\n"
        "👇 Presiona el botón en forma de clip📎, selecciona ubicación 📍y envia la ubicación de tu tienda",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=ReplyKeyboardMarkup(
            keyboards.create.reply_keyboard_back,
            resize_keyboard=True,
            one_time_keyboard=False
        )
    )

    return SHOP_LOCATION


def location(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    location = update.message.location
    location = [location.latitude, location.longitude]

    user_data["shop"]["location"] = {
        "type": "Point",
        "coordinates": location
    }
    token = get_token_or_refresh(user_data)
    shop = do_shop_register(token, user_data["shop"].copy())

    if "logo" in user_data["shop"]:
        shop["local_logo"] = user_data["shop"]["logo"]

    user_data["shop"] = shop

    markup = ReplyKeyboardMarkup(
        keyboards.main.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    update.message.reply_text(
        "Tu tienda 🏬 ha sido registrada exitosamente",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return END_SHOP_REGISTRATION


def skip_location(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    
    token = get_token_or_refresh(user_data)
    shop = do_shop_register(token, user_data["shop"].copy())

    if "logo" in user_data["shop"]:
        shop["local_logo"] = user_data["shop"]["logo"]
    
    user_data["shop"] = shop

    markup = ReplyKeyboardMarkup(
        keyboards.main.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False
    )
    update.message.reply_text(
        "No hay problema, puedes configurar la ubicación de tu tienda luego\n"
    )
    update.message.reply_text(
        "Tu tienda 🏬 ha sido registrada exitosamente",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )
    return END_SHOP_REGISTRATION


def back(update: Update, context: CallbackContext):

    welcome.callbacks.start_app(update, context)

    return BACK


def test(update: Update, context: CallbackContext) -> str:
    print("prueba en main shop")