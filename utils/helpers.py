from datetime import datetime, timedelta
import math
import os
import re
import time
from uuid import uuid4

from decouple import config


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

def create_persistence_path():
    storage_folder = config('PERSISTENCE_FOLDER')
    storage_filename = config('PERSISTENCE_FILENAME')

    if not os.path.exists(storage_folder):
        os.mkdir(storage_folder)
    
    return os.path.join(storage_folder, storage_filename)


def return_state_as_integer(state):
    return int.from_bytes(bytes(state.encode('utf-8')), 'little')


def get_unique_filename(ext='jpg'):
    media_folder = config('MEDIA_FOLDER')
    photo_folder = os.path.join(media_folder, 'photos')
    photo_filename = str(uuid4()).replace('-', '') + f'.{ext}'

    if not os.path.exists(media_folder):
        os.mkdir(media_folder)

    if not os.path.exists(photo_folder):
        os.mkdir(photo_folder)
        
    return os.path.join(photo_folder, photo_filename)


def calc_age(birthdate: datetime):
    today = datetime.today()
    diff = today - birthdate

    return math.floor(diff.days / 365)


def timeit(method):
    def timed(*args, **kwargs):
        ts = time.time()
        reply = method(*args, **kwargs)
        te = time.time()
        print(f"Elapsed time at {method.__name__.upper()} is: {te - ts}")
        
        return reply
    return timed


def get_time_ago(d1: datetime, d2: datetime) -> str:
    """
    minutos, horas, dias, semanas, meses, años
    """
    diff = d2 - (d1 - timedelta(hours=4))
    years = diff.days // 365
    months = diff.days // 30
    weeks = diff.days // 7
    days = diff.days
    hours = diff.seconds // 3600
    minuts = diff.seconds // 60

    ago_number = 0
    ago_string = ""

    if years:
        ago_string = "año" if years == 1 else "años"
        ago_number = years
    elif months:
        ago_string = "mes" if months == 1 else "meses"
        ago_number = months
    elif weeks:
        ago_string = "semana" if weeks == 1 else "semanas"
        ago_number = weeks
    elif days:
        ago_string = "dia" if days == 1 else "dias"
        ago_number = days
    elif hours:
        ago_string = "hora" if hours == 1 else "horas"
        ago_number = hours
    elif minuts:
        ago_string = "minuto" if minuts == 1 else "minutos"
        ago_number = minuts
    else:
        ago_string = "ahora"
        ago_number = diff.seconds

    if ago_string != "ahora":
        return f"hace {ago_number} {ago_string}"

    return "ahora"


def email_is_valid(email: str) -> bool:
    if re.fullmatch(regex, email):
        return True
    return False