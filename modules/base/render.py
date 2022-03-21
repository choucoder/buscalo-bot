import datetime
from typing import Dict
from venv import create

from emoji import emojize
from geopy.distance import geodesic
from telegram import (
    InlineKeyboardMarkup, Update, ParseMode
)
import requests
from decouple import config

from utils.helpers import get_time_ago


def render_send_location_help(update: Update):
    text = ''
    text += '*Como enviar tu ubicacion?*\n\n'
    text += '\t\t1. Presiona el icono de archivo adjunto (:paperclip:) en el campo del mensaje :point_down:.\n'
    text += '\t\t2. Una vez aparezcan las opciones en la pantalla, selecciona *Ubicacion* :round_pushpin:.\n'
    text += '\t\t3. Si te sale el mensaje "`Permitir a telegram usar tu ubicacion`", debes aceptar para poder continuar.\n'
    text += '\t\t4. Una vez aceptada, puedes enviar tu ubicacion actual o establecer una nueva ubicacion y enviar esta.\n'

    update.message.reply_text(
        emojize(text, use_aliases=True),
        parse_mode=ParseMode.MARKDOWN,
    )


def start_help(update: Update):
    text = ''

    text += 'En este 🤖 bot puedes buscar productos/servicios cerca de ti y poder '
    text += 'contactar con sus proveedores via Telegram o WhatsApp. Ademas, puedes '
    text += 'hacer publicaciones de promociones, productos nuevos o simplemente '
    text += 'estados de WhatsApp de tu negocio para que las personas a tu alrededor '
    text += 'los vean y esten al tanto de lo que ofreces.\n\n'
    text += '*Estas son las secciones del menu principal*: :point_down::point_down: \n\n'
    text += '1. 🔎 *Buscar productos:* Buscar cualquier producto o servicio que este a tu alrededor.\n\n'
    text += '2. 🌎 *Interactuar:* Ver y publicar estados para que otras personas a tu alrededor lo vean. Puedes publicar estados con el perfil de tienda o de usuario.\n\n'
    text += '3. 📮 *Mis posts:* Ver todos los estados que has publicado\n\n'
    text += '4. 🏬 *Mi tienda:* Gestiona tu tienda, agrega productos, servicios y mucho mas.\n\n'
    text += '5. ℹ️ *Feedback:* Enviar sugerencias acerca de este bot.\n\n'
    text += '6. ⚙️ *Configuracion:* Configuracion de datos de perfil (nombre, foto, ubicacion, etc).\n\n'
    text += '*Importante:exclamation::exclamation:*\n'
    text += '_En este menu o en la seccion Interactuar, puedes agregar '
    text += 'un estado simplemente subiendo una foto y adjuntandole el texto '
    text += 'que quieras a esta imagen. Asi de simple_.\n'

    update.message.reply_text(
        emojize(text, use_aliases=True),
        parse_mode=ParseMode.MARKDOWN,
    )


def get_start_message() -> str:
    text = "En esta sección puedes buscar 🔎 productos o servicios, publicar o ver estados 🌎, acceder a la sección de tu tienda 🏬, ver los estados 📮 que has publicado y configurar ⚙️ tu cuenta\n\n👇 Presiona el botón en forma de clip📎, selecciona una foto y agregale un comentario para publicar un estado"
    return text


def get_photo_help():
    text = "¡Agrega tu foto o hazte un selfie!\n\n"
    text += "👇 Presiona el emoji del clip📎 y selecciona una foto"

    return text

def get_shop_section_help():
    text = "En esta sección puedes ➕ agregar productos a tu tienda, ver los productos que has agregado y modificar ⚙️ la información de tu tienda"
    return text


def get_shop_settings_section_help():
    text = "Aqui puedes configurar la 💱 moneda y los ✏️ datos de tu tienda\n\n"
    text = "Selecciona una opción 👇👇"
    return text

def get_product_list_section_help():
    text = "Aqui puedes ver tus productos, ✏️ editarlos y ❌ eliminarlos"
    return text


def get_location_help():
    text = "👇 Presiona el boton en forma de clip📎, selecciona ubicacion 📍y envia donde te encuentras"