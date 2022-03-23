from datetime import datetime
from uuid import uuid4
from emoji import emojize
from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, ParseMode
)
from telegram.ext import (
    CallbackContext,
)

from utils.helpers import calc_age, email_is_valid, get_unique_filename
from ..keyboards.create import (
    reply_keyboard_skip, reply_keyboard_accept_conditions,
    reply_keyboard_gender
)
from ..requests.create import do_register_request
from ..states import *
from modules.base.states import WELCOME, USER_REGISTRATION, WELCOME
from modules.welcome.callbacks import start_app
from modules.base.render import get_photo_help, render_send_location_help


genders_en = {
    'Masculino': 'Male',
    'Femenino': 'Female',
    'Prefiero no decir': 'Other',
}

terms_and_conditions = (
    "*Terminos y condiciones*\n\n"
    "Acepto que la información que he suministrado en este bot es "
    "correcta y que soy mayor de 13 años de edad.\n\n"
)


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    user_data['profile_data'] = {
        'telegram_user_id': update.effective_user.id,
        'telegram_chat_id': update.effective_chat.id,
        'telegram_username': update.effective_user.username,
        'username': update.effective_user.username,
    }

    if not user_data['profile_data']['telegram_username']:
        username = str(uuid4()).replace('-', '')[:16]
        username = "none-" + username
        user_data['profile_data']['telegram_username'] = username
        user_data['profile_data']['username'] = username

    user_data['is_registered'] = False
    user_data['level'] = USER_REGISTRATION
    user_data['level_state'] = GENDER
    
    markup = ReplyKeyboardMarkup(
        reply_keyboard_gender,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        "¿Cual es tu género?\n\n"
        "Selecciona una de las siguientes opciones 👇👇👇",
        reply_markup=markup
    )  
    return USER_REGISTRATION


def gender(update: Update, context: CallbackContext) -> str:
    answer = update.message.text
    gender = ' '.join(answer.split()[1: ])
    gender = genders_en[gender]

    user_data = context.user_data
    user_data['profile_data']['gender'] = gender

    user_data['level_state'] = FIRST_NAME

    update.message.reply_text(
        "¿Cual es tu nombre?\n\n",
        reply_markup=ReplyKeyboardRemove(),
    )

    return FIRST_NAME


def first_name(update: Update, context: CallbackContext) -> str:
    answer = update.message.text
    answer = ' '.join([name.capitalize() for name in answer.split()])

    user_data = context.user_data
    user_data['profile_data']['first_name'] = answer
    user_data['level_state'] = LAST_NAME

    name = answer.split()[0]

    update.message.reply_text(
        f"¡Genial, {name}! \n\n"
        f"Ahora, ¿cual es tu apellido?",
    )

    return LAST_NAME


def last_name(update: Update, context: CallbackContext) -> str:
    answer = update.message.text
    answer = ' '.join([name.capitalize() for name in answer.split()])

    user_data = context.user_data
    user_data['profile_data']['last_name'] = answer
    user_data['level_state'] = EMAIL

    name = user_data['profile_data']['first_name'].split()[0]

    update.message.reply_text(
        f"¿Cual es tu fecha de nacimiento {name}? 📅\n\n"
        "Usa los siguientes formatos: \n"
        "dd-mm-yy Ejemplo: *22-04-1997*\n"
        "dd/mm/yy Ejemplo: *22/04/1997*\n",
        parse_mode=ParseMode.MARKDOWN,
    )
    return AGE


