import json
from typing import Dict
import requests

from decouple import config

from utils.helpers import timeit


API_URL = config('API_URL')

@timeit
def get_products(token: Dict, shop_id, page=1):
    url = f"{API_URL}/shops/{shop_id}/products?page={page}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.get(url, headers=headers, data={})
    response = response.json()

    return response['data'], response['count']