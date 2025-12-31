import yfinance as yf


def get_stock_details(ticker_symbol):
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

        print(f"--- {ticker_symbol.upper()} Stock Data ---")
        print(f"Yearly Target Price: {target_price}")
        print(f"Next Earnings Date: {earnings_date}")

    except Exception as e:
        print(f"Error fetching data for {ticker_symbol}: {e}")


# Example usage
ticker = input("Enter stock ticker: ")
get_stock_details(ticker)