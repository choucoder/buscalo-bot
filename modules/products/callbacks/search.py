from ast import Call
from emoji import emojize
from telegram import (
    ParseMode, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
)
from telegram.ext import CallbackContext

from modules.base.requests import get_token_or_refresh
from modules.base.render import render_send_location_help
from modules.products import keyboards
from modules import shops
from modules import welcome
from modules.products.keyboards.search import get_view_store_products_inline_keyboard_markup
from ..states import *
from ..requests.list import get_products
from ..requests.search import (
    get_product, product_search, do_update_search_settings,
    rating_product,
)
from ..render import (
    render_search_product, render_search_product_inline,
    render_search_product_map,
    render_report_options_product_inline,
    render_product_back,
)
from ..keyboards.search import get_product_search_inline_markup


report_options = [
    (1, 'Desnudos'),
    (2, 'Violencia'),
    (3, 'Suicidio'),
    (4, 'Informacion Falsa'),
    (5, 'Spam'),
    (6, 'Lenguaje que incita al odio'),
    (7, 'Terrorismo'),
    (8, 'Otro'),
]

def navigate_to_self(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    count_products = user_data.get('count_products', 0)
    
    if count_products > 0 and 'search_product' in user_data:
        markup = ReplyKeyboardMarkup(
            keyboards.search.reply_keyboard,
            resize_keyboard=True,
            one_time_keyboard=False,
            input_field_placeholder='Ingrese el nombre'
        )

        update.message.reply_text(
            "...",
            reply_markup=markup
        )

        render_search_product(update, user_data['search_product'], user_data)

    else:
        markup = ReplyKeyboardMarkup(
            keyboards.search.reply_keyboard_non_response,
            resize_keyboard=True,
            one_time_keyboard=False,
        )
        update.message.reply_text(
            "Aqui puedes realizar 🔎 busquedas y ⚙️ configurar parametros de busqueda (ubicación, amplitud de busqueda)\n\n"
            "Escribe el nombre del producto o servicio que buscas 👇\n"
            "Escribe @<id-de-tienda>, para ver el perfil de la tienda 👇",
            reply_markup=markup,
            parse_mode=ParseMode.MARKDOWN
        )

    return PRODUCT_SEARCH


def navigate_to_search_settings(update: Update, context: CallbackContext) -> str:
    markup = ReplyKeyboardMarkup(
        keyboards.search.reply_keyboard_search_settings,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        "Selecciona el parametro de busqueda a editar 👇",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SEARCH_SETTINGS


def navigate_to_search_range_settings(update: Update, context: CallbackContext) -> str:
    markup = ReplyKeyboardMarkup(
        keyboards.search.reply_keyboard_search_range_settings,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        "Selecciona la amplitud de la busqueda 👇",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SEARCH_RANGE_SETTINGS


def navigate_to_search_location_settings(update: Update, context: CallbackContext) -> str:
    markup = ReplyKeyboardMarkup(
        keyboards.search.reply_keyboard_search_location_settings,
        resize_keyboard=True,
        one_time_keyboard=False,
    )

    update.message.reply_text(
        "¿Donde quieres buscar?!\n\n"
        "👇 Presiona el botón en forma de clip📎, selecciona ubicación 📍y envia la ubicación",
        reply_markup=markup,
        parse_mode=ParseMode.MARKDOWN
    )

    return SEARCH_LOCATION_SETTINGS


def back(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    user_data.pop('search_product', None)
    user_data.pop('current_page', None)
    user_data.pop('count_products', None)

    welcome.callbacks.start_app(update, context)
    return PRODUCT_SEARCH_BACK


def back_search_settings(update: Update, context: CallbackContext) -> str:
    navigate_to_self(update, context)
    return SEARCH_SETTINGS_BACK


def back_search_location_settings(update: Update, context: CallbackContext) -> str:
    navigate_to_search_settings(update, context)
    return SEARCH_LOCATION_SETTINGS_BACK


def back_search_range_settings(update: Update, context: CallbackContext) -> str:
    navigate_to_search_settings(update, context)
    return SEARCH_RANGE_SETTINGS_BACK


def handle_query(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    query = update.message.text

    if query.startswith('@') and len(query) >=8 and ' ' not in query:
        shop_id = query[1: ]
        return shops.callbacks.search.navigate_to_self(update, context, shop_id=shop_id)
    else:
        query = query.lower()
        token = get_token_or_refresh(user_data)
        products, count = product_search(token, query, page=1)
        
        if count > 0:
            user_data['search_product'] = products[0]
            user_data['current_page'] = 1
            user_data['count_products'] = count
            user_data['query'] = query

            markup = ReplyKeyboardMarkup(
                keyboards.search.reply_keyboard,
                resize_keyboard=True,
                one_time_keyboard=False
            )
            update.message.reply_text(
                "...",
                reply_markup=markup
            )
            render_search_product(update, products[0], user_data)
        else:
            user_data['count_products'] = count
            
            markup = ReplyKeyboardMarkup(
                keyboards.search.reply_keyboard_non_response,
                resize_keyboard=True,
                one_time_keyboard=False
            )

            update.message.reply_text(
                "No pudimos encontrar lo que buscas 😞\n"
                "Configura ⚙️ los parametros de búsqueda e intentalo de nuevo",
                reply_markup=markup,
                parse_mode=ParseMode.MARKDOWN
            )


def prev(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    
    if user_data['count_products'] == 0:
        update.message.reply_text(
            "Estas en la primera pagina y al parecer no has registrado productos"
        )
    elif user_data['current_page'] == 1:
        render_search_product(update, user_data['search_product'], user_data)

    else:
        token = get_token_or_refresh(user_data)
        query = user_data['query']
        current_page = user_data['current_page']
        
        products, _ = product_search(token, query, page=current_page - 1)

        user_data['search_product'] = products[0]
        user_data['current_page'] -= 1

        render_search_product(update, products[0], user_data)


def next(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data

    if user_data['count_products'] == 0:
        update.message.reply_text(
            "Estas en la primera pagina y al parecer no has registrado productos"
        )
    elif user_data['current_page'] == user_data['count_products']:
        render_search_product(update, user_data['search_product'], user_data)

    else:
        token = get_token_or_refresh(user_data)
        query = user_data['query']
        current_page = user_data['current_page']

        products, _ = product_search(token, query, page=current_page + 1)

        user_data['search_product'] = products[0]
        user_data['current_page'] += 1

        render_search_product(update, products[0], user_data)


def update_search_range_settings(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    search_range = update.message.text.split()[0]
    search_range = int(search_range) * 1000

    token = get_token_or_refresh(user_data)
    payload = {'distance': search_range}

    response = do_update_search_settings(token, payload)
    
    text = f'El radio de búsqueda :satellite: ha sido actualizado a {search_range / 1000} Km'
    text = emojize(text, use_aliases=True)

    update.message.reply_text(
        text
    )
    navigate_to_search_settings(update, context)

    return SEARCH_RANGE_SETTINGS_BACK


def update_search_location_settings(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    location = update.message.location
    location = [location.latitude, location.longitude]

    payload = {
        'location': {
            'type': 'Point',
            'coordinates': location,
        },
    }
    token = get_token_or_refresh(user_data)
    response = do_update_search_settings(token, payload)

    text = f'La ubicación de búsqueda :round_pushpin: ha sido actualizada'
    text = emojize(text, use_aliases=True)
    update.message.reply_text(
        text
    )

    navigate_to_search_settings(update, context)
    return SEARCH_LOCATION_SETTINGS_BACK


def add_to_car(update: Update, context: CallbackContext):
    query = update.callback_query
    _, product_id = query.data.split('-')

    print("Adding product to car: ", product_id)
    update.callback_query.answer()


def view_store_products(update: Update, context: CallbackContext):
    query = update.callback_query
    _, product_id, shop_id = query.data.split('-')
    
    markup = get_view_store_products_inline_keyboard_markup(
        product_id, shop_id, page=1
    )
    token = get_token_or_refresh(context.user_data)
    products, count = get_products(token, shop_id, page=1)
    update.callback_query.answer()

    render_search_product_inline(update, products[0], markup, context.user_data)


def view_store_products_next(update: Update, context: CallbackContext):
    query = update.callback_query
    _, product_id, shop_id, page = query.data.split('-')
    page = int(page)

    token = get_token_or_refresh(context.user_data)
    products, count = get_products(token, shop_id, page=page)
    update.callback_query.answer()

    if page < count:
        page = page + 1

        markup = get_view_store_products_inline_keyboard_markup(
            product_id, shop_id, page
        )

        render_search_product_inline(update, products[0], markup, context.user_data)


def view_store_products_prev(update: Update, context: CallbackContext):
    query = update.callback_query
    _, product_id, shop_id, page = query.data.split('-')
    page = int(page)

    if page > 1:
        page = page - 1
        update.callback_query.answer()

        markup = get_view_store_products_inline_keyboard_markup(
            product_id, shop_id, page
        )
        token = get_token_or_refresh(context.user_data)
        products, count = get_products(token, shop_id, page=page)
        render_search_product_inline(update, products[0], markup, context.user_data)
    else:
        update.callback_query.answer()


def view_store_products_back(update: Update, context: CallbackContext):
    query = update.callback_query
    _, product_id, shop_id, page = query.data.split('-')

    update.callback_query.answer()

    token = get_token_or_refresh(context.user_data)
    product = get_product(token, product_id)
    markup = get_product_search_inline_markup(product)

    render_search_product_inline(update, product, markup, context.user_data)


def like_product(update: Update, context: CallbackContext):
    user_data = context.user_data
    token = get_token_or_refresh(user_data)

    query = update.callback_query
    product_id = query.data.split('-')[-1]

    message = rating_product(token, product_id)

    # update.callback_query.bot.forward_message(
    #     user_data['user']['telegram_chat_id'],
    #     update.callback_query.id)
    query.answer(text=message)


def chat(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.message.chat_id,
        reply_to_message_id=update.message.message_id,
        text="Hey there!")


def view_product_shop_map(update: Update, context: CallbackContext):
    user_data = context.user_data

    product = user_data['search_product']
    shop_location = product['shop']['location']

    if shop_location:
        lat, lon = shop_location['coordinates']
        update.message.reply_location(
            latitude=lat,
            longitude=lon
        )
        update.message.reply_text(
            product['shop']['address']['address']
        )
    else:
        update.message.reply_text(
            'No se puede obtener la localizacion de la tienda'
        )


def product_report(update: Update, context: CallbackContext):
    query = update.callback_query
    product_id = query.data.split('-')[-1]

    product = context.user_data['search_product']
    render_report_options_product_inline(update, product)

    update.callback_query.answer()


def product_report_back(update: Update, context: CallbackContext):
    query = update.callback_query
    product_id = query.data.split('-')[-1]

    product = context.user_data['search_product']
    render_product_back(update, product, context.user_data)

    update.callback_query.answer()


def report(update: Update, context: CallbackContext):
    query = update.callback_query.data
    query = query.split('-')

    report_option = int(query[-1])
    product_id = query[-2]

    report = report_options[report_option-1][1]
    product = context.user_data['search_product']

    render_product_back(update, product, context.user_data)

    update.callback_query.answer(
        text=f"Este producto {product_id} ha sido reportado como {report}"
    )