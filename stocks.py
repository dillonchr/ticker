import time
import datetime
import json
import requests
from pydash import get

from watch import get_shares
from cashout import get_portfolio_breakdown


def print_percentage(percentage):
    """ pretty print """
    percentage = round(percentage, 2)
    return "{} {}%".format("▲" if 0 < percentage else "▽", percentage)


def print_price(price):
    """ pretty print price """
    price = round(price, 2) if 1 < price else round(price, 6)
    return "${}".format(price)


def print_coin_data(coin):
    """ coin data for ticker """
    with requests.get("https://api.coingecko.com/api/v3/coins/{}?localization=false&tickers=true&market_data=true&community_data=false&developer_data=false&sparkline=false".format(coin)) as r:
        data = r.json()
        price = print_price(get(data, "market_data.current_price.usd"))
        symbol = get(data, "symbol", coin)
        print("[=]{}".format(symbol))
        pct24h = print_percentage(get(data, "market_data.price_change_percentage_24h", 0))
        pct1h = print_percentage(get(data, "market_data.price_change_percentage_1h_in_currency.usd", 0))
        print("{}|=|{}|=|{}".format(pct24h, price, pct1h))
        print("")



if "__main__" == __name__:
    print("24hr|=|{}|=|1hr".format(datetime.datetime.now().strftime("%m/%d/%y")))
    print("")
    for coin in get_shares().keys():
        if coin != "budget" and coin != "paycheck":
            print_coin_data(coin)
    print("")
    print("<=>portfolio")
    print("total|=|budget")
    portfolio = get_portfolio_breakdown()
    print("${}|=|{}%|=|${}".format(
        round(portfolio.get("value"), 2),
        round(portfolio.get("percent_change"), 2),
        round(portfolio.get("budget_value"), 2)
    ))
