import time
import datetime
import os
import json

import requests
from pydash import get

URL = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin%2Cethereum%2Cbitcoin&vs_currencies=usd"

def get_prices():
    with requests.get(URL) as r:
        return r.json()

last_update = ""

def should_buy():
    global last_update
    prices = get_prices()
    ltc = get(prices, "litecoin.usd", 0)
    btc = get(prices, "bitcoin.usd", 0)
    eth = get(prices, "ethereum.usd", 0)
    if 137 < ltc:
        trade_alarm()
    else:
        update = f"LTC ${ltc} ETH ${eth} BTC ${btc}"
        if last_update != update:
            last_update = update
            print(f"{update} {datetime.datetime.now()}")
            shares = get_shares()
            value = shares.get("eth", 0) * eth + shares.get("btc", 0) * btc + shares.get("ltc", 0) * ltc
            print(f"portfolio total: {value}")

def get_shares():
    with open("shares.json", "r") as share_data:
        data = share_data.read()
        return json.loads(data)

def trade_alarm():
    os.system(f"say \"do be trading my man\"")


while True:
    should_buy()
    time.sleep(30)
