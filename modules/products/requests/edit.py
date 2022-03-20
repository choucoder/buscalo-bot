import json
from typing import Dict
import requests

from decouple import config
from utils.helpers import timeit


API_URL = config('API_URL')

@timeit
def do_update(token: Dict, data: Dict, product_id: str) -> Dict:
    url = "%s/products/%s" % (API_URL, product_id)
    
    payload = json.dumps(data)

    headers = {
        'Content-Type': "application/json",
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.patch(url, headers=headers, data=payload)
    response = response.json()

    return response["data"]

@timeit
def do_photo_update(token: Dict, path: str, product_id) -> Dict:
    url = "%s/products/%s" % (API_URL, product_id)

    filename = path.split('/')[-1]
    ext = filename.split('.')[-1]

    files = [
        ('photo', (filename, open(path, 'rb'), f"image/{ext}"))
    ]
    headers = {
        'Authorization': f'Bearer {token["access"]}'
    }

    response = requests.patch(url, headers=headers, data={}, files=files)
    response = response.json()

    return response["data"]