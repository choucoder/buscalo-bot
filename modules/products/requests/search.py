import json
from typing import Dict
import requests

from decouple import config
from utils.helpers import timeit


API_URL = config('API_URL')

@timeit
def product_search(token: Dict, query: Dict, page=1) -> Dict:
    if page == 1:
        url = f"{API_URL}/products?name={query}"
    else:
        url = f"{API_URL}/products?name={query}&page={page}"

    payload = json.dumps({})

    headers = {
        'Content-Type': "application/json",
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.get(url, headers=headers, data=payload)
    response = response.json()

    return response['data'], response['count']


@timeit
def do_update_search_settings(token: Dict, data: Dict) -> Dict:
    url = f"{API_URL}/me/settings"

    payload = json.dumps(data)

    headers = {
        'Content-Type': "application/json",
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.patch(url, headers=headers, data=payload)
    response = response.json()

    return response['data']

@timeit
def get_product(token: Dict, product_id: str) -> Dict:
    url = "%s/products/%s" % (API_URL, product_id)
    
    payload = json.dumps({})

    headers = {
        'Content-Type': "application/json",
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.get(url, headers=headers, data=payload)
    if response.status_code == 200:
        response = response.json()
        return response["data"]
    else:
        return {}

@timeit
def rating_product(token: Dict, product_id: str) -> str:
    url = "%s/products/%s/rating" % (API_URL, product_id)
    
    payload = json.dumps({
        'rating': 5
    })

    headers = {
        'Content-Type': "application/json",
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.patch(url, headers=headers, data=payload)
    
    if response.status_code == 201:
        return "Te gusto este producto"
    elif response.status_code == 204:
        return "Ya no te gusta este producto"
    elif response.status_code == 404:
        return "El producto al que intentas reaccionar ya no esta disponible"
    else:
        return "Error de validacion de los datos"

@timeit
def do_product_report(token: Dict, product_id: str, type_id: str) -> Dict:
    url = f"{API_URL}/reports"
    
    payload = json.dumps({
        'id': product_id,
        'issued_by_model': 1,
        'type': type_id,
    })

    headers = {
        'Content-Type': "application/json",
        'Authorization': f'Bearer {token["access"]}',
    }

    response = requests.post(url, headers=headers, data=payload)
    return response