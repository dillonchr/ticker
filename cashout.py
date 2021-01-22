import json

from watch import get_current_portfolio_value, get_shares

def get_splits():
    with open("splits.json", "r") as data:
        return json.loads(data.read())

if __name__ == "__main__":
    splits = get_shares()
    total_balance = get_current_portfolio_value(splits)
    print("Total portfolio value : {}".format(total_balance))

    budget = splits.get("budget", 0)
    paycheck = splits.get("paycheck", 0)

    total_capital = budget + paycheck
    increase_pct = (total_balance - total_capital) / total_capital
    print("Total balance increase: {}".format(increase_pct))
    print("Total budget balance  : {}".format(budget + (budget * increase_pct)))

