import json

from watch import get_current_portfolio_value

def get_splits():
    with open("splits.json", "r") as data:
        return json.loads(data.read())

if __name__ == "__main__":
    total_balance = get_current_portfolio_value()
    splits = get_splits()
    budget = splits.get("budget", 0)
    paycheck = splits.get("paycheck", 0)

    total_capital = budget + paycheck
    increase_pct = (total_balance - total_capital) / total_capital
    print("Total portfolio value : {}".format(total_balance))
    print("Total balance increase: {}".format(increase_pct))
    print("Total budget balance  : {}".format(budget + (budget * increase_pct)))

