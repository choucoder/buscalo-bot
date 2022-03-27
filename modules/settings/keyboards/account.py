from emoji import emojize
from telegram import KeyboardButton


reply_keyboard = [
    [
        KeyboardButton(text=emojize(':wastebasket: Eliminar cuenta', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ],
]

reply_keyboard_delete = [
    [
        KeyboardButton(text=emojize('Continuar', use_aliases=True)),
        KeyboardButton(text=emojize('Cancelar', use_aliases=True)),
    ], 
]