from typing import Dict

from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton


reply_keyboard = [
    [
        KeyboardButton(text=emojize('Ver Productos', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ]
]

def get_shop_contact_inline_markup(shop: Dict) -> InlineKeyboardMarkup:
    user = shop['user']
    username = user['telegram_username']

    username = "none-" + username

    if username and not username.startswith('none-'):
        url = f"t.me/{username}"
    else:
        user_id = user['telegram_user_id']
        url = f"tg://user?id={user_id}"
    
    reply_keyboard_inline = [
        [
            InlineKeyboardButton(
                text=emojize('Chat de tienda :speech_balloon:', use_aliases=True),
                url=url
            )
        ]
    ]

    return InlineKeyboardMarkup(reply_keyboard_inline)