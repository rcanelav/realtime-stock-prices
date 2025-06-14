from datetime import datetime
from typing import Optional

import yfinance as yf

from src.models.models import EmptyInput


# ########################################################################
#                           Tool Definitions
# ########################################################################
def get_current_datetime(_: Optional[EmptyInput] = None) -> str:
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
        if not isinstance(ticker, str) or not ticker.strip():
            return "Invalid input: ticker must be a non-empty string."

        ticker = ticker.strip().upper()
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d", interval="1m")

        if data is None or data.empty:
            return f"No real-time data found for ticker '{ticker}'. It may be invalid or delisted."

        if 'Close' not in data.columns or data['Close'].isna().all():
            return f"Price data for '{ticker}' is unavailable or incomplete."

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
        if data is None or data.empty:
            return f"No historical data found for {ticker} between {start_date} and {end_date}."

        data.reset_index(inplace=True)

        if 'Date' in data.columns:
            data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')

        # Relevant columns for output
        output_table = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']].to_string(index=False)

        return f"Historical data for {ticker}:\n{output_table}"
    except Exception as e:
        return f"An error occurred while fetching historical data for {ticker}: {e}"
