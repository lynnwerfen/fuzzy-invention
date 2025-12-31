import yfinance as yf
import sys
import pandas as pd
from datetime import datetime

def get_stock_details():
    TICKER_FILE = "tickers.txt"
    results = []

    print(f"Fetching data for tickers in {TICKER_FILE}...")
    try:
        with open(TICKER_FILE, 'r') as f:
            tickers = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {TICKER_FILE} not found.")
        sys.exit(1)

    for ticker_symbol in tickers:
        try:
            # Initialize the ticker object
            stock = yf.Ticker(ticker_symbol)

            # 1. Get Analyst Yearly Target Price
            # 'targetMeanPrice' is the consensus yearly target
            info = stock.info
            target_price = info.get('targetMeanPrice', 'N/A')

            # 2. Get Next Earnings Date
            # 'calendar' typically contains the next earnings date
            calendar = stock.calendar
            earnings_date = "N/A"

            if calendar is not None and 'Earnings Date' in calendar:
                # Usually returns a list of potential dates
                earnings_date = calendar['Earnings Date']

            #print(f"--- {ticker_symbol.upper()} Stock Data ---")
            #print(f"Yearly Target Price: {target_price}")
            #print(f"Next Earnings Date: {earnings_date}")

            results.append({
                'Ticker': ticker_symbol,
                'Next Earnings Date': earnings_date,
                'Mean Target Price': target_price
            })

        except Exception as e:
            print(f"Error fetching data for {ticker_symbol}: {e}")
            results.append({
                'Ticker': ticker_symbol,
                'Next Earnings Date': earnings_date,
                'Mean Target Price': target_price
            })

    # Create and display a Pandas DataFrame
    if results:
        df = pd.DataFrame(results)
        print("\n--- Stock Data Summary ---")
        print(df.to_markdown(index=False))


# Example usage
#ticker = input("Enter stock ticker: ")
get_stock_details()