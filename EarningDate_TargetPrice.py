import yfinance as yf
import sys
from datetime import datetime
from tabulate import tabulate
import tkinter as tk
import webbrowser
import os
from waitress import serve

from flask import Flask
app = Flask(__name__)  # This MUST be outside any 'if' or function

## local testing
#@app.route("/")  # Define the root route
#def home():
#    return "Flask is working!"  # Text shown on the root page

@app.route('/stock')
def get_stock_details():

    ## Create button inside this method
    #def open_text_file():
        ##local testing
        #filepath = os.path.abspath("C:/Users/hou_1/PycharmProjects/PythonProject2/tickers.txt")

    #    filepath = os.path.abspath("/home/lynnw/fuzzy-invention/tickers.txt")
    #    webbrowser.open(f"file://{filepath}")

    #root = tk.Tk()

    #button = tk.Button(root, text="Open Text File", command=open_text_file)
    #button.pack(pady=10)

    #root.title("Tickers")
    #root.mainloop()

    global fifty_day_average, market_cap, employee_num, dividend_yield, ex_dividend_date, earnings_date, current_price, target_price, trailing_pe, forward_pe, eps_growth, peg_ratio, two_hundred_day_average

    ticker_file = "tickers.txt"
    results = []

    print(f"Fetching data for tickers in {ticker_file}...")
    try:
        with open(ticker_file, 'r') as f:
            tickers = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Error: {ticker_file} not found.")
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
                market_cap_b = market_cap_str / 1_000_000_000
                market_cap = f"{market_cap_b:,.2f}B"
            else:
                market_cap = 'N/A'

            employee_num_str = info.get('fullTimeEmployees', 'N/A')
            if employee_num_str and isinstance(employee_num_str, (int, float)):
                employee_num = f"{employee_num_str:,}"
            else:
                employee_num = 'N/A'

            dividend_yield = info.get('dividendYield', 'N/A')
            ex_dividend_date_str = info.get('exDividendDate')
            if dividend_yield == 'N/A':
                ex_dividend_date = 'N/A'
            else:
                ex_dividend_date = datetime.fromtimestamp(ex_dividend_date_str).strftime('%Y-%m-%d')

            target_price = info.get('targetMeanPrice', 'N/A')

            # 2. Get Next Earnings Date
            # 'calendar' typically contains the next earnings date
            calendar = stock.calendar
            earnings_date = "N/A"
            if calendar is not None and 'Earnings Date' in calendar:
                # Usually returns a list of potential dates
                earnings_date = calendar['Earnings Date'][0].strftime('%Y-%m-%d')

            trailing_pe = info.get('trailingPE', 'N/A')
            forward_pe = info.get('forwardPE', 'N/A')
            eps_growth = info.get('earningsGrowth', 'N/A')
            peg_ratio = info.get('pegRatio', 'N/A')
            fifty_day_average = info.get('fiftyDayAverage', 'N/A')
            two_hundred_day_average = info.get('twoHundredDayAverage', 'N/A')

            results.append({
                'Ticker': ticker_symbol,
                'Market Cap (>5B)': market_cap,
                'Employees': employee_num,
                'Dividend': dividend_yield,
                'Ex-dividend Date': ex_dividend_date,
                'Next Earnings Date': earnings_date,
                'Current Price': current_price,
                'Mean Target Price': target_price,
                'Trailing PE (<25)': trailing_pe,
                'Forward PE (< 15)': forward_pe,
                'EPS Growth (> 15)': eps_growth,
                'PEG Ratio (< 2)': peg_ratio,
                '50 MA': fifty_day_average,
                '200 MA': two_hundred_day_average
            })

        except Exception as e:
            print(f"Error fetching data for {ticker_symbol}: {e}")
            results.append({
                'Ticker': ticker_symbol,
                'Market Cap': market_cap,
                'Employees': employee_num,
                'Dividend': dividend_yield,
                'Ex-dividend Date': ex_dividend_date,
                'Next Earnings Date': earnings_date,
                'Current Price': current_price,
                'Mean Target Price': target_price,
                'Trailing PE (<25)': trailing_pe,
                'Forward PE (< 15)': forward_pe,
                'EPS Growth (> 15)': eps_growth,
                'PEG Ratio (< 2)': peg_ratio,
                '50 MA': fifty_day_average,
                '200 MA (< 15)': two_hundred_day_average
            })

    # Create and display a Pandas DataFrame
    if results:
        ##for command line - local testing
        #df = pd.DataFrame(results)
        #print("\n--- Stock Data Summary ---")
        ##print(df.to_markdown(index=False))
        #print(tabulate(df, headers='keys', tablefmt='fancy_grid', stralign='right', showindex=False))  # 'psql' includes full row borders

        # for web app - deploy version
        markdown_table = tabulate(results, headers='keys', tablefmt='fancy_grid', stralign='right', showindex=False)
        return f"<pre>{markdown_table}</pre>"

if __name__ == "__main__":
    # Enable debug
    #app.run(debug=True)

    # To avoid seeing development server vs production WSGI server
    serve(app, host='127.0.0.1', port=5000)

get_stock_details()