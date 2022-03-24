import json
from typing import Dict
import requests

from decouple import config


API_URL = config('API_URL')

def do_product_register(token: Dict, data: Dict, shop_id: str) -> Dict:
    url = f"{API_URL}/shops/{shop_id}/products"
    path = data.pop('photo', None)
    payload = json.dumps(data)

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access"]}',
    }
    response = requests.post(url, headers=headers, data=payload)
    response = response.json()
    product_data = response["data"]

    if path:
        response = do_product_photo_update(product_data["id"], path, token)
        product_data["photo"] = response["data"]["photo"]

    return product_data


def do_product_photo_update(product_id: str, path: str, token: Dict) -> Dict:
    url = f"{API_URL}/products/{product_id}"

    filename = path.split('/')[-1]
    ext = filename.split('.')[-1]

    files = [
        ('photo', (filename, open(path, 'rb'), f"image/{ext}"))
    ]
    headers = {
        'Authorization': f'Bearer {token["access"]}'
    }
    response = requests.request("PATCH", url, headers=headers, data={}, files=files)
    return response.json()
