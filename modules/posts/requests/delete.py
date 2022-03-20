from typing import Dict
import requests

from decouple import config
from utils.helpers import timeit


API_URL = config('API_URL')

@timeit
def do_delete(token: Dict, post_id) -> None:
    url = "%s/posts/%s" % (API_URL, post_id)

    headers = {
        'Authorization': f'Bearer {token["access"]}'
    }

    response = requests.delete(url, headers=headers, data={})

    return response