def age(update: Update, context: CallbackContext) -> str:
    # formats will be dd-mm-yy or dd/mm/yy Ex. 22/4/1997
    user_data = context.user_data
    birthdate = update.message.text
    separator = "-" if "-" in birthdate else "/"

    name = user_data['profile_data']['first_name'].split()[0]

    if separator == "-":
        try:
            dt_birthdate = datetime.strptime(birthdate, "%d-%m-%Y")
            user_age = calc_age(dt_birthdate)
            
            if user_age > 95:
                update.message.reply_text(
                    "Vamos!, di tu verdadera edad. No exageres"
                )
                update.message.reply_text(
                    f"¿Cual es tu fecha de nacimiento {name}? 📅\n\n"
                    "Usa los siguientes formatos: \n"
                    "dd-mm-yy Ejemplo: *22-04-1997*\n"
                    "dd/mm/yy Ejemplo: *22/04/1997*\n",
                    parse_mode=ParseMode.MARKDOWN,
                )
                return AGE

            elif user_age < 13:
                update.message.reply_text(
                    "Debes tener 13 años en adelante para poder registrarte"
                )
                update.message.reply_text(
                    f"¿Cual es tu fecha de nacimiento {name}? 📅\n\n"
                    "Usa los siguientes formatos: \n"
                    "dd-mm-yy Ejemplo: *22-04-1997*\n"
                    "dd/mm/yy Ejemplo: *22/04/1997*\n",
                    parse_mode=ParseMode.MARKDOWN,
                )
                return AGE

            else:
                update.message.reply_text(
                    f"¡Agrega una foto tuya o hazte un selfie {name}!\n\n"
                    "👇 Presiona el boton en forma de clip📎 y selecciona una foto",
                    parse_mode=ParseMode.MARKDOWN,
                )
                birthdate = '-'.join(birthdate.split('-')[:: -1])
                user_data['profile_data']['birthdate'] = birthdate

                return PHOTO
        except:
            update.message.reply_text(
                'Formato de fecha incorrecto'
            )
            update.message.reply_text(
                f"¿Cual es tu fecha de nacimiento {name}? 📅\n\n"
                "Usa los siguientes formatos: \n"
                "dd-mm-yy Ejemplo: *22-04-1997*\n"
                "dd/mm/yy Ejemplo: *22/04/1997*\n",
                parse_mode=ParseMode.MARKDOWN,
            )
            return AGE
    else:
        try:
            dt_birthdate = datetime.strptime(birthdate, "%d/%m/%Y")
            user_age = calc_age(dt_birthdate)

            if user_age > 95:
                update.message.reply_text(
                    "Vamos!, di tu verdadera edad. No exageres"
                )
                update.message.reply_text(
                    f"¿Cual es tu fecha de nacimiento {name}? 📅\n\n"
                    "Usa los siguientes formatos: \n"
                    "dd-mm-yy Ejemplo: *22-04-1997*\n"
                    "dd/mm/yy Ejemplo: *22/04/1997*\n",
                    parse_mode=ParseMode.MARKDOWN,
                )
                return AGE

            elif user_age < 13:
                update.message.reply_text(
                    "Debes tener 13 años en adelante para poder registrarte"
                )
                update.message.reply_text(
                    f"¿Cual es tu fecha de nacimiento {name}? 📅\n\n"
                    "Usa los siguientes formatos: \n"
                    "dd-mm-yy Ejemplo: *22-04-1997*\n"
                    "dd/mm/yy Ejemplo: *22/04/1997*\n",
                    parse_mode=ParseMode.MARKDOWN,
                )
                return AGE

            else:
                update.message.reply_text(
                    f"¡Agrega una foto tuya o hazte un selfie {name}!\n\n"
                    "👇 Presiona el boton en forma de clip📎 y selecciona una foto",
                    parse_mode=ParseMode.MARKDOWN,
                )
                birthdate = '-'.join(birthdate.split('/')[:: -1])
                user_data['profile_data']['birthdate'] = birthdate

                return PHOTO

        except:
            update.message.reply_text(
                'Formato de fecha incorrecto'
            )
            update.message.reply_text(
                f"¿Cual es tu fecha de nacimiento {name}? 📅\n\n"
                "Usa los siguientes formatos: \n"
                "dd-mm-yy Ejemplo: *22-04-1997*\n"
                "dd/mm/yy Ejemplo: *22/04/1997*\n",
                parse_mode=ParseMode.MARKDOWN,
            )
            return AGE


def email(update: Update, context: CallbackContext) -> str:
    answer = update.message.text
    user_data = context.user_data
    name = user_data['profile_data']['first_name'].split()[0]

    if email_is_valid(answer):
        user_data['profile_data']['email'] = answer
        user_data['level_state'] = PHOTO

        update.message.reply_text(
            f"¡Agrega una foto tuya o hazte un selfie {name}!\n\n"
            "👇 Presiona el boton en forma de clip📎 y selecciona una foto",
            parse_mode=ParseMode.MARKDOWN,
        )

        return PHOTO
    else:
        update.message.reply_text(
            "El correo electrónico ingresado no es valido\n"
            "Por favor, ingrese una dirección de correo valida",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=reply_keyboard_skip,
                resize_keyboard=True,
                one_time_keyboard=False,
            ),
        )


