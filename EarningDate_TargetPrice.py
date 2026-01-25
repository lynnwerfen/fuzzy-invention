import yfinance as yf
import sys
import pandas as pd
from datetime import datetime

from flask import Flask
app = Flask(__name__)  # This MUST be outside any 'if' or function
#@app.route('/')

@app.route('/stock')
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
            current_price = info.get('currentPrice', 'N/A')
            market_cap_str = info.get('marketCap', 'N/A')
            if market_cap_str and isinstance(market_cap_str, (int, float)):
                market_cap_m = market_cap_str / 1_000_000
                market_cap = f"{market_cap_m:,.2f}M"
            else:
                market_cap = 'N/A'

            employee_num_str = info.get('fullTimeEmployees', 'N/A')
            if employee_num_str and isinstance(employee_num_str, (int, float)):
                employee_num = f"{employee_num_str:,}"
            else:
                employee_num = 'N/A'

            dividend_yield = info.get('dividendYield', 'N/A')
            exdividend_date_str = info.get('exDividendDate')
            if dividend_yield == 'N/A':
                exdividend_date = 'N/A'
            else:
                exdividend_date = datetime.fromtimestamp(exdividend_date_str).strftime('%Y-%m-%d')

            target_price = info.get('targetMeanPrice', 'N/A')

            # 2. Get Next Earnings Date
            # 'calendar' typically contains the next earnings date
            calendar = stock.calendar
            earnings_date = "N/A"

            if calendar is not None and 'Earnings Date' in calendar:
                # Usually returns a list of potential dates
                earnings_date = calendar['Earnings Date'][0].strftime('%Y-%m-%d')

            results.append({
                'Ticker': ticker_symbol,
                'Current Price': current_price,
                'Market Cap': market_cap,
                'Fulltime Employees': employee_num,
                'Dividend': dividend_yield,
                'Exdividend Date': exdividend_date,
                'Next Earnings Date': earnings_date,
                'Mean Target Price': target_price
            })

        except Exception as e:
            print(f"Error fetching data for {ticker_symbol}: {e}")
            results.append({
                'Ticker': ticker_symbol,
                'Current Price': current_price,
                'Market Cap': market_cap,
                'Fulltime Employees': employee_num,
                'Dividend': dividend_yield,
                'Exdividend Date': exdividend_date,
                'Next Earnings Date': earnings_date,
                'Mean Target Price': target_price
            })

    # Create and display a Pandas DataFrame
    if results:
        df = pd.DataFrame(results)
        
        #for command line - local testing
        #print("\n--- Stock Data Summary ---")
        #print(df.to_markdown(index=False))

        #for web app - deploy version
        markdown_table = df.to_markdown(index=False)
        return f"<pre>{markdown_table}</pre>"

# Example usage
#ticker = input("Enter stock ticker: ")
get_stock_details()