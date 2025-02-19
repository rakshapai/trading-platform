import robin_stocks.robinhood as rh
import pandas as pd

def compute_percent_change(open_price, close_price):
    """
    Computes the percent change between open and close prices.
    
    :param open_price: The opening price.
    :param close_price: The closing price.
    :returns: Percent change as a float, or None if open_price is zero or an error occurs.
    """
    try:
        open_price = float(open_price)
        close_price = float(close_price)
        if open_price == 0:
            return None
        return ((close_price - open_price) / open_price) * 100
    except Exception as e:
        print(f"Error computing percent change: {e}")
        return None

def get_stock_info(symbol):
    """
    Fetches real-time stock information.
    
    :param symbol: Stock ticker symbol.
    :returns: Stock quote information from Robinhood.
    """
    return rh.stocks.get_stock_quote_by_symbol(symbol)

def format_stock_stats(stock_stat):
    """
    Converts a stock stat such as market cap, volume number into a human-readable string in millions (M),
    billions (B), or trillions (T), rounded to two decimal places.

    :param market_cap: The market cap value as a number (or a string that can be converted).
    :returns: A string representing the market cap in M, B, or T.
    """
    try:
        cap = float(stock_stat)
    except (ValueError, TypeError):
        return "N/A"
    
    if cap >= 1e12:
        return f"{cap / 1e12:.2f}T"
    elif cap >= 1e9:
        return f"{cap / 1e9:.2f}B"
    elif cap >= 1e6:
        return f"{cap / 1e6:.2f}M"
    else:
        return f"{cap:.2f}"
    

def get_company_details(ticker):
    """
    Retrieves company details (company name, headquarters, and company size)
    from the stock fundamentals data for a given ticker.
    
    :param ticker: Stock ticker symbol (e.g., "AAPL").
    :returns: A dictionary with keys "company_name", "headquarters", and "company_size",
              or None if fundamentals data is not available.
    """
    fundamentals = rh.stocks.get_fundamentals(ticker)
    instruments = rh.stocks.get_instruments_by_symbols(ticker)
    if fundamentals and len(fundamentals) > 0:
        fundamental = fundamentals[0]
        instrument = instruments[0]
        company_name = instrument.get("simple_name", "N/A")
        headquarters = fundamental.get("headquarters_state", "N/A")
        stock_price = get_stock_info(ticker).get("last_trade_price", "N/A")
        market_cap = fundamental.get("market_cap", "N/A")
        pe_ratio = fundamental.get("pe_ratio", "N/A")
        average_volume = fundamental.get("average_volume", "N/A")
        
        return {
            "company_name": company_name,
            "headquarters": headquarters,
            "stock_price": stock_price,
            "market_cap": format_stock_stats(market_cap),
            "average_volume": format_stock_stats(average_volume),
            "pe_ratio": pe_ratio
        }
    return None


def classify_risk(stock_volatility):
    """
    Classify stocks based on volatility.
    (Example: Low if volatility < 2%, Medium if 2-5%, High if >5%)
    
    :param stock_volatility: Volatility percentage.
    :returns: A string representing the risk classification.
    """
    if stock_volatility < 2:
        return "Low"
    elif 2 <= stock_volatility <= 5:
        return "Medium"
    else:
        return "High"

def get_quote_percent_change(ticker):
    """
    Retrieves real-time quote data for a ticker and computes the percent change
    between the last trade price and the previous close.
    
    :param ticker: Stock ticker symbol (e.g., "AAPL")
    :returns: Percent change as a float, or None if data is missing.
    """
    quote_data = rh.get_quotes(ticker)
    if quote_data:
        quote = quote_data[0]
        return compute_percent_change(quote.get('previous_close', 0),
                                      quote.get('last_trade_price', 0))
    return None

def get_percent_change(ticker, interval, span):
    """
    Retrieves historical data for a ticker and computes the percent change
    between the first open price and the last close price in the returned data.
    
    :param ticker: Stock ticker symbol.
    :param interval: Data interval (e.g., "5minute", "hour", "day").
    :param span: Data span (e.g., "day", "week", "month", "year").
    :returns: Percent change as a float, or None if data is missing.
    """
    historicals = rh.stocks.get_stock_historicals(
        ticker, interval=interval, span=span, bounds='regular'
    )
    if not historicals or len(historicals) == 0:
        return None
    return compute_percent_change(historicals[0]['open_price'],
                                  historicals[-1]['close_price'])

def build_temp_table(tickers):
    """
    Builds a temporary table (as a Pandas DataFrame) with percent changes for day, week,
    month, and year for each ticker. The stock name (ticker) is placed in the rightmost column.
    
    :param tickers: List of stock ticker symbols.
    :returns: Pandas DataFrame with percent changes and the corresponding stock symbol.
    """
    temp_data = []
    for ticker in tickers:
        day_change   = get_percent_change(ticker, interval="5minute", span="day")
        week_change  = get_percent_change(ticker, interval="10minute", span="week")
        month_change = get_percent_change(ticker, interval="hour", span="month")
        year_change  = get_percent_change(ticker, interval="day", span="year")
        
        temp_data.append({
             "stock": ticker,
            "day_change_perc": day_change,
            "week_change_perc": week_change,
            "month_change_perc": month_change,
            "year_change_perc": year_change
           
        })
    
    df = pd.DataFrame(temp_data, columns=[
        "stock","day_change_perc", "week_change_perc", "month_change_perc", "year_change_perc"
    ])
    
    company_df = pd.DataFrame([{**get_company_details(ticker), "stock": ticker} for ticker in df['stock']])

    merged_table = df.merge(company_df, on="stock", how="left")

    return merged_table

