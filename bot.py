from decimal import ConversionSyntax
from email.message import Message
import logging
import os
import sys

from modules.base import states
from modules.products.requests.search import product_search
from modules.shops.states import SHOP_DETAILS
sys.dont_write_bytecode = True

from emoji import emojize
from decouple import config
from requests import Session

from telegram import (
    ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, KeyboardButton, user, 
)
from telegram.callbackquery import CallbackQuery
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackQueryHandler,
    CallbackContext,
    Filters
)
from telegram.ext.picklepersistence import PicklePersistence

from utils.helpers import create_persistence_path
from modules.base.states import (
    WELCOME,
    USER_REGISTRATION,
)
from modules.welcome import callbacks as welcome_callbacks
from modules.welcome import states as welcome_states
from modules.base import states as base_states
from modules.base.requests import get_and_login_or_abort
from modules import shops
from modules import products
from modules import posts
from modules import feed
from modules import feedback
from modules import settings
from modules import users


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> str:
    user_data = context.user_data
    _ = user_data.pop('count_products', 0)

    if not update.effective_user.is_bot:
        if not user_data.get('token', None):
            user_id = update.effective_user.id
            response = get_and_login_or_abort(user_id)

            if not response:
                return users.callbacks.create.navigate_to_self(update, context)
            else:
                user_data['profile_data'] = response['user']
                user_data['token'] = response['token']
                return welcome_callbacks.start_app(update, context)
        else:
            return welcome_callbacks.start_app(update, context)

    else:
        update.message.reply_text(
            'No puedes registrarte porque eres un bot'
        )
        update.effective_user.decline_join_request(
            update.effective_chat.id
        )


def wrong(update: Update, context: CallbackContext) -> str:
    update.message.reply_text(
        "??"
    )


