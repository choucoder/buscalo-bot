from typing import Dict
import requests

from decouple import config
from utils.helpers import timeit


API_URL = config('API_URL')

@timeit
def do_delete(token: Dict, product_id) -> None:
    url = "%s/products/%s" % (API_URL, product_id)

    headers = {
        'Authorization': f'Bearer {token["access"]}'
    }

    response = requests.delete(url, headers=headers, data={})

    return response