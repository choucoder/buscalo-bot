from emoji import emojize
from telegram import KeyboardButton


reply_keyboard = [
    [
        KeyboardButton(text=emojize('Nombre', use_aliases=True)),
        KeyboardButton(text=emojize('Descripcion', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':frame_with_picture: Logo', use_aliases=True)),
        KeyboardButton(text=emojize(':round_pushpin: Ubicacion', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize('WhatsApp de tienda', use_aliases=True)),
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

reply_keyboard_currency = [
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ]
]