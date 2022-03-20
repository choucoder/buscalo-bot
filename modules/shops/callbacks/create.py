import pprint

from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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
            one_time_keyboard=False
        )
        update.message.reply_text(
            "Ups, aun no tienes una tienda. Pues vamos a crearla.\n\n"
            "Cual es el nombre de tu tienda?",
            reply_markup=markup
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
        "Descripcion de tu tienda (que productos/servicios presta): "
    )

    return SHOP_DESCRIPTION


def description(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    description = update.message.text
    user_data["shop"]["description"] = description

    markup = ReplyKeyboardMarkup(
        keyboards.create.reply_keyboard_skip,
        resize_keyboard=True,
        one_time_keyboard=False
    )

    update.message.reply_text(
        "Genial, ahora se de que se trata todo esto\n\n"
        "Sube el logo de tu tienda para que sea mas facil reconocerla:\n"
        "Si quieres omitir este paso, dale al boton /omitir\n",
        reply_markup=markup
    )
    return SHOP_LOGO


def logo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    
    logo_path = get_unique_filename()
    logo_file = update.message.photo[-1].get_file()
    logo_file.download(logo_path)

    user_data["shop"]["logo"] = logo_path

    update.message.reply_text(
        "Ok, tu logo ha sido subido. Pues sigamos!\n"
        "Ingresa la localizacion de tu tienda (direccion del mapa)\n\n"
        "Asi los interesados puedan saber a donde te encuentras ubicado\n"
    )
    render_send_location_help(update)
    
    return SHOP_LOCATION


def skip_logo(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        "No te preocupes, puedes subir el logo de tu tienda luego!\n"
        "Ingresa la localizacion de tu tienda (direccion del mapa)\n\n"
        "Asi los interesados puedan saber a donde te encuentras ubicado\n"
    )

    render_send_location_help(update)

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
        "Listo. Creo que esto es todo. Tu negocio ha sido registrado. Diviertete\n",
        reply_markup=markup
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
        "Listo. Creo que esto es todo. Tu negocio ha sido registrado. Diviertete\n",
        reply_markup=markup
    )

    return END_SHOP_REGISTRATION


def back(update: Update, context: CallbackContext):

    welcome.callbacks.start_app(update, context)

    return BACK


def test(update: Update, context: CallbackContext) -> str:
    print("prueba en main shop")