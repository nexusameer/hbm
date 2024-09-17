import requests
import json
import hbm_app.python_scripts.config as config
from datetime import datetime

def pagination_handler(url):
    result = []
    while True:
        print(url)
        response = requests.get(url, headers=config.headers).json()
        result = result + response.get('results')
        if response.get('next'):
            url = response.get('next')
        else:
            return result


def rest_api_url(endpoint, **kwargs):
    url = f"{config.base_url}{endpoint}/" 
    if kwargs:
        url += '?'
        for key, value in kwargs.items():
            url += f'{key}={value}&'
    return url


def get_customers(**kwargs):
    endpoint = 'customers'
    url = rest_api_url(endpoint, **kwargs)
    return pagination_handler(url)


def get_transactions(**kwargs):
    endpoint = 'transactions'
    url = rest_api_url(endpoint, **kwargs)
    return pagination_handler(url)


def post_transaction(data):
    url = config.base_url + 'transactions/'
    return requests.post(url, data=json.dumps(data, default=str), headers=config.headers).json()

def post_action(data):
    url = config.base_url + 'actionlog/'
    return requests.post(url, data=json.dumps(data, default=str), headers=config.headers).json()

def end_action(action):
    url = f"{config.base_url}actionlog/{action.get('id')}/" 
    data = {
        'completed': True,
        'end_date': datetime.now()
    }
    return requests.patch(url, data=json.dumps(data, default=str), headers=config.headers).json()

def post_error(action, error):
    print("ERROR")
    print(error)
    url = config.base_url + 'error_log/'
    data = {
        "action": action.get('id'),
        "error": error
    }
    return requests.post(url, data=json.dumps(data, default=str), headers=config.headers).json()