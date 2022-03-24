from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext
from modules.base.requests import get_token_or_refresh

from modules.products import keyboards, callbacks
from ..states import *
from ..requests.delete import do_delete
from ..render import render_product


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    token = get_token_or_refresh(user_data)

    if "current_product" in user_data:
        product_id = user_data['current_product']['id']
        product = do_delete(token, product_id)
        
        update.message.reply_text(
            'Producto ha sido eliminado',
        )
        
        return callbacks.list.navigate_to_self(update, context)