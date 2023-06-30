import time

import requests
import json
import asyncio
import aiohttp

from datetime import datetime

from base_func import get_data, get_table_prices, cut_digits
from google_sheets import get_google_sheet_data
from tg_bot import send_text_message, message
from keys import *


def get_covens(covens_list):
    for interval in covens_list:
        if "RC" in interval:
            rc_interval = interval[3:].split("-")
            min_rc = rc_interval[0]
            max_rc = rc_interval[1]
            url = f"https://backend.orakler.com/covens?per_page=10&page=1&min_price=0&max_price=1000&min_rc={min_rc}&max_rc={max_rc}&property=all&sort=price"
            data = get_data(url)
            covens_list = data['data']
            get_covens_structure(covens_list)


def get_covens_structure(covens_list):
    for coven in covens_list:
        wizards_list = []
        scepters_list = []
        durability = [[], []]
        for wizard in coven['wizards']:
            wizards_list.append(wizard['scepters'])
            durability[0].append(wizard['durability'])
        for scepter in coven['scepters']:
            scepters_list.append(scepter['researchCapacity'])
            durability[1].append(scepter['durability'])
        coven_price = float(coven['price'])
        coven_real_price = get_coven_real_price(wizards_list, scepters_list, durability)
        if coven_real_price > coven_price:
            coven_info = f"Coven RC {coven['totalResearchCapacity']}, price {cut_digits(coven_price)}, " \
                   f"sell price {cut_digits(coven_real_price)}, " \
                   f"profit {cut_digits(coven_real_price - coven_price)}, #{coven['id']}"
            coven_durability = f"Wizards average durability {sum(durability[0]) / len(durability[0])}, wizards min durability {min(durability[0])}\n" \
                               f"Scepters average durability {sum(durability[1]) / len(durability[1])}, scepters min durability {min(durability[1])}"
            print(coven_info)
            print(coven_durability)
            print("--------------")


def get_coven_real_price(wizards_list, scepters_list, durability):
    wizards_price = get_coven_wizards_price(wizards_list)
    scepters_price = get_coven_scepters_price(scepters_list)
    coven_price = (wizards_price + scepters_price) * 0.9
    return coven_price


def get_coven_wizards_price(wizards_list):
    wizards_sum = 0
    for wizard in wizards_list:
        wizard_price = float(sell_prices[f"Level {wizard}"])
        wizards_sum += wizard_price
    return wizards_sum


def get_coven_scepters_price(scepters_list):
    scepters_sum = 0
    for scepter in scepters_list:
        rc_number = scepter // 10
        scepter_price = float(sell_prices[f"RC {rc_number}0-{rc_number}9"])
        scepters_sum += scepter_price
    return scepters_sum


if __name__ == "__main__":
    scepters_notice_list = []
    buy_prices, sell_prices, covens_rc_list = get_table_prices()
    print(buy_prices)
    print(sell_prices)
    covens_list = get_covens(covens_rc_list)
    # while True:
    #     start_time = datetime.now()
    #     loop = asyncio.get_event_loop()
    #     loop.run_until_complete(get_scepters(buy_prices))
    #     print(datetime.now() - start_time)
    #     time.sleep(1)
