import time
import datetime
import os

import requests
from pydash import get

URL = "https://api.coingecko.com/api/v3/simple/price?ids=litecoin%2Cethereum%2Cripple&vs_currencies=usd"

def get_prices():
    with requests.get(URL) as r:
        return r.json()

last_update = ""

def should_buy():
    global last_update
    prices = get_prices()
    ltc = get(prices, "litecoin.usd", 0)
    ripple = get(prices, "ripple.usd", 0)
    eth = get(prices, "ethereum.usd", 0)
    if 0.39 < ripple and eth < 621:
        say_update("Oh my god. You have to trade now!")
        print("YOU SHOULD BUY NOW")
    else:
        update = f"LTC ${ltc} ETH ${eth} XRP ${ripple}"
        if last_update != update:
            last_update = update
            print(f"{update} {datetime.datetime.now()}")

def say_update(update):
    os.system(f"say \"{update}\"")


while True:
    should_buy()
    time.sleep(30)
