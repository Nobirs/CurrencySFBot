import telebot
from pprint import pformat

from config import BOT_TOKEN, WIKI_CURRENCIES, CURRENCIES, POPULAR_CURRENCIES
from APIFixer import get_currency_list, get_price
from extensions import TMessageParseException, RequestException, parse_convert_message


bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start_help_handler(message: telebot.types.Message):
    text = "Бот предназначен для конвертирования валют.\n"\
            "Для использования введите <изначальная валюта> <валюта для результата> <количество для перевода>.\n"\
            f"Популярные валюты:\n\n{pformat(POPULAR_CURRENCIES)}\n\n"\
            "Чтобы увидеть список всех доступных валют введите: /values\n"\
            "Внимание! Для работы с валютами, не входящими в список выше, "\
            "необходимо использовать их обозначения(CNY, USD)\n"\
            "Для работы с большинством валют необходимо использовать формат записи <USD RUB 500>"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def get_values(message: telebot.types.Message):
    text = ""
    currencies = get_currency_list()
    count = 0
    for abbr, name in currencies.items():
        text += f'{abbr} -> {name}\n'
        count += 1
        if count >= 15:
            bot.send_message(message.chat.id, text)
            text = ""
            count = 0


@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    text = message.text
    try:
        currency_from, currency_to, amount = parse_convert_message(text)
        price = get_price(currency_from, currency_to, int(amount))
        result_text = f"{amount} {currency_from} -> {price} {currency_to}"
    except TMessageParseException as e:
        result_text = str(e)
    except RequestException as e:
        result_text = str(e)

    bot.send_message(message.chat.id, result_text)


bot.polling(none_stop=True)