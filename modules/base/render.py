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

    text += 'En este đ¤ bot puedes buscar productos/servicios cerca de ti y poder '
    text += 'contactar con sus proveedores via Telegram o WhatsApp. Ademas, puedes '
    text += 'hacer publicaciones de promociones, productos nuevos o simplemente '
    text += 'estados de WhatsApp de tu negocio para que las personas a tu alrededor '
    text += 'los vean y esten al tanto de lo que ofreces.\n\n'
    text += '*Estas son las secciones del menu principal*: :point_down::point_down: \n\n'
    text += '1. đ *Buscar productos:* Buscar cualquier producto o servicio que este a tu alrededor.\n\n'
    text += '2. đ *Interactuar:* Ver y publicar estados para que otras personas a tu alrededor lo vean. Puedes publicar estados con el perfil de tienda o de usuario.\n\n'
    text += '3. đŽ *Mis posts:* Ver todos los estados que has publicado\n\n'
    text += '4. đŦ *Mi tienda:* Gestiona tu tienda, agrega productos, servicios y mucho mas.\n\n'
    text += '5. âšī¸ *Feedback:* Enviar sugerencias acerca de este bot.\n\n'
    text += '6. âī¸ *Configuracion:* Configuracion de datos de perfil (nombre, foto, ubicacion, etc).\n\n'
    text += '*Importante:exclamation::exclamation:*\n'
    text += '_En este menu o en la seccion Interactuar, puedes agregar '
    text += 'un estado simplemente subiendo una foto y adjuntandole el texto '
    text += 'que quieras a esta imagen. Asi de simple_.\n'

    update.message.reply_text(
        emojize(text, use_aliases=True),
        parse_mode=ParseMode.MARKDOWN,
    )


def get_start_message() -> str:
    text = "\t\t\tEn esta secciÃŗn puedes buscar đ productos o servicios, publicar o ver estados đ, acceder a la secciÃŗn de tu tienda đŦ, ver los estados đŽ que has publicado y configurar âī¸ tu cuenta\n\nđ Presiona el botÃŗn en forma de clipđ, selecciona una foto y agregale un comentario para publicar un estado"
    return text


def get_photo_help():
    text = "ÂĄAgrega tu foto o hazte un selfie!\n\n"
    text += "đ Presiona el emoji del clipđ y selecciona una foto"

    return text

def get_shop_section_help():
    text = "\t\t\tEn esta secciÃŗn puedes â agregar productos a tu tienda, ver los productos que has agregado y modificar âī¸ la informaciÃŗn de tu tienda"
    return text


def get_shop_settings_section_help():
    text = "Aqui puedes configurar la đą moneda y los âī¸ datos de tu tienda\n\n"
    text = "Selecciona una opciÃŗn đđ"
    return text

def get_product_list_section_help():
    text = "\t\t\tAqui puedes ver tus productos, âī¸ editarlos y â eliminarlos"
    return text


def get_location_help():
    text = "đ Presiona el boton en forma de clipđ, selecciona ubicacion đy envia donde te encuentras"