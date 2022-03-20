from telegram import Update
from telegram.ext import CallbackContext

from modules.posts import keyboards, callbacks
from ..states import *
from ..requests.delete import do_delete


def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    token = user_data['token']

    if "current_post" in user_data:
        post_id = user_data['current_post']['id']
        _ = do_delete(token, post_id)
        
        update.message.reply_text(
            'El estado ha sido eliminado',
        )
        
        return callbacks.list.navigate_to_self(update, context)