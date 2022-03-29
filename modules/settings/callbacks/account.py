from emoji import emojize
from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext

from modules import settings
from modules.base.requests import get_token_or_refresh
from modules.base.states import USER_REGISTRATION, WELCOME
from modules.users.requests.delete import do_user_delete
from modules.welcome.callbacks import start
from ..states import *


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    markup = ReplyKeyboardMarkup(
        settings.keyboards.account.reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        "Selecciona una opción 👇",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SETTINGS_ACCOUNT


def back(update: Update, context: CallbackContext) -> str:
    settings.callbacks.main.navigate_to_self(update, context)
    return SETTINGS_ACCOUNT_BACK


def navigate_to_self_delete(update: Update, context: CallbackContext) -> str:
    markup = ReplyKeyboardMarkup(
        settings.keyboards.account.reply_keyboard_delete,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    text = ":warning: Esta seguro que desea eliminar su cuenta? :warning:\n\n"
    text += "Su cuenta sera eliminada junto con su tienda, productos y estados compartidos"
    text = emojize(text, use_aliases=True)

    update.message.reply_text(
        text,
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SETTINGS_ACCOUNT_DELETE


def delete_cancel(update: Update, context: CallbackContext) -> str:
    navigate_to_self(update, context)
    return SETTINGS_ACCOUNT_DELETE_CANCEL


def delete_confirm(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    text = "Su cuenta ha sido eliminada. Para volver a registrarse tendra que ejecutar el comando /start en el bot"
    token = get_token_or_refresh(user_data)
    response = do_user_delete(token)

    if response.status_code == 204:
        user_data.clear()
        _ = context.user_data.pop('token', None)
        _ = context.user_data.pop('profile_data', None)
        _ = context.user_data.pop('shop', None)

        update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardRemove()
        )
        return start(update, context)
    else:
        update.message.reply_text(
            "Hubo un error al intentar eliminar su cuenta. Intentelo de nuevo",
            parse_mode=ParseMode.MARKDOWN
        )
        navigate_to_self(update, context)
        return SETTINGS_ACCOUNT_DELETE_CANCEL