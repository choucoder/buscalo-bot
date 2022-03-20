from emoji import emojize
from telegram import KeyboardButton


reply_keyboard = [
    [
        KeyboardButton(text=emojize('Nombre', use_aliases=True)),
        KeyboardButton(text=emojize('Apellido', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize('Fecha nacimiento', use_aliases=True)),
        KeyboardButton(text=emojize('Genero', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize('Foto', use_aliases=True)),
        KeyboardButton(text=emojize('Ubicacion', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ]
]

reply_keyboard_gender = [
    [
        KeyboardButton(text=emojize(':man: Masculino')),
        KeyboardButton(text=emojize(':woman: Femenino')),
        KeyboardButton(text=emojize(':question: Prefiero no decir', use_aliases=True))
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ]
]

reply_keyboard_back = [
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ]
]

