import requests
from bs4 import BeautifulSoup

from extensions import check_status_code
from config import WIKI_URL, WIKI_CURRENCIES


def get_dict_of_currencies_from_wiki():
    """Parse wiki table and get names and abbreviates of currencies.
    Use default values from config if parsing failed."""
    currencies = {}
    try:
        response = requests.get(WIKI_URL)
        check_status_code(response.status_code, WIKI_URL)
        html = response.content
        soup = BeautifulSoup(html, 'lxml')
        table = soup.find_all('table')[1]

        for row in table.find_all('tr')[2:]:
            currency_name = str(row.td.text).strip("\n")
            currency_country = str(row.find_all('td')[1].get_text()).strip("\n")
            currency_abbr = str(row.find_all('td')[2].get_text()).strip("\n")
            currencies[currency_abbr] = f'{currency_name}({currency_country})'.replace("\xa0", " ")
    except Exception as e:
        print(e)
        currencies = WIKI_CURRENCIES
    return currencies
