import json
from pprint import pprint
from typing import Dict
import requests

from decouple import config
from utils.helpers import timeit


API_URL = config('API_URL')


def get_feed(token: Dict) -> Dict:
    url = f"{API_URL}/feed"

    headers = {
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.get(url, headers=headers, data={})
    response = response.json()

    return response['data']


@timeit
def post_react(token: Dict, post_id: str) -> str:
    url = "%s/posts/%s/react" % (API_URL, post_id)
    
    payload = json.dumps({
        'type': 1
    })

    headers = {
        'Content-Type': "application/json",
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.patch(url, headers=headers, data=payload)
    
    if response.status_code == 201:
        return "Te gusto este post"
    elif response.status_code == 204:
        return "Ya no te gusta este post"
    else:
        return "Error de validacion de los datos"