from emoji import emojize
from telegram import KeyboardButton


reply_keyboard = [
    [
        KeyboardButton(text=emojize('Nombre', use_aliases=True)),
        KeyboardButton(text=emojize('Detalles', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize('Precio', use_aliases=True)),
        KeyboardButton(text=emojize('Foto', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ],
]
