from datetime import datetime, timedelta
import json
from typing import Dict
import requests

from decouple import config

from utils.helpers import timeit


API_URL = config('API_URL')


def get_session_token_until_success(username, password):
    response = get_session_token(username, password)

    while response and response.status_code != 200:
        response = get_session_token(username, password)
    
    return response


def get_session_token(username, password):
    url = f"{API_URL}/token/"
    payload = json.dumps({
        "username": username,
        "password": password
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    response_json = response.json()
    
    access_token_expires_at = datetime.today() + timedelta(days=1)
    refresh_token_expires_at = datetime.today() + timedelta(days=15)

    response_json['access_token_expires_at'] = str(access_token_expires_at)
    response_json['refresh_token_expires_at'] = str(refresh_token_expires_at)
    
    return response_json


def refresh_session_token(refresh_token):
    endpoint = f"{API_URL}/token/refresh/"

    payload = json.dumps({
        "refresh": refresh_token
    })
    headers = {
        "Content-Type": "application/json"
    }

    response = requests.request("POST", endpoint, headers=headers, data=payload)
    response_json = response.json()

    access_token_expires_at = datetime.today() + timedelta(days=1)
    refresh_token_expires_at = datetime.today() + timedelta(days=15)

    response_json['access_token_expires_at'] = str(access_token_expires_at)
    response_json['refresh_token_expires_at'] = str(refresh_token_expires_at)

    return response_json


def is_still_authorized(access_token):
    endpoint = f"{API_URL}/me"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        return True

    return False


@timeit
def get_token_or_refresh(user_data):
    token = user_data['token'].copy()
    today = datetime.today()
    access_expires_at = token.get('access_token_expires_at', str(today - timedelta(days=-3)))
    access_expires_at = datetime.strptime(access_expires_at, "%Y-%m-%d %H:%M:%S.%f")

    if today >= (access_expires_at - timedelta(minutes=5)):
        refresh_expires_at = token.get('refresh_token_expires_at', str(today - timedelta(days=-3)))
        refresh_expires_at = datetime.strptime(refresh_expires_at, "%Y-%m-%d %H:%M:%S.%f")

        if today >= (refresh_expires_at - timedelta(minutes=5)):
            token = refresh_session_token(token['refresh'])
        else:
            username = user_data['profile_data']['username']
            password = user_data['profile_data']['telegram_user_id']

            token = get_session_token(username, password)
    else:
        print("[INFO] Token de acceso no ha expirado")

    user_data['token'] = token

    return token


def get_user(token):
    endpoint = f"{API_URL}/me"

    headers = {
        'Authorization': f'Bearer {token["access"]}',
        "Content-Type": "application/json",
    }
    response = requests.get(endpoint, headers=headers)
    response = response.json()
    
    return response['data']


def get_and_login_or_abort(user_id: str) -> Dict:
    endpoint = f"{API_URL}/aux/users"

    headers = {
        "Content-Type": "application/json",
    }
    payload = json.dumps({
        "bot_username": "buscalo",
        "bot_password": "buscalopassword",
        "telegram_user_id": user_id
    })

    response = requests.request("POST", endpoint, headers=headers, data=payload)
    if response.status_code == 200:
        response = response.json()
        username = response['data']['telegram_username']
        password = response['data']['telegram_user_id']
        token =  get_session_token(username=username, password=password)

        return {'user': response['data'], 'token': token}
    else:
        return {}
