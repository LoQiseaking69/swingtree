import time
from typing import List, Union
from coinbase.wallet.client import Client
from .core import SwingTreeAPI
from .exceptions import InvalidOperationError, DataIntegrityError


class CoinbaseTradingBot:
    """
    A trading bot that integrates Coinbase API with SwingTree for dynamic high-low trend tracking.
    """

    def __init__(self, api_key: str, api_secret: str, trading_pair: str = "BTC-USD", mode: str = "min"):
        if not api_key or not api_secret:
            raise ValueError("API key and secret are required.")
        
        self.client = Client(api_key, api_secret)
        self.trading_pair = trading_pair
        self.tree_api = None
        self.price_history: List[float] = []
        self.mode = mode

    def fetch_latest_price(self) -> float:
        """
        Fetch the latest price of the trading pair.

        :return: Latest price as a float
        """
        try:
            spot_price = self.client.get_spot_price(currency_pair=self.trading_pair)
            return float(spot_price["amount"])
        except Exception as e:
            raise DataIntegrityError(f"Failed to fetch price data: {e}")

    def update_price_history(self, max_length: int = 100):
        """
        Update the local price history by fetching the latest price.

        :param max_length: Maximum number of prices to store in history
        """
        price = self.fetch_latest_price()
        self.price_history.append(price)
        if len(self.price_history) > max_length:
            self.price_history.pop(0)  # Maintain max length
        if not self.tree_api:
            self.tree_api = SwingTreeAPI(self.price_history, mode=self.mode)
        else:
            self.tree_api.update_value(len(self.price_history) - 1, price)

    def get_trend_snapshot(self) -> Union[int, float]:
        """
        Get a snapshot of the current trend using the aggregation function.

        :return: Current trend value
        """
        if not self.tree_api:
            raise InvalidOperationError("SwingTreeAPI is not initialized.")
        return self.tree_api.range_query(0, len(self.price_history) - 1)

    def execute_trading_logic(self):
        """
        Basic trading logic based on price trends.
        """
        trend_value = self.get_trend_snapshot()
        current_price = self.price_history[-1]

        if current_price < trend_value * 0.95:  # Example condition for buying
            print(f"Buying opportunity detected at {current_price} (trend: {trend_value})")
            # Execute buy order logic here
        elif current_price > trend_value * 1.05:  # Example condition for selling
            print(f"Selling opportunity detected at {current_price} (trend: {trend_value})")
            # Execute sell order logic here

    def run_bot(self, interval: int = 60):
        """
        Run the trading bot with periodic updates.

        :param interval: Time interval in seconds between price checks
        """
        try:
            while True:
                self.update_price_history()
                self.execute_trading_logic()
                time.sleep(interval)
        except KeyboardInterrupt:
            print("Bot stopped by user.")
        except Exception as e:
            print(f"Error: {e}")