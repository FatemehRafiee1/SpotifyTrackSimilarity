import os
import time
import logging
import requests

from get_access import get_access_key

def handle_rate_limiting(response):
    retry_after = int(response.headers.get('Retry-After', 1))
    logging.warning(f"Rate limited. Retrying after {retry_after} seconds.")
    time.sleep(retry_after)

def get_response(url, headers):
    global access_token
    while True: 
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429: 
            handle_rate_limiting(response)
        elif response.status_code == 401: 
            get_access_key()
            access_token = os.getenv('ACCESS_TOKEN')
        else:
            error_msg = f"Error {response.status_code}: {response.text}"
            logging.error(error_msg)
            raise Exception(error_msg)