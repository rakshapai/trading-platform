import robin_stocks.robinhood as rh
import login 
import pandas as pd
from helpers import get_quote_percent_change, build_temp_table  

login.login()

# List of valid sectors
VALID_SECTORS = [
    "Communication Services",
    "Consumer Discretionary",
    "Consumer Durables",
    "Consumer Staples",
    "Energy",
    "Financials",
    "Health Care",
    "Industrials",
    "Information Technology",
    "Materials",
    "Real Estate",
    "Utilities"
]

def get_top_movers_by_sector(sector="Information Technology", info=None):
    """
    Returns the Top 10 market movers filtered by sector.
    
    :param sector: The industry sector to filter by.
                   Valid sectors are: 
                   "Communication Services", "Consumer Discretionary", "Consumer Staples",
                   "Energy", "Financials", "Health Care", "Industrials", "Information Technology",
                   "Materials", "Real Estate", "Utilities"
    :param info: (Optional) Specific stock data to return.
    :returns: List of top movers in the specified sector.
    """
    # Validate that the requested sector is in our valid sectors list.
    if sector not in VALID_SECTORS:
        print(f"Sector '{sector}' is not recognized. Please choose from: {', '.join(VALID_SECTORS)}")
        return []
    
    # Step 1: Get the top 20 movers
    top_movers = rh.markets.get_top_movers()
    if not top_movers:
        print("No market movers found.")
        return []
    
    # Step 2: Get stock symbols from movers
    symbols = [stock["symbol"] for stock in top_movers]
    
    # Step 3: Fetch fundamentals (including sector) for each stock
    stock_fundamentals = rh.stocks.get_fundamentals(symbols)

    # print (stock_fundamentals[:1])

    
    # Step 4: Filter stocks belonging to the requested sector and compute percent change using the helper function
    sector_movers = []
    for stock in stock_fundamentals:
        stock_sector = stock.get("sector", "")
        if any(word in stock_sector.lower() for word in sector.lower().split()):
            symbol = stock.get("symbol")
            # Get the percent change from the helper function
            price_change = get_quote_percent_change(symbol)
            if price_change is not None:
                sector_movers.append({
                    "symbol": symbol,
                    "percent_change": price_change,
                    "sector": stock_sector
                })
    
    # Step 5: Sort movers by the absolute value of price change (highest first) and return the top 10
    sector_movers = sorted(sector_movers, key=lambda x: abs(float(x["percent_change"])), reverse=True)
    
    return sector_movers[:10]
