import robin_stocks.robinhood as rh


# Get Portfolio Holdings
def get_portfolio():
    portfolio = rh.account.build_holdings()
    for stock, details in portfolio.items():
        print(f"Stock: {stock}")
        print(f"  Quantity: {details['quantity']}")
        print(f"  Equity: ${details['equity']}")
        print(f"  Average Buy Price: ${details['average_buy_price']}")
        print(f"  Percentage Change: {details['percentage']}\n")
    return portfolio

# Get Available Cash for Trading
def get_cash_available():
    profile = rh.account.load_account_profile()
    cash = profile.get('cash', '0')  # Check if 'cash' key exists
    buying_power = profile.get('buying_power', '0')
    print(f"Cash Available: ${cash}")
    print(f"Buying Power: ${buying_power}")
    return cash, buying_power
