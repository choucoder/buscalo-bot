from typing import Dict

from emoji import emojize
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton


reply_keyboard = [
    [
        KeyboardButton(text=emojize('Ver productos', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ]
]

reply_keyboard_view_products = [
    [
        KeyboardButton(text=emojize(':arrow_left: Anterior', use_aliases=True)),
        KeyboardButton(text=emojize('Siguiente :arrow_right:', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ],
]

reply_keyboard_view_products_empty = [
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ],
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

    if shop['phone_number']:
        reply_keyboard_inline.append(
            [
                InlineKeyboardButton(
                    text=emojize('Chat de WhatsApp :telephone_receiver:', use_aliases=True),
                    url=f"wa.me/{shop['phone_number']}?text=Buenas!"
                )
            ]
        )

    return InlineKeyboardMarkup(reply_keyboard_inline)