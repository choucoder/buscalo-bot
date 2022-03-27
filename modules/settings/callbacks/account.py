from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext

from modules import settings
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

    update.message.reply_text(
        "Desea eliminar su cuenta? 👇\n\n"
        "Se eliminara toda su cuenta incluida su tienda, productos, estados",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SETTINGS_ACCOUNT_DELETE


def delete_cancel(update: Update, context: CallbackContext) -> str:
    navigate_to_self(update, context)
    return SETTINGS_ACCOUNT_DELETE_CANCEL


def delete_confirm(update: Update, context: CallbackContext) -> str:
    pass
