import login
import portfolio
import top_movers
import helpers
import q_learning

# === Step 1: Login ===
login.login()
print("Login Successfully!!! \n Test Stock: AAPL")
login.QUOTE('aapl')

# === Step 2: Fetch Portfolio and Available Cash ===
print ("\n=== Portfolio Holdings ===")
# portfolio_holdings = portfolio.get_portfolio()
cash_available, buying_power = portfolio.get_cash_available()
trade_budget = float(cash_available) * 0.2  # Allocate 20% of available cash

print(f"Total Cash Available: ${cash_available}")
print(f"Trade Budget (20% allocation): ${trade_budget}")

# === Step 3: Get Top Movers in an Industry ===
industry = "Consumer Durables"  # Change to 'consumer', 'industry', 'sp500'
top_movers = top_movers.get_top_movers_by_sector(industry)
print("\nTop 10 Movers in", industry)
for stock in top_movers:
    print(f"{stock['symbol']}: {stock['percent_change']}% change")

# Extract tickers from the top movers and build the temporary table with additional intervals
tickers = [stock['symbol'] for stock in top_movers]
temp_table = helpers.build_temp_table(tickers)

print("\nTemporary Table with Daily, Weekly, Monthly, and Yearly Percent Changes:")
print(temp_table)

# === Step 4: Classify Stocks by Risk ===
risk_tolerance = "High"  # Set as Low, Medium, or High
classified_stocks = []
for stock in top_movers:
    volatility = abs(float(stock["percent_change"]))
    risk = helpers.classify_risk(volatility)
    classified_stocks.append({"symbol": stock["symbol"], "risk": risk, "volatility": volatility})

# === Step 5: Filter Stocks Based on Risk Tolerance ===
filtered_stocks = [s for s in classified_stocks if s["risk"] == risk_tolerance]
if not filtered_stocks:
    print(f"No stocks found under {risk_tolerance} risk tolerance. Consider adjusting your threshold.")
    exit()

# === Step 6: Use Q-Learning to Choose Stocks to Buy ===

# Q-Learning Parameters
q_learning.alpha = 0.1
q_learning.gamma = 0.6
q_learning.epsilon = 0.1
best_stock, invest_amount = q_learning.q_learning_stock_selection(filtered_stocks, int(trade_budget))

print(f"\nRecommended Stock to Buy: {best_stock['symbol']}")
print(f"Investment Amount: ${invest_amount}")

# === Step 7: Execute Trade ===
quantity = invest_amount // float(helpers.get_stock_info(best_stock["symbol"])["last_trade_price"])
print(f"Buying {quantity} shares of {best_stock['symbol']}")




