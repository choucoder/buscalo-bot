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
            InlineKeyboardButton(
                text=emojize(':warning: Reportar', use_aliases=True),
                callback_data=f"REPORT_POST-{post['id']}"
            )
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
                    text=emojize(':speech_balloon: Chat de tienda', use_aliases=True),
                    url=url,
                )
            ]
        )

    markup = InlineKeyboardMarkup(inline_reply_keyboard)

    return markup


def get_feed_report_inline_keyboard_markup(feed: Dict) -> InlineKeyboardMarkup:
    post = feed['post']
    user = feed['user']
    shop = post['shop']

    problems_options = [
        (1, 'Desnudos'),
        (2, 'Violencia'),
        (3, 'Suicidio'),
        (4, 'Informacion Falsa'),
        (5, 'Spam'),
        (6, 'Lenguaje que incita al odio'),
        (7, 'Terrorismo'),
        (8, 'Otro'),
    ]

    inline_keyboard_buttons = []

    for option in problems_options:
        _id, _ = option
        inline_keyboard_buttons.append(
            InlineKeyboardButton(
                text=emojize(f"{_id}", use_aliases=True),
                callback_data=f"FEED_REPORT_OPTION-{post['id']}-{_id}"
            )
        )

    inline_reply_keyboard = []
    for i, kb in enumerate(inline_keyboard_buttons):
        if i % 4 == 0:
            inline_reply_keyboard.append([])
            inline_reply_keyboard[-1].append(inline_keyboard_buttons[i])
        else:
            inline_reply_keyboard[-1].append(inline_keyboard_buttons[i])
    
    inline_reply_keyboard.append(
        [
            InlineKeyboardButton(
                text=emojize(':arrow_left: Atras', use_aliases=True),
                callback_data=f"REPORT_POST_BACK-{post['id']}"
            ) 
        ]
    )

    return InlineKeyboardMarkup(inline_reply_keyboard)