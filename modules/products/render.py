from ast import alias
from typing import Dict
from pprint import pprint

from emoji import emojize
from geopy.distance import geodesic
from telegram import (
    InlineKeyboardMarkup, Update, ParseMode, InputMediaPhoto
)

import requests
from decouple import config

from .keyboards.search import get_product_search_inline_markup


API_URL = config('API_URL')

def render_product(update: Update, product: Dict, markup=None, current_page=None, pages=None) -> None:
    text = f"*{product['name']}*:pushpin:\n\n"
    text += f"{product['details']}\n"
    if product['shop']['currency']:
        currency = product['shop']['currency']['code']
    else:
        currency = ''
    text += f"Precio:  {product['price']} {currency}\n"

    if current_page and pages:
        text += f"\n{current_page}/{pages}"

    is_photo = False

    if product['photo']:
        response = requests.get(f"{API_URL}{product['photo']}")
        is_photo = True

    if markup:
        if is_photo:
            update.message.reply_photo(
                caption=emojize(text, use_aliases=True),
                photo=response.content,
                reply_markup=markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            update.message.reply_text(
                emojize(text, use_aliases=True),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=markup
            )
    else:
        if is_photo:
            update.message.reply_photo(
                caption=emojize(text, use_aliases=True),
                photo=response.content,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            update.message.reply_text(
                emojize(text, use_aliases=True),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=markup
            )

def render_search_product(update: Update, product: Dict, user_data) -> None:
    text = f"*{product['name']}* :pushpin:\n\n"
    text += f"{product['details']}\n"
    if product['shop']['currency']:
        currency = product['shop']['currency']['code']
    else:
        currency = ''

    text += f"💲 Precio: {product['price']} {currency}\n"
    text += f":department_store: {product['shop']['name']} `{product['shop']['id']}`\n"
     
    if "address" in product['shop'] and product['shop']['address']:
        address = product['shop']['address']
        city = address.get('city', None)
        state = address.get('state', None)
        country = address.get('country', None)

        text += f":globe_with_meridians: Ubicación: {city}, {state}, {country}\n"
    else:
        text += f":globe_with_meridians: Ubicación: Desconocida :grey_exclamation:"

    shop_location = product['shop']['location']
    user_location = user_data['user']['location']
    
    if shop_location and user_location:
        shop_location = shop_location['coordinates']
        user_location = user_location['coordinates']

        distance = geodesic(shop_location, user_location)
        distance_km = round(distance.km, 2)

        text += f":round_pushpin: A {distance_km} km de distancia\n\n"
    else:
        text += "\n"

    text += f":heart: {product['votes_amount']}\n"

    is_photo = False

    if product['photo']:
        response = requests.get(f"{API_URL}{product['photo']}")
        is_photo = True

    if is_photo:    
        update.message.reply_photo(
            caption=emojize(text, use_aliases=True),
            photo=response.content,
            reply_markup=get_product_search_inline_markup(product),
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        update.message.reply_text(
            emojize(text, use_aliases=True),
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=get_product_search_inline_markup(product),
        )


def render_search_product_inline(update: Update, product: Dict, markup: InlineKeyboardMarkup, user_data):    
    text = f"*{product['name']}* :pushpin:\n\n"
    text += f"{product['details']}\n"
    if product['shop']['currency']:
        currency = product['shop']['currency']['code']
    else:
        currency = ''

    text += f"💲 Precio: {product['price']} {currency}\n"
    text += f":department_store: {product['shop']['name']} `{product['shop']['id']}`\n"
    
    if "address" in product['shop'] and product['shop']['address']:
        address = product['shop']['address']
        city = address.get('city', None)
        state = address.get('state', None)
        country = address.get('country', None)

        text += f":globe_with_meridians: Ubicación: {city}, {state}, {country}\n\n"
    else:
        text += f":globe_with_meridians: Ubicación: Desconocida :grey_exclamation:"

    shop_location = product['shop']['location']
    user_location = user_data['user']['location']
    
    if shop_location and user_location:
        shop_location = shop_location['coordinates']
        user_location = user_location['coordinates']

        distance = geodesic(shop_location, user_location)
        distance_km = round(distance.km, 2)

        text += f":round_pushpin: A {distance_km} km de distancia\n\n"
    else:
        text += "\n"

    text += f":heart: {product['votes_amount']}\n"
    
    is_photo = False

    if product['photo']:
        response = requests.get(f"{API_URL}{product['photo']}")
        is_photo = True
    
    if is_photo:
        update.callback_query.edit_message_media(
            InputMediaPhoto(response.content, caption=emojize(text, use_aliases=True), parse_mode=ParseMode.MARKDOWN)
        )
    else:
        update.callback_query.edit_message_text(
           emojize(text, use_aliases=True),
           parse_mode=ParseMode.MARKDOWN
        )
    
    # markup = get_product_search_inline_markup(product)
    update.callback_query.edit_message_reply_markup(markup)


def render_search_product_map(update: Update, product: Dict, markup: InlineKeyboardMarkup, user_data):
    shop_location = product['shop']['location']

    if shop_location:
        lat, lon = shop_location
        update.callback_query.edit_message_live_location(latitude=lat, longitude=lon)