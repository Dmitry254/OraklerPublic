import time
import traceback

import requests
import json
from datetime import datetime
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_abi import decode_abi
from eth_utils import decode_hex

from base_func import get_data, get_data_no_timeout
from keys import *


def set_http_web3():
    web3 = Web3(Web3.HTTPProvider(bsc))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3


def set_wss_web3():
    web3 = Web3(Web3.WebsocketProvider(bsc_wss, websocket_timeout=360, websocket_kwargs={"max_size": 650000000}))
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return web3


def get_contract(w3, contract_address):
    abi_endpoint = f"https://api.bscscan.com/api?module=contract&action=getabi&address={contract_address}&apikey={bsc_scan_api}"
    abi = json.loads(requests.get(abi_endpoint).text)
    print(abi)
    contract = w3.eth.contract(contract_address, abi=abi["result"])
    return contract


def get_transaction_data(w3, contract, transaction_hash):
    transaction = w3.eth.getTransaction(transaction_hash)
    func_obj, func_params = contract.decode_function_input(transaction["input"])
    return func_obj, func_params


def send_accept_tx(web3, nft_id, nft_price, gas_price):
    if web3.eth.gas_price > 10000000000:
        text = "Слишком высокая цена газа"
        return text
    try:
        nft_id = hex(int(nft_id))[2:]
        nft_id = f"{(64 - len(nft_id)) * '0'}{nft_id}"
        nft_price = hex(nft_price * price_coeff)[2:]
        price = f"{(64 - len(nft_price)) * '0'}{nft_price}"
        data = f"0x598647f8{nft_id}{price}"
        tx_data = {'to': contract_address, 'from': my_address, 'data': data,
                   'gas': 500000, 'gasPrice': gas_price + 5500000000, 'nonce': web3.eth.get_transaction_count(my_address)}
        sign_tx = web3.eth.account.sign_transaction(tx_data, private_key=private_key)
        web3.eth.send_raw_transaction(sign_tx.rawTransaction)
        text = "Транзакция успешно отправлена"
        return text
    except:
        error = traceback.format_exc()
        return error
