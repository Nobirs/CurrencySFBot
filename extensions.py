from config import POPULAR_CURRENCIES, CURRENCIES, WIKI_CURRENCIES


class RequestException(Exception):
    pass


class TMessageParseException(Exception):
    pass


def check_status_code(status_code, request_url):
    """Raise exception if response status code is incorrect."""
    if status_code // 100 == 3:
        raise RequestException(f"[{status_code}] Ошибка! Перенаправление на другую страницу.")
    elif status_code // 100 == 4:
        raise RequestException(f"[{status_code}] Ошибка! неверный запрос({request_url})")
    elif status_code // 100 == 5:
        raise RequestException(f"[{status_code}] Ошибка! Неполадки на запрашиваемом сервере...")


def parse_convert_message(message: str):
    """Parse message like <USD RUB 100>.
    Raise exception if message is incorrect"""
    a = message.split(" ")
    if len(a) != 3:
        raise TMessageParseException("Неправильный формат сообщения(количество параметров должно равняться "
                                     "3).\n<FROM> <TO> <AMOUNT>")
    else:
        currency_from, currency_to, amount = a
        try:
            amount = float(amount)
        except ValueError as e:
            raise TMessageParseException(f"Количество денег для конвертирования не является числом({amount}).")

        # Raise TMessageException if currency name is not available to convert.
        currency_from = convert_currency_to_ticker(currency_from)
        currency_to = convert_currency_to_ticker(currency_to)
    return currency_from, currency_to, amount


def convert_currency_to_ticker(currency_name: str):
    if len(currency_name) == 3:
        if currency_name in POPULAR_CURRENCIES.values():
            return currency_name
        elif currency_name in WIKI_CURRENCIES.keys():
            return currency_name
        elif currency_name in CURRENCIES.keys():
            return currency_name
        else:
            raise TMessageParseException(f"Ошибка! Неизвестная валюта - ({currency_name})")
    else:
        if currency_name.lower() in POPULAR_CURRENCIES.keys():
            return POPULAR_CURRENCIES[currency_name.lower()]
        elif currency_name in WIKI_CURRENCIES.values():
            for key, value in WIKI_CURRENCIES.items():
                if value == currency_name:
                    return key
        elif currency_name in CURRENCIES.values():
            for key, value in CURRENCIES.items():
                if value == currency_name:
                    return key
        else:
            raise TMessageParseException(f"Ошибка! Невозможно опознать валюту({currency_name})")