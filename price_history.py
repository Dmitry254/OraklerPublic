import time

import requests
import json
import asyncio
import aiohttp

from datetime import datetime

from base_func import get_data, get_table_prices
from price_table import fill_table_wizards, fill_table_scepters
from keys import *


async def get_wizards(buy_prices):
    tasks = []
    async with aiohttp.ClientSession() as session:
        for level in buy_prices.keys():
            if "Level" in level:
                wizard_level = level[-1]
                url = f"https://backend.orakler.com/wizards?per_page=10&page=1&min_scepters={wizard_level}&max_scepters={wizard_level}&min_price=0&max_price=1000&property=all&sort=price"
                task = asyncio.create_task(get_wizards_data(session, url, level))
                tasks.append(task)
        await asyncio.wait(tasks)


async def get_wizards_data(session, url, level):
    global wizards_dict
    async with session.get(url) as resp:
        wizards_data = await resp.json()
        for wizard in wizards_data['data']:
            if int(wizard['durability']) > 35:
                if level in wizards_dict.keys():
                    wizards_dict[level].append(float(wizard['price']))
                else:
                    wizards_dict[level] = []
                    wizards_dict[level].append(float(wizard['price']))


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
    global scepters_dict
    async with session.get(url) as resp:
        scepters_data = await resp.json()
        for scepter in scepters_data['data']:
            if int(scepter['durability']) > 24:
                if interval in scepters_dict.keys():
                    scepters_dict[interval].append(float(scepter['price']))
                else:
                    scepters_dict[interval] = []
                    scepters_dict[interval].append(float(scepter['price']))


if __name__ == "__main__":
    scepters_dict = {}
    wizards_dict = {}
    buy_prices, sell_prices, covens_rc_list = get_table_prices()
    loop_sc = asyncio.get_event_loop()
    loop_sc.run_until_complete(get_scepters(buy_prices))
    loop_wz = asyncio.get_event_loop()
    loop_wz.run_until_complete(get_wizards(buy_prices))
    fill_table_wizards(wizards_dict)
    fill_table_scepters(scepters_dict)
