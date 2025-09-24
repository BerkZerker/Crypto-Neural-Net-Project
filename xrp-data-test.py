# This script fetches the last 3 months of XRP market data from CoinGecko,
# analyzes it to find the highest and lowest prices, and then uses CCXT
# to get the current price from an exchange.

import ccxt
import pandas as pd
from pycoingecko import CoinGeckoAPI
from datetime import datetime, timedelta

def get_xrp_market_data():
    """
    Fetches and analyzes XRP market data for the last 90 days.
    """
    try:
        # 1. Initialize the CoinGecko API client
        cg = CoinGeckoAPI()

        # 2. Define the date range (last 90 days)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=90)

        # Convert dates to unix timestamps as required by the API
        from_timestamp = int(start_date.timestamp())
        to_timestamp = int(end_date.timestamp())

        print("Fetching 90 days of historical data for XRP from CoinGecko...")
        # 3. Fetch the historical market data
        historical_data = cg.get_coin_market_chart_range_by_id(
            id='ripple',
            vs_currency='usd',
            from_timestamp=from_timestamp,
            to_timestamp=to_timestamp
        )
        
        print("Data fetched successfully.")

        # 4. Process the data using pandas
        # Extract the prices list and load it into a DataFrame
        prices = historical_data['prices']
        df = pd.DataFrame(prices, columns=['timestamp', 'price'])

        # Convert timestamp to a readable datetime format
        df['date'] = pd.to_datetime(df['timestamp'], unit='ms')

        if df.empty:
            print("No data returned from CoinGecko.")
            return

        # 5. Find the highest and lowest prices
        highest_price_row = df.loc[df['price'].idxmax()]
        lowest_price_row = df.loc[df['price'].idxmin()]

        # 6. Print the results
        print("\n--- XRP Price Analysis (Last 90 Days) ---")
        print(f"Highest Price: ${highest_price_row['price']:.4f} on {highest_price_row['date'].strftime('%Y-%m-%d')}")
        print(f"Lowest Price:  ${lowest_price_row['price']:.4f} on {lowest_price_row['date'].strftime('%Y-%m-%d')}")
        print("------------------------------------------")

    except Exception as e:
        print(f"An error occurred while fetching from CoinGecko: {e}")


# Note that binance is not accessable for users in the USA
# def get_current_xrp_price():
#     """
#     Fetches the current XRP price from Binance using CCXT.
#     """
#     try:
#         # Initialize the CCXT exchange client (e.g., Binance)
#         exchange = ccxt.binance()
        
#         # Fetch the ticker for XRP/USDT
#         print("\nFetching current price from Binance...")
#         ticker = exchange.fetch_ticker('XRP/USDT')
#         current_price = ticker['last']
        
#         print(f"Current XRP/USDT Price on {exchange.id}: ${current_price:.4f}")

#     except ccxt.NetworkError as e:
#         print(f"Network error while fetching from {exchange.id}: {e}")
#     except ccxt.ExchangeError as e:
#         print(f"Exchange error while fetching from {exchange.id}: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred with CCXT: {e}")


if __name__ == "__main__":
    get_xrp_market_data()
