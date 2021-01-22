import time
import datetime
import os
import json

import requests
from pydash import get

def get_url(shares):
    """ fetch coingecko url for relevant coins """
    return "https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=" + "%2C".join(shares.keys())

def get_prices(shares):
    with requests.get(get_url(shares)) as r:
        return r.json()

last_update = ""

def should_buy():
    global last_update
    shares = get_shares()
    prices = get_prices(shares)

    total_value = 0.0
    update = ""

    for coin, value in prices.items():
        usd = get(value, "usd", 0)
        total_value += usd * shares.get(coin, 0)
        update += " $".join([coin, str(usd)]) + " -- "

    if last_update != update:
        last_update = update
        print("{}\n{}".format(datetime.datetime.now(), update))
        print("portfolio total: ${}".format(total_value))

last_shares_res = None

def get_shares():
    global last_shares_res

    if last_shares_res:
        return last_shares_res

    with requests.get(os.environ["SHARES_URL"]) as res:
        share_data = {}
        rows = res.text
        for row in rows.split("\r\n"):
            split = row.split("\t")
            if len(split) > 1:
                share_data[split[0]] = float(split[1])

        last_shares_res = share_data
        return share_data

def get_current_portfolio_value(shares):
    if not shares:
        shares = get_shares()
    prices = get_prices(shares)
    total_value = 0.0

    for coin, value in prices.items():
        usd = get(value, "usd", 0)
        total_value += usd * shares.get(coin, 0)
    return total_value

def trade_alarm(update):
    #os.system(f"say \"do be trading my man\"")
    with open(".discord", "r") as config:
        webhook_url = config.read().strip()
        with requests.post(webhook_url, json={"content": "You should trade! {}".format(update)}, headers={"Content-Type": "application/json"}) as r:
            if not r.ok:
                print("{}".format(r.text))

if __name__ == "__main__":
    while True:
        should_buy()
        time.sleep(30)
