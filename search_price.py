import time

import requests
import json
import asyncio
import aiohttp

from datetime import datetime

from base_func import get_data, get_table_prices
from google_sheets import get_google_sheet_data
from tg_bot import send_text_message, message
from keys import *


async def get_scepters(buy_prices):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for interval in buy_prices.keys():
            if "RC" in interval:
                rc_interval = interval[3:].split("-")
                min_rc = rc_interval[0]
                max_rc = rc_interval[1]
                url = f"https://backend.orakler.com/scepters?per_page=10&page=1&min_price=0&max_price=1000&min_rc={min_rc}&max_rc={max_rc}&property=all&sort=price"
                task = asyncio.create_task(get_scepters_data(session, url, interval))
                tasks.append(task)
        await asyncio.wait(tasks)


async def get_scepters_data(session, url, interval):
    global scepters_notice_list
    async with session.get(url) as resp:
        scepters_data = await resp.json()
        for scepter in scepters_data['data']:
            if float(scepter['price']) < buy_prices[interval]:
                notice = [int(scepter['price']), scepter['id']]
                if notice not in scepters_notice_list:
                    scepters_notice_list.append(notice)
                    print(scepters_notice_list)
                    text = f"Scepter {scepter['researchCapacity']} RC, price {scepter['price']} ORKL, {scepter['durability']} days, #{scepter['id']}"
                    send_text_message(message, text)
                    print(text)
                    print(url)


if __name__ == "__main__":
    scepters_notice_list = []
    buy_prices, sell_prices, covens_rc_list = get_table_prices()
    print(buy_prices)
    print(sell_prices)
    while True:
        start_time = datetime.now()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(get_scepters(buy_prices))
        print(datetime.now() - start_time)
        time.sleep(1)
