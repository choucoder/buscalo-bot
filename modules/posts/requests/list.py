import json
from typing import Dict, Tuple
import requests

from decouple import config

from utils.helpers import timeit


API_URL = config('API_URL')

@timeit
def get_posts(token: str, page=1) -> Tuple[Dict, int]:
    url = f"{API_URL}/me/posts?page={page}"

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.get(url, headers=headers, data={})
    response = response.json()

    return response['data'], response['count']