import json
from pprint import pprint
from typing import Dict
import requests

from decouple import config


API_URL = config('API_URL')

def do_post_create(token: Dict, data: Dict) -> Dict:
    url = f"{API_URL}/posts"

    path = data.pop('photo', None)
    filename = path.split('/')[-1]
    ext = filename.split('.')[-1]

    files = [
        ('photo', (filename, open(path, 'rb'), f"image/{ext}")),
        ('text', (None, data['text'])),
        ('as_shop', (None, data['as_shop'])),
    ]

    headers = {
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.post(url, headers=headers, data={}, files=files)
    response = response.json()

    return response


def get_feed(token: Dict) -> Dict:
    url = f"{API_URL}/feed"

    headers = {
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.get(url, headers=headers, data={})
    response = response.json()

    return response['data']