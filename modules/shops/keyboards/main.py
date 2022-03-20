from emoji import emojize
from telegram import KeyboardButton


reply_keyboard = [
    [
        KeyboardButton(text=emojize(':heavy_plus_sign: Producto', use_aliases=True)),
        KeyboardButton(text=emojize('Ver Productos', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':clipboard: Ordenes de tienda', use_aliases=True)),
        KeyboardButton(text=emojize(':gear: Configuracion', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ]
]