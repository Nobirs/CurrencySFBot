import json
import requests

import config
from config import API_KEY, API_URL
from extensions import RequestException, check_status_code
from wiki_currencies_parser import get_dict_of_currencies_from_wiki


def get_currency_list() -> dict:
    """Get dict{"ABC":"currency name"} of available currencies using API."""
    request_url = API_URL + f'/symbols?apikey={API_KEY}'
    try:
        response = requests.get(request_url)
        # Raise exception if status code is incorrect.
        check_status_code(response.status_code, request_url)
        currencies = json.loads(response.content)['symbols']
    except RequestException as e:
        print(e)
        currencies = config.CURRENCIES

    wiki_currencies = get_dict_of_currencies_from_wiki()
    for abbr in currencies.keys():
        if abbr in wiki_currencies.keys():
            currencies[abbr] = wiki_currencies[abbr]
    return currencies


def get_price(c_from, c_to, c_amount):
    """Use API to get amount of currency_from in currency_to."""
    url = API_URL + f'/convert?to={c_to}&from={c_from}&amount={c_amount}'
    headers = {
        'apikey': API_KEY,
    }
    response = requests.request("GET", url, headers=headers)

    # Raise RequestException if status code is incorrect.
    check_status_code(response.status_code, url)

    response = json.loads(response.content)
    return response['result']
