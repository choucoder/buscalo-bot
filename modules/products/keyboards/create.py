from emoji import emojize
from telegram import KeyboardButton


reply_keyboard = [
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ],
]

reply_keyboard_skip = [
    [
       KeyboardButton(text=emojize('/omitir', use_aliases=True)),
    ],
    [
       KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ],
]