def skip_email(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data['level_state'] = PHOTO

    name = user_data['profile_data']['first_name'].split()[0]

    update.message.reply_text(
        "No hay problema, puedes configurarlo en otro momento"
    )
    update.message.reply_text(
        f"¡Agrega una foto tuya o hazte un selfie {name}!\n\n"
        "👇 Presiona el boton en forma de clip📎 y selecciona una foto",
        parse_mode=ParseMode.MARKDOWN,
    )

    return PHOTO


def photo(update: Update, context: CallbackContext) -> str:
    photo_path = get_unique_filename()
    photo_file = update.message.photo[-1].get_file()
    photo_file.download(photo_path)

    user_data = context.user_data
    user_data['profile_data']['photo'] = photo_path
    user_data['level_state'] = LOCATION
    name = user_data['profile_data']['first_name'].split()[0]


    update.message.reply_text(
        f"¿Cual es tu ubicación {name}?\n\n"
        "👇 Presiona el botón en forma de clip📎, selecciona ubicacion 📍y envia donde te encuentras",
        parse_mode=ParseMode.MARKDOWN
    )

    return LOCATION


def photo_attach(update: Update, context: CallbackContext) -> str:
    photo_path = get_unique_filename()
    file = context.bot.getFile(update.message.document.file_id)
    file.download(photo_path)

    user_data = context.user_data
    user_data['profile_data']['photo'] = photo_path
    user_data['level_state'] = LOCATION
    name = user_data['profile_data']['first_name'].split()[0]

    update.message.reply_text(
        f"¿Cual es tu ubicación {name}?\n\n"
        "👇 Presiona el botón en forma de clip📎, selecciona ubicacion 📍y envia donde te encuentras",
        parse_mode=ParseMode.MARKDOWN
    )

    return LOCATION


def skip_photo(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data['level_state'] = LOCATION
    name = user_data['profile_data']['first_name'].split()[0]


    update.message.reply_text(
        "No hay problema, puedes configurar tu foto de perfil en otro momento"
    )
    update.message.reply_text(
        f"¿Cual es tu ubicación {name}?\n\n"
        "👇 Presiona el botón en forma de clip📎, selecciona ubicacion 📍y envia donde te encuentras",
        parse_mode=ParseMode.MARKDOWN
    )

    return LOCATION


def location(update: Update, context: CallbackContext) -> str:
    location = update.message.location
    location = [location.latitude, location.longitude]

    user_data = context.user_data
    user_data['profile_data']['location'] = {
        'type': "Point",
        'coordinates': location,
    }
    user_data['level_state'] = ACCEPT_CONDITIONS
    name = user_data['profile_data']['first_name'].split()[0]

    markup = ReplyKeyboardMarkup(
        keyboard=reply_keyboard_accept_conditions,
        resize_keyboard=True
    )

    update.message.reply_text(
        f"¡Genial {name}!, ya casi estamos listos\n"
    )
    update.message.reply_text(
        terms_and_conditions,
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return ACCEPT_CONDITIONS


def skip_location(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data['level_state'] = ACCEPT_CONDITIONS
    name = user_data['profile_data']['first_name'].split()[0]

    markup = ReplyKeyboardMarkup(
        keyboard=reply_keyboard_accept_conditions,
        resize_keyboard=True
    )

    update.message.reply_text(
        f"No tan genial {name}, pareces algo paranoico {name}, pero continuamos\n"
    )

    update.message.reply_text(
        terms_and_conditions,
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return ACCEPT_CONDITIONS


def accept_conditions(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data['level'] = WELCOME
    del user_data['level_state']

    me_info, token = do_register_request(user_data['profile_data'])
    
    if me_info and token:
        user_data['token'] = token
        user_data['profile_data'] = me_info
        name = user_data['profile_data']['first_name'].split()[0]

        update.message.reply_text(
            f"¡Bienvenido {name}!",
            reply_markup=ReplyKeyboardRemove()
        )

        start_app(update, context)

        return WELCOME
    else:
        update.message.reply_text(
            'Ha ocurrido un error\n\n'
            "El email que ingresaste ya lo ocupa otra persona\n"
        )
        return navigate_to_self(update, context)