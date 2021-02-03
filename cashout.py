import json

from watch import get_current_portfolio_value, get_shares

def get_splits():
    with open("splits.json", "r") as data:
        return json.loads(data.read())

def get_portfolio_breakdown():
    splits = get_shares()
    total_balance = get_current_portfolio_value(splits)
    budget = splits.get("budget", 0)
    paycheck = splits.get("paycheck", 0)
    total_capital = budget + paycheck
    increase_pct = (total_balance - total_capital) / total_capital
    return {
        "value": total_balance,
        "percent_change": increase_pct * 100,
        "budget_value": budget + (budget * increase_pct)
    }

if __name__ == "__main__":
    portfolio = get_portfolio_breakdown()
    total = round(portfolio.get("value"))
    pct = round(portfolio.get("percent_change"), 2)
    budget = round(portfolio.get("budget_value"))
    print("{} / {}% / {}".format(total, pct, budget))

