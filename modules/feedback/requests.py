import json
from typing import Dict
import requests

from decouple import config


API_URL = config('API_URL')

def send_feedback(token: Dict, data: Dict) -> Dict:
    url = f"{API_URL}/feedback"

    headers = {
        'Authorization': f'Bearer {token["access"]}',
        'Content-Type': 'application/json'
    }

    payload = json.dumps(data)

    response = requests.post(url, headers=headers, data=payload)
    response = response.json()

    return response