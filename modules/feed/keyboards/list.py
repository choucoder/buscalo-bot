from typing import Dict

from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton


reply_keyboard = [
    [
        KeyboardButton(text=emojize(':arrow_double_down: Deslizar', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':heavy_plus_sign: Nuevo estado', use_aliases=True)),
        KeyboardButton(text=emojize(':department_store: Ver tienda', use_aliases=True))
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True))
    ]
]

def get_feed_inline_keyboard_markup(feed: Dict) -> InlineKeyboardMarkup:
    post = feed['post']
    user = feed['user']
    shop = post['shop']

    inline_reply_keyboard = [
        [
            InlineKeyboardButton(
                text=emojize(':heart:/:broken_heart:', use_aliases=True),
                callback_data=f"LIKE_POST-{post['id']}"
            ),
        ],
    ]
    if shop:
        if user['telegram_username'] and not user['telegram_username'].startswith('none-'):
            url = f"t.me/{user['telegram_username']}"
        else:
            url = f"tg://user?id={user['telegram_user_id']}"
        
        inline_reply_keyboard.append(
            [
                InlineKeyboardButton(
                    text=emojize('Chat de tienda :speech_balloon:', use_aliases=True),
                    url=url,
                )
            ]
        )

    markup = InlineKeyboardMarkup(inline_reply_keyboard)

    return markup