import json
from typing import Dict
import requests

from decouple import config


API_URL = config('API_URL')

def is_shop_created(token: Dict):
    url = f"{API_URL}/me/shop"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        response = response.json()
        return response['data']
    
    return False


def do_shop_register(token: Dict, data: Dict) -> Dict:
    url = f"{API_URL}/shops/"
    path = data.pop('logo', None)
    payload = json.dumps(data)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access"]}',
    }
    response = requests.post(url, headers=headers, data=payload)
    response = response.json()
    shop_data = response["data"]

    if path:
        response = do_shop_logo_update(shop_data["id"], path, token)
        shop_data["logo"] = response["data"]["logo"]

    return shop_data


def do_shop_logo_update(shop_id: str, path: str, token: Dict) -> Dict:
    url = f"{API_URL}/shops/{shop_id}"

    filename = path.split('/')[-1]
    ext = filename.split('.')[-1]

    files = [
        ('logo', (filename, open(path, 'rb'), f"image/{ext}"))
    ]
    headers = {
        'Authorization': f'Bearer {token["access"]}'
    }
    response = requests.request("PATCH", url, headers=headers, data={}, files=files)
    return response.json()


def do_shop_update(token: Dict, shop_id: str, data: Dict) -> Dict:
    url = f"{API_URL}/shops/{shop_id}"
    payload = json.dumps(data)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access"]}',
    }
    response = requests.patch(url, headers=headers, data=payload)
    if response.status_code == 200:
        response = response.json()
        return response['data']
    else:
        return None


def get_shop(token: Dict, shop_id: str) -> Dict:
    url = f"{API_URL}/shops/{shop_id}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.request("GET", url, headers=headers)

    if response.status_code == 200:
        response = response.json()
        return response['data']
    else:
        return {}