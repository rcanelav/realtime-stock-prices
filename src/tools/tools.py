from datetime import datetime

import yfinance as yf

from src.models.models import EmptyInput


# ########################################################################
#                           Tool Definitions
# ########################################################################
def get_current_datetime(_: EmptyInput = None) -> str:
    """
    Returns the current date and time in a human-readable format.
    """
    now = datetime.now()
    return now.strftime("Today is %A, %B %d, %Y and the time is %H:%M:%S")


def retrieve_realtime_stock_price(ticker: str) -> str:
    """
    Retrieves the most recent stock price for a given ticker.
    """
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")
        if data.empty:
            return f"Could not find real-time price for {ticker}. The ticker may be invalid or delisted."
        price = data['Close'].iloc[-1]
        return f"The latest price for {ticker} is ${price:.2f}."
    except Exception as e:
        return f"An error occurred while fetching the price for {ticker}: {e}"


def retrieve_historical_stock_price(ticker: str, start_date: str, end_date: str) -> str:
    """
    Retrieves historical stock prices for a given ticker and date range.
    """
    try:
        data = yf.download(ticker, start=start_date, end=end_date)
        if data.empty:
            return f"No historical data found for {ticker} between {start_date} and {end_date}."
        data.reset_index(inplace=True)
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        return f"Historical data for {ticker}:\n{data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_string(index=False)}"
    except Exception as e:
        return f"An error occurred while fetching historical data for {ticker}: {e}"
