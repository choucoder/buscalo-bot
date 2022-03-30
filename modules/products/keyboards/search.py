from typing import Dict

from emoji import emojize
from telegram import KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


reply_keyboard = [
    [
        KeyboardButton(text=emojize(':arrow_left: Anterior', use_aliases=True)),
        KeyboardButton(text=emojize('Siguiente :arrow_right: ', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':world_map: Ver ubicacion de tienda', use_aliases=True)),
        KeyboardButton(text=emojize(':gear: Configuracion de busqueda', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ]
]


reply_keyboard_non_response = [
    [
        KeyboardButton(text=emojize(':gear: Configuracion de busqueda', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ],
]


reply_keyboard_search_settings = [
    [
        KeyboardButton(text=emojize(':satellite: Radio de busqueda', use_aliases=True)),
        KeyboardButton(text=emojize(':round_pushpin: Ubicacion', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ],
]


reply_keyboard_search_range_settings = [
    [
        KeyboardButton(text=emojize('5 Km', use_aliases=True)),
        KeyboardButton(text=emojize('10 Km', use_aliases=True)),
        KeyboardButton(text=emojize('20 Km', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize('30 Km', use_aliases=True)),
        KeyboardButton(text=emojize('40 Km', use_aliases=True)),
        KeyboardButton(text=emojize('50 Km', use_aliases=True)),
    ],
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ],
]


reply_keyboard_search_location_settings = [
    [
        KeyboardButton(text=emojize(':arrow_left: Atras', use_aliases=True)),
    ],
]


def get_product_search_inline_markup(product: Dict, user, is_added=False) -> InlineKeyboardMarkup:
    shop_id = product['shop']['id']
    user_id = product['shop']['user']['telegram_user_id']
    username = product['shop']['user']['telegram_username']
    product_id = product['id']

    if username and not username.startswith("none-"):
        url = f"t.me/{username}?start=holacomoesas"
    else:
        url = f"tg://user?id={user_id}"

    reply_keyboard_product_search = [
        [
            InlineKeyboardButton(
                text=emojize('Ver productos de la tienda'),
                callback_data=f"VIEW_STORE_PRODUCTS-{product_id}-{shop_id}"
            ),
        ],
        [
            InlineKeyboardButton(
                text=emojize(':heart:/:broken_heart:', use_aliases=True),
                callback_data=f"LIKE_PRODUCT-{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text=emojize(':speech_balloon: Chat de tienda', use_aliases=True),
                url=url,
            ),
        ],
    ]

    if user['id'] != product['shop']['user']['id']:
        reply_keyboard_product_search[-2].append(
            InlineKeyboardButton(
                text=emojize(':warning: Reportar', use_aliases=True),
                callback_data=f"REPORT_PRODUCT-{product_id}"
            )
        )

    if product['shop']['phone_number']:
        text = f"{product['name']}\n"
        text += f"{product['details']}\n"
        if product['shop']['currency']:
            currency = product['shop']['currency']['code']
        else:
            currency = ''

        text += f"Precio: {product['price']} {currency}\n\n"
        text += f"Tienda: {product['shop']['name']}\n"
        
        if "address" in product['shop']:
            address = product['shop']['address']
            city = address.get('city', None)
            state = address.get('state', None)
            country = address.get('country', None)

            text += f"Ubicacion: {city}, {state}, {country}\n"
        else:
            text += f"Ubicacion: Desconocida"

        reply_keyboard_product_search[-1].append(
            InlineKeyboardButton(
                text=emojize(':speech_balloon: WhatsApp', use_aliases=True),
                url=f"wa.me/{product['shop']['phone_number']}?text={text}"
            )
        )

    markup = InlineKeyboardMarkup(reply_keyboard_product_search)

    return markup


def get_view_store_products_inline_keyboard_markup(product_id, shop_id, page=1):

    reply_keyboard = [
        [
            InlineKeyboardButton(
                text=emojize(':arrow_left:', use_aliases=True),
                callback_data=f"VIEW_STORE_PRODUCTS_PREV-{product_id}-{shop_id}-{page}"
            ),
            InlineKeyboardButton(
                text=emojize(':arrow_right:', use_aliases=True),
                callback_data=f"VIEW_STORE_PRODUCTS_NEXT-{product_id}-{shop_id}-{page}"
            ),
        ],
        [
            InlineKeyboardButton(
                text=emojize(':arrow_left: Atras', use_aliases=True),
                callback_data=f"VIEW_STORE_PRODUCTS_BACK-{product_id}-{shop_id}-{page}"
            ),
        ]
    ]

    markup = InlineKeyboardMarkup(reply_keyboard)

    return markup


def get_product_report_inline_keyboard_markup(product: Dict) -> InlineKeyboardMarkup:
    problems_options = [
        (1, 'Desnudos'),
        (2, 'Violencia'),
        (3, 'Suicidio'),
        (4, 'Informacion Falsa'),
        (5, 'Spam'),
        (6, 'Lenguaje que incita al odio'),
        (7, 'Terrorismo'),
        (8, 'Otro'),
    ]

    inline_keyboard_buttons = []

    for option in problems_options:
        _id, _ = option
        inline_keyboard_buttons.append(
            InlineKeyboardButton(
                text=emojize(f"{_id}", use_aliases=True),
                callback_data=f"PRODUCT_REPORT_OPTION-{product['id']}-{_id}"
            )
        )

    inline_reply_keyboard = []
    for i, kb in enumerate(inline_keyboard_buttons):
        if i % 4 == 0:
            inline_reply_keyboard.append([])
            inline_reply_keyboard[-1].append(inline_keyboard_buttons[i])
        else:
            inline_reply_keyboard[-1].append(inline_keyboard_buttons[i])
    
    inline_reply_keyboard.append(
        [
            InlineKeyboardButton(
                text=emojize(':arrow_left: Atras', use_aliases=True),
                callback_data=f"REPORT_PRODUCT_BACK-{product['id']}"
            ) 
        ]
    )

    return InlineKeyboardMarkup(inline_reply_keyboard)