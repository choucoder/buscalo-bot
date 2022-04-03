import datetime
from typing import Dict
from venv import create

from emoji import emojize
from geopy.distance import geodesic
from telegram import (
    InlineKeyboardMarkup, Update, ParseMode
)
from telegram.utils.helpers import escape_markdown
import requests
from decouple import config

from utils.helpers import calc_age


API_URL = config('API_URL')


def render_user(update: Update, user: Dict, markup=None):
    text = f"{user['first_name']} {user['last_name']}\n"

    birthdate = datetime.datetime.strptime(user['birthdate'], "%d-%m-%Y")
    age = calc_age(birthdate)
    
    text += f"{age} Años\n"
    addr = user.get('address', '')

    if isinstance(addr, Dict):
        city = addr.get('city', '')
        state = addr.get('state', '')
        country = addr.get('country', '')
        addr = f"{city}, {state} - {country}"
    else:
        addr = 'Desconocida'
        
    text += f":earth_americas: {addr}\n"
    
    gender = "" 
    if user['gender'] == "Male":
        gender = ":man: Hombre"
    elif user['gender'] == "Female":
        gender = ":woman: Mujer"
    else:
        gender = ":exclamation:"

    text += f"Género: {gender}\n\n"

    is_verified = ":white_check_mark:" if user['is_verified'] else ":x:"
    text += f"Esta verificado: {is_verified}"

    is_photo = False

    if user['photo']:
        response = requests.get(f"{API_URL}{user['photo']}")
        is_photo = True

    if markup:
        if is_photo:
            try:
                update.message.reply_photo(
                    caption=emojize(text, use_aliases=True),
                    photo=response.content,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=markup    
                )
            except:
                update.message.reply_photo(
                    caption=escape_markdown(emojize(text, use_aliases=True)),
                    photo=response.content,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=markup    
                )
        else:
            try:
                update.message.reply_text(
                    emojize(text, use_aliases=True),
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=markup
                )
            except:
                update.message.reply_text(
                    escape_markdown(emojize(text, use_aliases=True)),
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=markup
                )
    else:
        if is_photo:
            try:
                update.message.reply_photo(
                    caption=emojize(text, use_aliases=True),
                    photo=response.content,
                    parse_mode=ParseMode.MARKDOWN,
                )
            except:
                update.message.reply_photo(
                    caption=escape_markdown(emojize(text, use_aliases=True)),
                    photo=response.content,
                    parse_mode=ParseMode.MARKDOWN,
                )      
        else:
            try:
                update.message.reply_text(
                    emojize(text, use_aliases=True),
                    reply_markup=markup,
                    parse_mode=ParseMode.MARKDOWN,
                )
            except:
                update.message.reply_text(
                    escape_markdown(emojize(text, use_aliases=True)),
                    reply_markup=markup,
                    parse_mode=ParseMode.MARKDOWN,
                )