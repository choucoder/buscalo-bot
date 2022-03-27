from emoji import emojize
from telegram import KeyboardButton


reply_keyboard = [
    [
        KeyboardButton(text=emojize(':pencil: Perfil', use_aliases=True)),
        KeyboardButton(text=emojize(':bust_in_silhouette: Cuenta', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ],
]