from emoji import emojize
from telegram import KeyboardButton


reply_keyboard_gender = [
    [
        KeyboardButton(text=emojize(':man: Masculino')),
        KeyboardButton(text=emojize(':woman: Femenino')),
        KeyboardButton(text=emojize(':question: Prefiero no decir', use_aliases=True))
    ]
]

reply_keyboard_skip = [
    [
        KeyboardButton(text='/Omitir'),
    ]
]

reply_keyboard_accept_conditions = [
    [
        KeyboardButton(text='Aceptar')
    ]
]