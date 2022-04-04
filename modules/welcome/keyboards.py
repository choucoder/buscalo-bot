from emoji import emojize
from telegram import KeyboardButton


welcome_reply_keyboard = [
    [
        KeyboardButton(text=emojize(':earth_americas: Interactuar', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':mag_right: Buscar productos', use_aliases=True)),
        KeyboardButton(text=emojize(':round_pushpin: Tiendas', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':department_store: Mi tienda', use_aliases=True)),
        KeyboardButton(text=emojize(':postbox: Mis estados', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':gear: Configuracion', use_aliases=True)),
    ]
]