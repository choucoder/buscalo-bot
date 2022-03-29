import json
from typing import Dict

import requests
from decouple import config


API_URL = config('API_URL')


def do_user_delete(token: Dict) -> requests.Response:
    url = f"{API_URL}/users"

    payload = json.dumps({})
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access"]}'
    }

    response = requests.delete(url, headers=headers, data=payload)
    return response