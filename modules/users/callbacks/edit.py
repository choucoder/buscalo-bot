from datetime import datetime

from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext

from modules import users
from modules import settings
from modules.base.requests import get_token_or_refresh
from modules.base.render import render_send_location_help
from modules.users.render import render_user
from modules.welcome import keyboards as welcome_keyboards
from utils.helpers import get_text_validated, get_unique_filename, calc_age
from ..states import *
from ..requests.edit import *


genders_en = {
    'Masculino': 'Male',
    'Femenino': 'Female',
    'Prefiero no decir': 'Other',
}

def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    markup = ReplyKeyboardMarkup(
        users.keyboards.edit.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )
    render_user(update, user_data['profile_data'], markup=markup)

    return USER_EDIT


def back(update: Update, context: CallbackContext) -> str:
    settings.callbacks.main.navigate_to_self(update, context)
    return USER_EDIT_BACK


def back_to_edit_choosing(update: Update, context: CallbackContext) -> str:
    navigate_to_self(update, context)
    return USER_EDIT_CHOOSING


def first_name(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data['user_edit_field'] = 'first_name'

    markup = ReplyKeyboardMarkup(
        users.keyboards.edit.reply_keyboard_back,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        "¿Cual es tu nombre?",
        reply_markup=markup
    )

    return USER_EDIT_TYPING


def last_name(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data['user_edit_field'] = 'last_name'

    markup = ReplyKeyboardMarkup(
        users.keyboards.edit.reply_keyboard_back,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        "¿Cual es tu apellido?",
        reply_markup=markup
    )

    return USER_EDIT_TYPING


def birthdate(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data['user_edit_field'] = 'birthdate'

    markup = ReplyKeyboardMarkup(
        users.keyboards.edit.reply_keyboard_back,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        f"¿Cual es tu fecha de nacimiento? 📅\n\n"
        "Usa los siguientes formatos: \n"
        "dd-mm-yy Ejemplo: *22-04-1997*\n"
        "dd/mm/yy Ejemplo: *22/04/1997*\n",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return USER_EDIT_TYPING


def gender(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data['user_edit_field'] = 'gender'

    markup = ReplyKeyboardMarkup(
        users.keyboards.edit.reply_keyboard_gender,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder='Genero?'
    )

    update.message.reply_text(
        "¿Cual es tu género?\n\n"
        "Selecciona una de las siguientes opciones 👇👇👇",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return USER_EDIT_TYPING


def photo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data['user_edit_field'] = 'photo'

    markup = ReplyKeyboardMarkup(
        users.keyboards.edit.reply_keyboard_back,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        "¡Agrega una foto tuya o hazte un selfie!\n\n"
        "👇 Presiona el boton en forma de clip📎 y selecciona o hazte una foto",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return USER_EDIT_TYPING


def location(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data['user_edit_field'] = 'location'

    markup = ReplyKeyboardMarkup(
        users.keyboards.edit.reply_keyboard_back,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        f"¿Cual es tu ubicación?\n\n"
        "👇 Presiona el botón en forma de clip📎, selecciona ubicación 📍y envia donde te encuentras",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return USER_EDIT_TYPING


def update_text_fields(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    field = user_data['user_edit_field']
    query = update.message.text

    payload = {}

    if field == 'first_name' or field == 'last_name':
        payload = {
            field: get_text_validated(query, max_length=150),
        }
        if 'first_name' == field:
            msg = 'Tu nombre ha sido actualizado'
        else:
            msg = 'Tu apellido ha sido actualizado'

    elif field == 'gender':
        gender = ' '.join(query.split()[1: ])
        gender = genders_en[gender]

        payload = {
            'gender': gender,
        }
        msg = 'Tu genero ha sido actualizado'

    else:
        _birthdate = query
        separator = "-" if "-" in _birthdate else "/"

        if separator == "-":
            try:
                dt_birthdate = datetime.strptime(_birthdate, "%d-%m-%Y")
                user_age = calc_age(dt_birthdate)

                if user_age > 95:
                    msg = 'No creo que tengas esta edad. Una mas y te baneo'
                elif user_age < 13:
                    msg = 'Tu edad debe ser mayor a 13, que es la edad permitida para usar este bot'
                else:
                    msg = 'Tu fecha de nacimiento ha sido actualizada'
                    _birthdate = '-'.join(_birthdate.split('-')[:: -1])
                    payload = {
                        'birthdate': _birthdate,
                    }

            except:
                msg = 'Formato de fecha invalido'
        else:
            try:
                dt_birthdate = datetime.strptime(_birthdate, "%d/%m/%Y")
                user_age = calc_age(dt_birthdate)

                if user_age > 95:
                    msg = 'No creo que tengas esta edad. Una mas y te baneo'
                elif user_age < 13:
                    msg = 'Tu edad debe ser mayor a 13, que es la edad permitida para usar este bot'
                else:
                    msg = 'Tu fecha de nacimiento ha sido actualizada'
                    _birthdate = '-'.join(_birthdate.split('/')[:: -1])
                    payload = {
                        'birthdate': _birthdate,
                    }
            except:
                msg = 'Formato de fecha invalido'  

    if payload:
        if update.effective_user.username:
            payload['telegram_username'] = update.effective_user.username
            payload['username'] = update.effective_user.username

        token = get_token_or_refresh(user_data)
        user_data['profile_data'] = do_user_update(token, payload)
        
        markup = ReplyKeyboardMarkup(
            users.keyboards.edit.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
        )

        render_user(update, user_data['profile_data'], markup=markup)
        return USER_EDIT_CHOOSING
    else:
        update.message.reply_text(
            msg
        )
        return birthdate(update, context)


def update_photo(update: Update, context: CallbackContext) -> str:
    photo_path = get_unique_filename()
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(photo_path)

    user_data = context.user_data

    token = get_token_or_refresh(user_data)
    user_data['profile_data'] = do_user_photo_update(token, photo_path)

    markup = ReplyKeyboardMarkup(
        users.keyboards.edit.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    render_user(update, user_data['profile_data'], markup=markup)

    return USER_EDIT_CHOOSING


def update_photo_attach(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        f"Debes subir una foto!\n\n"
        f"Asegurate de estar enviando la foto como imagen y no como archivo adjunto",
        parse_mode=ParseMode.MARKDOWN,
    )


def update_location(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    location = update.message.location
    location = [location.latitude, location.longitude]

    payload = {
        'location': {
            'type': 'Point',
            'coordinates': location,
        },
    }

    if update.effective_user.username:
        payload['telegram_username'] = update.effective_user.username
        payload['username'] = update.effective_user.username

    token = get_token_or_refresh(user_data)
    user_data['profile_data'] = do_user_update(token, payload)

    markup = ReplyKeyboardMarkup(
        users.keyboards.edit.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    render_user(update, user_data['profile_data'], markup=markup)
    return USER_EDIT_CHOOSING