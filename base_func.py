import requests
import json

from google_sheets import get_google_sheet_data


def get_data(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        }
        req = requests.get(url, headers, timeout=3.1)
        if req:
            res = json.loads(req.text)
        else:
            res = {}
    except requests.exceptions.ConnectTimeout:
        res = {}
    except requests.exceptions.ReadTimeout:
        res = {}
    return res


def get_data_no_timeout(url):
    try:
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        }
        req = requests.get(url, headers)
        if req:
            res = json.loads(req.text)
        else:
            res = {}
    except requests.exceptions.ConnectTimeout:
        res = {}
    except requests.exceptions.ReadTimeout:
        res = {}
    return res


def get_table_prices():
    buy_prices = {}
    sell_prices = {}
    covens_rc_list = []
    bnb_price = float(get_google_sheet_data('B10')[0][0].replace(',', '.'))
    orkl_price = float(get_google_sheet_data('B11')[0][0].replace(',', '.'))
    taxes = float(get_google_sheet_data('B12')[0][0].replace(',', '.'))
    profit = float(get_google_sheet_data('B13')[0][0].replace(',', '.'))
    commission = float(get_google_sheet_data('B14')[0][0].replace(',', '.'))
    wizard_range_data = 'A3:B7'
    wizard_data = get_google_sheet_data(wizard_range_data)
    scepter_range_data = 'E3:F23'
    scepter_data = get_google_sheet_data(scepter_range_data)
    coven_range_data = 'I3:I43'
    coven_data = get_google_sheet_data(coven_range_data)
    for wizard_price in wizard_data:
        buy_prices[wizard_price[0]] = float(wizard_price[1].replace(',', '.')) * commission - (
                    taxes * bnb_price / orkl_price + profit / orkl_price)
        sell_prices[wizard_price[0]] = float(wizard_price[1].replace(',', '.'))
    for scepter_price in scepter_data:
        buy_prices[scepter_price[0]] = float(scepter_price[1].replace(',', '.')) * commission - (
                    taxes * bnb_price / orkl_price + profit / orkl_price)
        sell_prices[scepter_price[0]] = float(scepter_price[1].replace(',', '.'))
    for coven in coven_data:
        covens_rc_list.append(coven[0])
    return buy_prices, sell_prices, covens_rc_list


def cut_digits(number):
    return f"{number:.1f}"
