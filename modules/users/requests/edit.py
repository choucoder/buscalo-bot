from ast import Bytes
import json
from typing import BinaryIO, Dict

import requests
from decouple import config

from modules.base.requests import (
    get_session_token,
)


API_URL = config('API_URL')


def do_user_update(token: Dict, data: Dict) -> Dict:
    url = f"{API_URL}/me"

    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access"]}'
    }

    response = requests.patch(url, headers=headers, data=payload)
    response = response.json()

    return response['data']


def do_user_photo_update(token: Dict, path: str) -> Dict:
    url = f"{API_URL}/me"

    filename = path.split('/')[-1]
    ext = filename.split('.')[-1]

    files = [
        ('photo', (filename, open(path, 'rb'), f"image/{ext}"))
    ]

    headers = {
        'Authorization': f'Bearer {token["access"]}'
    }

    response = requests.patch(url, headers=headers, files=files)
    response = response.json()

    return response['data']