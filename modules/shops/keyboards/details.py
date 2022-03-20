from emoji import emojize
from telegram import KeyboardButton


reply_keyboard = [
    [
        KeyboardButton(text=emojize('Ver productos', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ]
]