import json

import requests
from decouple import config

from modules.base.requests import (
    get_session_token,
)


API_URL = config('API_URL')


def do_register_request(data):
    url = f"{API_URL}/users/"
    photo_path = data.pop('photo', None)

    payload = json.dumps(data)
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 201:
        data = response.json()['data']
        username = data['username']
        password = data['telegram_user_id']
        response_login = get_session_token(username, password)
        
        if photo_path:
            response_update_photo = do_update_photo(photo_path, response_login['access'])
            response_update_photo_data = response_update_photo.json()['data']
        else:
            response_update_photo_data = data

        return response_update_photo_data, response_login

    else:
        print("response: ", response.json())
        return None, None


def do_update_photo(path, access):
    filename = path.split('/')[-1]
    ext = filename.split('.')[-1]
    url = f"{API_URL}/me"

    files = [
        ('photo', (filename, open(path, 'rb'), f"image/{ext}"))
    ]

    headers = {
        'Authorization': f'Bearer {access}'
    }

    response = requests.request("PATCH", url, headers=headers, data={}, files=files)
    return response