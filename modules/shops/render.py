from typing import Dict

from emoji import emojize
import flag
from telegram import (
    Update, ParseMode
)
from telegram.utils.helpers import escape_markdown
import requests
from decouple import config


API_URL = config('API_URL')

def show_shop(update: Update, shop: Dict, markup=None, hidden_ws=False) -> None:
    text = f"*{shop['name']}*\n\n"
    text += f":information_source: {shop['description']}\n"

    if "address" in shop and shop['address']:
        address = shop['address']
        city = address.get('city', None)
        state = address.get('state', None)
        country = address.get('country', None)

        text += f":globe_with_meridians: {city}, {state}, {country}\n"
    else:
        text += f":globe_with_meridians: Desconocida\n"

    if shop['currency']:
        text += f"🪙 Moneda: {shop['currency']['code']} " + flag.flag(f":{shop['currency']['country_code']}:") + "\n"
    
    if shop['phone_number'] and not hidden_ws:
        text += f"📞 WhatsApp: {shop['phone_number']}\n"

    text += f"\nID: `{shop['id']}`"

    is_photo = False

    if shop['logo']:    
        response = requests.get(f"{API_URL}{shop['logo']}")
        is_photo = True

    if markup:
        if is_photo:
            try:
                update.message.reply_photo(
                    caption=emojize(text, use_aliases=True),
                    photo=response.content,
                    reply_markup=markup,
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                update.message.reply_photo(
                    caption=escape_markdown(emojize(text, use_aliases=True)),
                    photo=response.content,
                    reply_markup=markup,
                    parse_mode=ParseMode.MARKDOWN
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
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                update.message.reply_text(
                    escape_markdown(emojize(text, use_aliases=True)),
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


def render_shop(update: Update, shop: Dict, markup=None, hidden_ws=False) -> None:
    text = f"*{shop['name']}*\n\n"
    text += f":information_source: {shop['description']}\n"

    if "address" in shop and shop['address']:
        address = shop['address']
        city = address.get('city', None)
        state = address.get('state', None)
        country = address.get('country', None)

        text += f":globe_with_meridians: {city}, {state}, {country}\n"
    else:
        text += f":globe_with_meridians: Desconocida\n"

    if shop['currency']:
        text += f"🪙 Moneda: {shop['currency']['code']} " + flag.flag(f":{shop['currency']['country_code']}:") + "\n"
    
    text += f"\nID: `{shop['id']}`"

    is_photo = False

    if shop['logo']:    
        response = requests.get(f"{API_URL}{shop['logo']}")
        is_photo = True

    if markup:
        if is_photo:
            try:
                update.message.reply_photo(
                    caption=emojize(text, use_aliases=True),
                    photo=response.content,
                    reply_markup=markup,
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                update.message.reply_photo(
                    caption=escape_markdown(emojize(text, use_aliases=True)),
                    photo=response.content,
                    reply_markup=markup,
                    parse_mode=ParseMode.MARKDOWN
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
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                update.message.reply_photo(
                    caption=escape_markdown(emojize(text, use_aliases=True)),
                    photo=response.content,
                    parse_mode=ParseMode.MARKDOWN
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


def render_shop_search(update: Update, shop: Dict, markup=None, hidden_ws=False, current_page=None, pages=None) -> None:
    text = f"*{shop['name']}*\n\n"
    text += f":information_source: {shop['description']}\n"

    if "address" in shop and shop['address']:
        address = shop['address']
        city = address.get('city', None)
        state = address.get('state', None)
        country = address.get('country', None)

        text += f":globe_with_meridians: {city}, {state}, {country}\n"
    else:
        text += f":globe_with_meridians: Desconocida\n"

    if shop['currency']:
        text += f"🪙 Moneda: {shop['currency']['code']} " + flag.flag(f":{shop['currency']['country_code']}:") + "\n"
    
    if shop['phone_number'] and not hidden_ws:
        text += f"📞 WhatsApp: {shop['phone_number']}\n"

    text += f"\n`@{shop['id']}`\n"

    if current_page and pages:
        text += f"\n{current_page}/{pages}"

    is_photo = False

    if shop['logo']:    
        response = requests.get(f"{API_URL}{shop['logo']}")
        is_photo = True

    if markup:
        if is_photo:
            try:
                update.message.reply_photo(
                    caption=emojize(text, use_aliases=True),
                    photo=response.content,
                    reply_markup=markup,
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                update.message.reply_photo(
                    caption=escape_markdown(emojize(text, use_aliases=True)),
                    photo=response.content,
                    reply_markup=markup,
                    parse_mode=ParseMode.MARKDOWN
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
                    parse_mode=ParseMode.MARKDOWN
                )
            except:
                update.message.reply_text(
                    escape_markdown(emojize(text, use_aliases=True)),
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