def main() -> None:
    PORT = int(os.environ.get('PORT', 8443))
    TOKEN = config('API_KEY')

    persistence = PicklePersistence(filename=create_persistence_path(), store_callback_data=True)
    updater = Updater(token=TOKEN, persistence=persistence, arbitrary_callback_data=True)

    dispatcher = updater.dispatcher

    message_handlers = [
        MessageHandler(Filters.photo, posts.callbacks.create.fast_post),
        MessageHandler(Filters.attachment, posts.callbacks.create.fast_post_attach),
    ]
    conversations = []

    shop_edit_curr_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), shops.callbacks.edit.back_currency),  
            MessageHandler(Filters.text & ~Filters.command, shops.callbacks.edit.update_currency),
        ],
        map_to_parent={
            shops.states.SHOP_EDIT_CURRENCY_BACK: shops.states.SHOP_SETTINGS
        },
        states={},
        fallbacks=[],
        persistent=True,
        name='shop_edit_curr'
    )
    conversations.append(shop_edit_curr_conv)

    shop_edit_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), shops.callbacks.edit.back),  
            MessageHandler(Filters.regex('Nombre$'), shops.callbacks.edit.name),
            MessageHandler(Filters.regex('Descripcion$'), shops.callbacks.edit.description),
            MessageHandler(Filters.regex('Logo$'), shops.callbacks.edit.logo),
            MessageHandler(Filters.regex('Ubicacion$'), shops.callbacks.edit.location),
            MessageHandler(Filters.regex('WhatsApp de tienda$'), shops.callbacks.edit.phone_number),
        ],
        states={
            shops.states.SHOP_EDIT_TYPING: [
                MessageHandler(Filters.regex('Atras$'), shops.callbacks.edit.back_to_edit_choosing),
                MessageHandler(Filters.text & ~Filters.command, shops.callbacks.edit.update_shop),
                MessageHandler(Filters.location & ~Filters.command, shops.callbacks.edit.update_location),
                MessageHandler(Filters.photo & ~Filters.command, shops.callbacks.edit.update_logo),
                MessageHandler(Filters.attachment & ~Filters.command, shops.callbacks.edit.update_logo_attach),
            ],
            shops.states.SHOP_EDIT_CHOOSING: [
                MessageHandler(Filters.regex('Atras$'), shops.callbacks.edit.back),  
                MessageHandler(Filters.regex('Nombre$'), shops.callbacks.edit.name),
                MessageHandler(Filters.regex('Descripcion$'), shops.callbacks.edit.description),
                MessageHandler(Filters.regex('Logo$'), shops.callbacks.edit.logo),
                MessageHandler(Filters.regex('Ubicacion$'), shops.callbacks.edit.location),
                MessageHandler(Filters.regex('WhatsApp de tienda$'), shops.callbacks.edit.phone_number),  
            ]
        },
        map_to_parent={
            shops.states.SHOP_EDIT_BACK: shops.states.SHOP_SETTINGS,
        },
        fallbacks=[],
        persistent=True,
        name='shop_edit',
    )
    conversations.append(shop_edit_conv)

    shop_settings_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), shops.callbacks.settings.back),
            MessageHandler(Filters.regex('Editar$'), shops.callbacks.edit.navigate_to_self),
            MessageHandler(Filters.regex('Moneda$'), shops.callbacks.edit.navigate_to_edit_currency)
        ],
        states={
            shops.states.SHOP_EDIT: [shop_edit_conv],
            shops.states.SHOP_EDIT_CURRENCY: [shop_edit_curr_conv],
        },
        map_to_parent={
            shops.states.SHOP_SETTINGS_BACK: shops.states.SHOP_MAIN,
            shops.states.SHOP_SETTINGS: shops.states.SHOP_SETTINGS
        },
        fallbacks={

        },
        persistent=True,
        name='shop_settings'
    )
    conversations.append(shop_settings_conv)

    product_edit_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), products.callbacks.edit.back),
            MessageHandler(Filters.regex('Nombre$'), products.callbacks.edit.name),
            MessageHandler(Filters.regex('Detalles$'), products.callbacks.edit.details),
            MessageHandler(Filters.regex('Precio$'), products.callbacks.edit.price),
            MessageHandler(Filters.regex('Foto$'), products.callbacks.edit.photo),
        ],
        states={
            products.states.PRODUCT_EDIT_TYPING: [
                MessageHandler(Filters.text & ~Filters.command, products.callbacks.edit.update_product),
                MessageHandler(Filters.photo, products.callbacks.edit.update_photo),
                MessageHandler(Filters.attachment, products.callbacks.edit.update_photo_attach),
            ],
            products.states.PRODUCT_EDIT_CHOOSING: [
                MessageHandler(Filters.regex('Atras$'), products.callbacks.edit.back),
                MessageHandler(Filters.regex('Nombre$'), products.callbacks.edit.name),
                MessageHandler(Filters.regex('Detalles$'), products.callbacks.edit.details),
                MessageHandler(Filters.regex('Precio$'), products.callbacks.edit.price),
                MessageHandler(Filters.regex('Foto$'), products.callbacks.edit.photo),     
            ],
        },
        map_to_parent={
            products.states.PRODUCT_EDIT_BACK: products.states.PRODUCT_LIST,
        },
        fallbacks=[],
        persistent=True,
        name='product_edit',
    )
    conversations.append(product_edit_conv)

    product_list_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), products.callbacks.list.back),
            MessageHandler(Filters.regex('Anterior$'), products.callbacks.list.prev),
            MessageHandler(Filters.regex('^Siguiente'), products.callbacks.list.next),
            MessageHandler(Filters.regex('Editar$'), products.callbacks.edit.navigate_to_self),
            MessageHandler(Filters.regex('Eliminar$'), products.callbacks.delete.navigate_to_self),
        ],
        states={
            products.states.PRODUCT_EDIT: [product_edit_conv],
        },
        map_to_parent={
            products.states.PRODUCT_LIST_BACK: shops.states.SHOP_MAIN,
            products.states.PRODUCT_LIST: products.states.PRODUCT_LIST,
        },
        fallbacks=[],
        persistent=True,
        name='product_list',
    )
    conversations.append(product_list_conv)

    product_create_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), products.callbacks.create.back),
            MessageHandler(Filters.text, products.callbacks.create.name),
        ],
        states={ 
            products.states.PRODUCT_DETAILS: [
                MessageHandler(Filters.regex('Atras$'), products.callbacks.create.back),
                MessageHandler(Filters.text, products.callbacks.create.details),
            ],
            products.states.PRODUCT_PRICE: [
                MessageHandler(Filters.regex('Atras$'), products.callbacks.create.back),
                MessageHandler(Filters.text, products.callbacks.create.price),
            ],
            products.states.PRODUCT_PHOTO: [
                MessageHandler(Filters.regex('Atras$'), products.callbacks.create.back),
                CommandHandler(
                    'omitir', products.callbacks.create.skip_photo
                ),
                MessageHandler(Filters.photo, products.callbacks.create.photo),
                MessageHandler(Filters.attachment, products.callbacks.create.photo_attach),
            ],
        },
        map_to_parent={
            products.states.PRODUCT_END_REGISTRATION: shops.states.SHOP_MAIN,
            products.states.PRODUCT_CREATE_BACK: shops.states.SHOP_MAIN,
        },
        fallbacks={

        },
        persistent=True,
        name='product_create',
    )
    conversations.append(product_create_conv)

    shop_create_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), shops.callbacks.create.back),
            MessageHandler(Filters.text, shops.callbacks.create.name)
        ],
        states={
            shops.states.SHOP_DESCRIPTION: [
                MessageHandler(Filters.regex('Atras$'), shops.callbacks.create.back),
                MessageHandler(
                    Filters.text, shops.callbacks.create.description
                )
            ],
            shops.states.SHOP_LOGO: [
                MessageHandler(
                    Filters.photo, shops.callbacks.create.logo
                ),
                MessageHandler(
                    Filters.attachment, shops.callbacks.create.logo_attach
                ),
                MessageHandler(Filters.regex('Atras$'), shops.callbacks.create.back),
            ],
            shops.states.SHOP_LOCATION: [
                MessageHandler(Filters.regex('Atras$'), shops.callbacks.create.back),
                MessageHandler(
                    Filters.location, shops.callbacks.create.location
                ),
            ],
        },
        map_to_parent={
            base_states.BACK: WELCOME,
            shops.states.END_SHOP_REGISTRATION: shops.states.SHOP_MAIN,
        },
        fallbacks=[],
        persistent=True,
        name='shop_create'
    )
    conversations.append(shop_create_conv)

    shop_main_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Producto$'), products.callbacks.create.navigate_to_self),
            MessageHandler(Filters.regex('Ver Productos$'), products.callbacks.list.navigate_to_self),
            MessageHandler(Filters.regex('Configuracion$'), shops.callbacks.settings.navigate_to_self),
            MessageHandler(Filters.regex('Atras$'), shops.callbacks.main.back),
            MessageHandler(Filters.text, shops.callbacks.create.test)
        ],
        states={
            products.states.PRODUCT_CREATE: [product_create_conv],
            products.states.PRODUCT_LIST: [product_list_conv],
            shops.states.SHOP_SETTINGS: [shop_settings_conv],
        },
        fallbacks=[],
        map_to_parent={
            base_states.BACK: WELCOME,
            shops.states.SHOP_MAIN: shops.states.SHOP_MAIN,
        },
        persistent=True,
        name='shop_main'
    )
    conversations.append(shop_main_conv)

    post_create_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.photo, posts.callbacks.create.photo),
            MessageHandler(Filters.attachment, posts.callbacks.create.photo_attach),
            MessageHandler(Filters.regex('Atras$'), posts.callbacks.create.back),
        ],
        states={
            posts.states.POST_CREATE_PUBLISHER_TYPE: [
                MessageHandler(Filters.regex('Atras$'), posts.callbacks.create.back),
                MessageHandler(Filters.regex('Usuario$'), posts.callbacks.create.publisher_type),
                MessageHandler(Filters.regex('Tienda$'), posts.callbacks.create.publisher_type),
            ],
        },
        fallbacks=[],
        map_to_parent={
            posts.states.POST_CREATE_BACK: feed.states.FEED,
        },
        persistent=True,
        name='post_create',
    )
    conversations.append(post_create_conv)

    shop_details_product_list_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), products.callbacks.list.back_non_owner),
            MessageHandler(Filters.regex('Anterior$'), products.callbacks.list.prev_non_owner),
            MessageHandler(Filters.regex('^Siguiente'), products.callbacks.list.next_non_owner),
        ],
        states={
        },
        map_to_parent={
            products.states.PRODUCT_LIST_BACK: shops.states.SHOP_DETAILS,
        },
        fallbacks=[],
        persistent=True,
        name='shop_details_product_list_conv',
    )
    conversations.append(shop_details_product_list_conv)

    shop_details_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), shops.callbacks.details.back),
            MessageHandler(Filters.regex('Ver productos$'), shops.callbacks.details.view_products),
        ],
        states={
            shops.states.SHOP_DETAILS_VIEW_PRODUCTS: [shop_details_product_list_conv]
        },
        fallbacks=[],
        map_to_parent={
            shops.states.SHOP_DETAILS_BACK: feed.states.FEED,
            shops.states.SHOP_DETAILS: shops.states.SHOP_DETAILS,
        },
        persistent=True,
        name='shop_details',
    )
    conversations.append(shop_details_conv)

    feed_selection_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Deslizar$'), feed.callbacks.list.swipe_down),
            MessageHandler(Filters.regex('Atras$'), feed.callbacks.list.back),
            MessageHandler(Filters.regex('Nuevo estado$'), posts.callbacks.create.navigate_to_self),
            MessageHandler(Filters.regex('Ver tienda$'), feed.callbacks.list.navigate_to_shop_details),
            CallbackQueryHandler(feed.callbacks.list.post_like, pattern='^LIKE_POST'),
            CallbackQueryHandler(feed.callbacks.list.report, pattern='^FEED_REPORT_OPTION'),
            CallbackQueryHandler(feed.callbacks.list.post_report_back, pattern='^REPORT_POST_BACK'),
            CallbackQueryHandler(feed.callbacks.list.post_report, pattern='^REPORT_POST'),
        ],
        states={
            posts.states.POST_CREATE: [post_create_conv],
            shops.states.SHOP_DETAILS: [shop_details_conv],
        },
        fallbacks=[],
        map_to_parent={
            feed.states.FEED_BACK: WELCOME,
            feed.states.FEED: feed.states.FEED,
        },
        persistent=True,
        name='feed_selection',
        per_message=False,
    )
    conversations.append(feed_selection_conv)

    search_range_settings_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), products.callbacks.search.back_search_range_settings),
            MessageHandler(Filters.regex(r'(5 Km|10 Km|20 Km|30 Km|40 Km|50 Km)'), products.callbacks.search.update_search_range_settings),
        ],
        states={},
        fallbacks=[],
        map_to_parent={
            products.states.SEARCH_RANGE_SETTINGS_BACK: products.states.SEARCH_SETTINGS
        },
        persistent=True,
        name='search_range_settings'
    )
    conversations.append(search_range_settings_conv)

    search_location_settings_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), products.callbacks.search.back_search_location_settings),
            MessageHandler(Filters.location, products.callbacks.search.update_search_location_settings),
        ],
        states={},
        fallbacks=[],
        map_to_parent={
            products.states.SEARCH_LOCATION_SETTINGS_BACK: products.states.SEARCH_SETTINGS,
        },
        persistent=True,
        name='search_location_settings',
    )
    conversations.append(search_location_settings_conv)

    search_settings_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), products.callbacks.search.back_search_settings),
            MessageHandler(Filters.regex('Radio de busqueda$'), products.callbacks.search.navigate_to_search_range_settings),
            MessageHandler(Filters.regex('Ubicacion$'), products.callbacks.search.navigate_to_search_location_settings),
        ],
        states={
            products.states.SEARCH_RANGE_SETTINGS: [
                search_range_settings_conv
            ],
            products.states.SEARCH_LOCATION_SETTINGS: [
                search_location_settings_conv
            ],
        },
        fallbacks=[],
        map_to_parent={
            products.states.SEARCH_SETTINGS: products.states.SEARCH_SETTINGS,
            products.states.SEARCH_SETTINGS_BACK: products.states.PRODUCT_SEARCH,
        },
        persistent=True,
        name='search_settings',
    )
    conversations.append(search_settings_conv)

    shop_search_view_products_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), shops.callbacks.search.back_to_shop_search),
            MessageHandler(Filters.regex('Anterior$'), shops.callbacks.search.prev_product),
            MessageHandler(Filters.regex('^Siguiente'), shops.callbacks.search.next_product),
        ],
        states={
        },
        map_to_parent={
            shops.states.SHOP_SEARCH_VIEW_PRODUCTS_BACK: shops.states.SHOP_SEARCH,
            shops.states.SHOP_SEARCH_VIEW_PRODUCTS: shops.states.SHOP_SEARCH_VIEW_PRODUCTS,
        },
        fallbacks=[],
        persistent=True,
        name='shop_search_view_products_conv',
    )
    conversations.append(shop_search_view_products_conv)

    shop_search_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), shops.callbacks.search.back),
            MessageHandler(Filters.regex('Ver productos$'), shops.callbacks.search.navigate_to_view_products),
        ],
        states={
            shops.states.SHOP_SEARCH_VIEW_PRODUCTS: [
                shop_search_view_products_conv,
            ]
        },
        fallbacks=[],
        map_to_parent={
            shops.states.SHOP_SEARCH_BACK: products.states.PRODUCT_SEARCH,
            shops.states.SHOP_SEARCH: shops.states.SHOP_SEARCH,
        },
        persistent=True,
        name='shop_search_conv',
        per_message=False,
    )
    conversations.append(shop_search_conv)

    product_search_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), products.callbacks.search.back),
            MessageHandler(Filters.regex('Anterior$'), products.callbacks.search.prev),
            MessageHandler(Filters.regex('^Siguiente'), products.callbacks.search.next),
            MessageHandler(Filters.regex('Ver ubicacion de tienda$'), products.callbacks.search.view_product_shop_map),
            MessageHandler(Filters.regex('Configuracion de busqueda$'), products.callbacks.search.navigate_to_search_settings),
            MessageHandler(Filters.text & (~Filters.command), products.callbacks.search.handle_query),
            CallbackQueryHandler(products.callbacks.search.view_store_products_next, pattern='^VIEW_STORE_PRODUCTS_NEXT'),
            CallbackQueryHandler(products.callbacks.search.view_store_products_prev, pattern='^VIEW_STORE_PRODUCTS_PREV'),
            CallbackQueryHandler(products.callbacks.search.view_store_products_back, pattern='^VIEW_STORE_PRODUCTS_BACK'),
            CallbackQueryHandler(products.callbacks.search.view_store_products, pattern='^VIEW_STORE_PRODUCTS'),
            CallbackQueryHandler(products.callbacks.search.like_product, pattern='^LIKE_PRODUCT'),
            CallbackQueryHandler(products.callbacks.search.chat, pattern='^CHAT'),
            CallbackQueryHandler(products.callbacks.search.report, pattern='^PRODUCT_REPORT_OPTION'),
            CallbackQueryHandler(products.callbacks.search.product_report_back, pattern='^REPORT_PRODUCT_BACK'),
            CallbackQueryHandler(products.callbacks.search.product_report, pattern='^REPORT_PRODUCT'),
        ],
        states={
            products.states.SEARCH_SETTINGS: [
                search_settings_conv,
            ],
            shops.states.SHOP_SEARCH: [
                shop_search_conv,
            ],
        },
        fallbacks=[],
        map_to_parent={
            products.states.PRODUCT_SEARCH_BACK: WELCOME,
            products.states.PRODUCT_SEARCH: products.states.PRODUCT_SEARCH
        },
        persistent=True,
        name='product_search',
        per_message=False,
    )
    conversations.append(product_search_conv)

    post_list_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), posts.callbacks.list.back),
            MessageHandler(Filters.regex('Anterior$'), posts.callbacks.list.prev),
            MessageHandler(Filters.regex('^Siguiente'), posts.callbacks.list.next),
            MessageHandler(Filters.regex('Eliminar$'), posts.callbacks.delete.navigate_to_self),
        ],
        states={
        },
        map_to_parent={
            posts.states.POST_LIST_BACK: WELCOME,
            posts.states.POST_LIST: posts.states.POST_LIST,
        },
        fallbacks=[],
        persistent=True,
        name='post_list',
    )
    conversations.append(post_list_conv)

    feedback_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), feedback.callbacks.create.back),
            MessageHandler(Filters.text & ~Filters.command, feedback.callbacks.create.send),
        ],
        states={},
        map_to_parent={
            feedback.states.FEEDBACK_BACK: WELCOME,
        },
        fallbacks=[],
        persistent=True,
        name='feedback',
    )
    conversations.append(feedback_conv)

    user_edit_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), users.callbacks.edit.back),
            MessageHandler(Filters.regex('Nombre$'), users.callbacks.edit.first_name),
            MessageHandler(Filters.regex('Apellido$'), users.callbacks.edit.last_name),
            MessageHandler(Filters.regex('Fecha nacimiento$'), users.callbacks.edit.birthdate),
            MessageHandler(Filters.regex('Genero$'), users.callbacks.edit.gender),
            MessageHandler(Filters.regex('Foto$'), users.callbacks.edit.photo),
            MessageHandler(Filters.regex('Ubicacion$'), users.callbacks.edit.location),
        ],
        states={
            users.states.USER_EDIT_TYPING: [
                MessageHandler(Filters.regex('Atras$'), users.callbacks.edit.back_to_edit_choosing),
                MessageHandler(Filters.text & ~Filters.command, users.callbacks.edit.update_text_fields),
                MessageHandler(Filters.location, users.callbacks.edit.update_location),
                MessageHandler(Filters.photo, users.callbacks.edit.update_photo),
                MessageHandler(Filters.attachment, users.callbacks.edit.update_photo_attach),
            ],
            users.states.USER_EDIT_CHOOSING: [
                MessageHandler(Filters.regex('Atras$'), users.callbacks.edit.back),
                MessageHandler(Filters.regex('Nombre$'), users.callbacks.edit.first_name),
                MessageHandler(Filters.regex('Apellido$'), users.callbacks.edit.last_name),
                MessageHandler(Filters.regex('Fecha nacimiento$'), users.callbacks.edit.birthdate),
                MessageHandler(Filters.regex('Genero$'), users.callbacks.edit.gender),
                MessageHandler(Filters.regex('Foto$'), users.callbacks.edit.photo),
                MessageHandler(Filters.regex('Ubicacion$'), users.callbacks.edit.location),
            ],
        },
        map_to_parent={
            users.states.USER_EDIT_BACK: settings.states.SETTINGS
        },
        fallbacks=[],
        persistent=True,
        name='user_edit',
    )
    conversations.append(user_edit_conv)

    settings_account_delete_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Cancelar$'), settings.callbacks.account.delete_cancel),
            MessageHandler(Filters.regex('Continuar$'), settings.callbacks.account.delete_confirm),
        ],
        states={},
        map_to_parent={
            settings.states.SETTINGS_ACCOUNT_DELETE_CANCEL: settings.states.SETTINGS_ACCOUNT,
        },
        fallbacks=[],
        persistent=True,
        name='settings_account_delete',
    )
    # conversations.append(settings_account_delete_conv)

    settings_account_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), settings.callbacks.account.back),
            MessageHandler(Filters.regex('Eliminar cuenta$'), settings.callbacks.account.navigate_to_self_delete),
        ],
        states={
            settings.states.SETTINGS_ACCOUNT_DELETE: [
                settings_account_delete_conv
            ]
        },
        map_to_parent={
            settings.states.SETTINGS_ACCOUNT_BACK: settings.states.SETTINGS,
            settings.states.SETTINGS_ACCOUNT: settings.states.SETTINGS_ACCOUNT,
        },
        fallbacks=[],
        persistent=True,
        name='settings_account',
    )
    conversations.append(settings_account_conv)

    settings_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Atras$'), settings.callbacks.main.back),
            MessageHandler(Filters.regex('Perfil$'), users.callbacks.edit.navigate_to_self),
            MessageHandler(Filters.regex('Cuenta$'), settings.callbacks.account.navigate_to_self),
        ],
        states={
            users.states.USER_EDIT: [user_edit_conv],
            settings.states.SETTINGS_ACCOUNT: [settings_account_conv],
        },
        map_to_parent={
            settings.states.SETTINGS_BACK: WELCOME,
            settings.states.SETTINGS: settings.states.SETTINGS
        },
        fallbacks=[],
        persistent=True,
        name='settings',
    )
    conversations.append(settings_conv)

    welcome_selection_conv = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('Interactuar$'), feed.callbacks.list.navigate_to_self),
            MessageHandler(Filters.regex('Mi tienda$'), shops.callbacks.main.navigate_to_self),
            MessageHandler(Filters.regex('Buscar productos$'), products.callbacks.search.navigate_to_self),
            MessageHandler(Filters.regex('Mis posts$'), posts.callbacks.list.navigate_to_self),
            MessageHandler(Filters.regex('Feedback$'), feedback.callbacks.create.navigate_to_self),
            MessageHandler(Filters.regex('Configuracion$'), settings.callbacks.main.navigate_to_self),
            MessageHandler(Filters.text & (~Filters.command), posts.callbacks.create.fast_post_text),
            CommandHandler('start', start),
        ],
        states={
            feed.states.FEED: [feed_selection_conv],
            shops.states.SHOP_MAIN: [shop_main_conv],
            shops.states.SHOP_CREATE: [shop_create_conv],
            products.states.PRODUCT_SEARCH: [product_search_conv],
            posts.states.POST_LIST: [post_list_conv],
            feedback.states.FEEDBACK: [feedback_conv],
            settings.states.SETTINGS: [settings_conv],
        },
        fallbacks=[
        ],
        map_to_parent={
            WELCOME: WELCOME
        },
        persistent=True,
        name='welcome',
    )

    user_registration_conv = ConversationHandler(
        entry_points=[
            MessageHandler(
                Filters.regex('(Masculino|Femenino|Prefiero no decir)$'),
                users.callbacks.create.gender
            )
        ],
        states={
            users.states.FIRST_NAME: [
                MessageHandler(
                    Filters.text, users.callbacks.create.first_name
                ),
            ],
            users.states.LAST_NAME: [
                MessageHandler(
                    Filters.text, users.callbacks.create.last_name
                )
            ],
            users.states.AGE: [
                MessageHandler(
                    Filters.text, users.callbacks.create.age
                )
            ],
            users.states.EMAIL: [
                CommandHandler(
                    'Omitir', users.callbacks.create.skip_email
                ),
                MessageHandler(
                    Filters.text, users.callbacks.create.email
                )
            ],
            users.states.PHOTO: [
                MessageHandler(
                    Filters.photo, users.callbacks.create.photo
                ),
                MessageHandler(
                    Filters.attachment, users.callbacks.create.photo_attach
                )
            ],
            users.states.LOCATION: [
                MessageHandler(
                    Filters.location, users.callbacks.create.location
                ),
                CommandHandler(
                    'Omitir', users.callbacks.create.skip_location
                ),
            ],
            users.states.ACCEPT_CONDITIONS: [
                MessageHandler(
                    Filters.regex('^Aceptar$'),
                    users.callbacks.create.accept_conditions
                )
            ]
        },
        map_to_parent={
            WELCOME: WELCOME,
        },
        fallbacks=[MessageHandler(Filters.all, wrong)],
        persistent=True,
        name='user_registration',
    )
    conversations.append(user_registration_conv)
    # Noobs
    settings_account_delete_conv.states[USER_REGISTRATION] = [
        user_registration_conv
    ]

    start_conversation = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
        ],
        states={
            USER_REGISTRATION: [user_registration_conv],
            WELCOME: [welcome_selection_conv],
        },
        fallbacks=[],
        persistent=True,
        name='start_conversation',
    )

    # Adding /start command to all conversations
    for i in range(len(conversations)):
        conv = conversations[i]
        conv.entry_points.append(CommandHandler('start', start))
        conv.map_to_parent[WELCOME] = WELCOME
        conv.fallbacks.append(MessageHandler(Filters.all, wrong))

    # Adding handler for create a post
    welcome_selection_conv.entry_points.extend(message_handlers)
    product_search_conv.entry_points.extend(message_handlers)
    feed_selection_conv.entry_points.extend(message_handlers)

    dispatcher.add_handler(start_conversation)
    updater.start_webhook(listen='0.0.0.0',
                          port=int(PORT),
                          url_path=TOKEN,
                          webhook_url='https://buscalobot.herokuapp.com/' + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()