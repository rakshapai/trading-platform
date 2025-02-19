import pandas as pd
import yfinance as yf
import numpy as np
from datetime import datetime


class StockListDownloader:
    """
    Downloads and combines stock lists from NASDAQ Trader for NASDAQ‐listed stocks
    and NYSE-listed stocks (from the 'otherlisted' file).
    """

    NASDAQ_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
    OTHER_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"

    def __init__(self):
        self.nasdaq_df = None
        self.nyse_df = None
        self.combined_df = None

    def download_nasdaq_listed(self):
        """Download NASDAQ-listed stocks and add Platform column."""
        nasdaq = pd.read_csv(self.NASDAQ_URL, sep='|')
        # Remove file metadata row.
        nasdaq = nasdaq[nasdaq['Symbol'] != "File Creation Time"]
        nasdaq.rename(columns={"Symbol": "Ticker"}, inplace=True)
        nasdaq['Platform'] = 'NASDAQ'
        self.nasdaq_df = nasdaq[['Ticker', 'Platform']]
        return self.nasdaq_df

    def download_nyse_listed(self):
        """Download other listed stocks, filter for NYSE and add Platform column."""
        other = pd.read_csv(self.OTHER_URL, sep='|')
        # Filter out test issues.
        other = other[other['Test Issue'] != 'Y']
        # Filter for NYSE stocks. In this file, Exchange 'N' represents NYSE.
        nyse = other[other['Exchange'] == 'N'].copy()
        nyse.rename(columns={"ACT Symbol": "Ticker"}, inplace=True)
        nyse['Platform'] = 'NYSE'
        self.nyse_df = nyse[['Ticker', 'Platform']]
        return self.nyse_df

    def combine_and_save_csv(self, output_file="nasdaq_nyse_listed_stocks.csv"):
        """
        Combine NASDAQ and NYSE stocks, remove duplicates, and write to a CSV file.
        Returns the combined DataFrame.
        """
        if self.nasdaq_df is None:
            self.download_nasdaq_listed()
        if self.nyse_df is None:
            self.download_nyse_listed()
        self.combined_df = pd.concat([self.nasdaq_df, self.nyse_df], ignore_index=True)
        self.combined_df.drop_duplicates(subset=['Ticker'], inplace=True)
        self.combined_df.to_csv(output_file, index=False)
        print(f"CSV file '{output_file}' written with {len(self.combined_df)} stocks.")
        return self.combined_df


class StockStatsFetcher:
    """
    Uses yfinance to fetch key statistics and historical performance for a given ticker.
    """

    def __init__(self):
        pass

    def get_stock_stats(self, ticker):
        """
        Fetch key statistics and performance metrics for a given ticker.
        Returns a dictionary with:
          - Ticker, Name, Company, Market Cap, PE Ratio, Dividend Yield,
            Average Volume, Closing Price, Industry, Sector,
            Year Growth (%), and Month Growth (%).
        """
        tkr = yf.Ticker(ticker)
        info = tkr.info

        # Calculate year and month growth based on historical closing prices.
        try:
            hist_year = tkr.history(period="1y")
            year_growth = ((hist_year['Close'].iloc[-1] - hist_year['Close'].iloc[0]) /
                           hist_year['Close'].iloc[0]) * 100
        except Exception as e:
            year_growth = np.nan

        try:
            hist_month = tkr.history(period="1mo")
            month_growth = ((hist_month['Close'].iloc[-1] - hist_month['Close'].iloc[0]) /
                            hist_month['Close'].iloc[0]) * 100
        except Exception as e:
            month_growth = np.nan

        return {
            'Ticker': ticker,
            'Name': info.get('longName', 'N/A'),
            'Company': info.get('shortName', 'N/A'),
            'Market Cap': info.get('marketCap', np.nan),
            'PE Ratio': info.get('trailingPE', np.nan),
            'Dividend Yield': info.get('dividendYield', np.nan),
            'Average Volume': info.get('averageVolume', np.nan),
            'Closing Price': info.get('previousClose', np.nan),
            'Industry': info.get('industry', 'N/A'),
            'Sector': info.get('sector', 'N/A'),
            'Year Growth (%)': round(year_growth, 2) if not np.isnan(year_growth) else np.nan,
            'Month Growth (%)': round(month_growth, 2) if not np.isnan(month_growth) else np.nan,
            'Date': datetime.now().strftime("%Y-%m-%d")
        }

    def get_stats_for_tickers(self, tickers):
        """
        Retrieves statistics for a list of tickers.
        Returns a DataFrame containing the stats.
        """
        stats_list = []
        for ticker in tickers:
            # print(f"Processing {ticker}...")
            try:
                stats = self.get_stock_stats(ticker)
                stats_list.append(stats)
            except Exception as e:
                print(f"Error processing {ticker}: {e}")
        return pd.DataFrame(stats_list)


class StockAnalyzer:
    """
    Main class that combines the stock list downloader and stats fetcher
    to analyze and output stock data.
    """

    def __init__(self, output_csv="nasdaq_nyse_listed_stocks.csv"):
        self.downloader = StockListDownloader()
        self.stats_fetcher = StockStatsFetcher()
        self.output_csv = output_csv

    def run(self):
        """
        Downloads the stock list, fetches key stats for each stock,
        and writes the results to a CSV file.
        """
        # Step 1: Download combined stock list.
        stock_list_df = self.downloader.combine_and_save_csv(self.output_csv)
        tickers = stock_list_df['Ticker'].tolist()
        
        # For demonstration, you might want to limit to a subset of tickers.
        # Remove or modify the following line as needed.
        # tickers = tickers[:50]  # For example, process first 50 tickers only.

        # Step 2: Fetch stock statistics.
        stats_df = self.stats_fetcher.get_stats_for_tickers(tickers)

        # Optionally merge Platform info from the stock list.
        merged_df = pd.merge(stats_df, stock_list_df, on="Ticker", how="left")

        # Write the detailed stats to a CSV file.
        stats_output = "stock_stats.csv"
        merged_df.to_csv(stats_output, index=False)
        print(f"Stock statistics written to {stats_output}.")
        return merged_df


if __name__ == "__main__":
    analyzer = StockAnalyzer()
    final_stats_df = analyzer.run()
    # For display purposes, print the first few rows.
    print(final_stats_df.head())
