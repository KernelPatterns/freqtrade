from freqtrade.exchange.interface import IExchange

import logging
 
import requests

from freqtrade.exchange.interface import IExchange


logger = logging.getLogger(__name__)


class Indodax(IExchange):
    """
    Custom implementation for the Indodax exchange.
    """

    BASE_URL = "https://indodax.com/tapi"

    def __init__(self, config: dict) -> None:
        super().__init__(config)
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self._timeframes = {
            "1m": "1",
            "15m": "15",
            "30m": "30",
            "1h": "60",
            "4h": "240",
            "1d": "1D",
        }

    @property
    def timeframes(self):
        return self._timeframes

    def _request(self, endpoint, params=None):
        """Helper function to make API requests."""
        url = f"{self.BASE_URL}/{endpoint}"
        logger.debug(f"Requesting {url} with params {params}")
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def fetch_tickers(self):
        """
        Fetch all tickers from the exchange.
        """
        data = self._request("ticker_all")
        tickers = {}
        for pair, ticker in data["tickers"].items():
             tickers[pair] = {
                "symbol": pair,
                "last": float(ticker["last"]),
                "high": float(ticker["high"]),
                "low": float(ticker["low"]),
                "volume": float(ticker["vol_idr"]),
             }
         return tickers

    def fetch_ohlcv(self, pair, timeframe, since=None, limit=None):
        """
        Fetch OHLCV data for a trading pair.
        """
        if timeframe not in self.timeframes:
            raise ValueError(f"Timeframe {timeframe} is not supported.")

        params = {
            "symbol": pair.replace("/", "_").lower(),
            "resolution": self.timeframes[timeframe],
            "from": since or 0,
            "to": "9999999999",  # Use a high timestamp if `since` is not provided
        }
        data = self._request("chart", params)
        ohlcv = [
            [
                int(candle["time"]),
                float(candle["open"]),
                float(candle["high"]),
                float(candle["low"]),
                float(candle["close"]),
                float(candle["volume"]),
            ]
             for candle in data
        ]
        return ohlcv

    def fetch_balance(self):
        """
        Fetch account balance.
        """
        # Normally, authenticated requests require HMAC signing with API key/secret.
        raise NotImplementedError("Authenticated requests are not implemented yet.")

    def fetch_order_book(self, pair, limit=None):
        """
        Fetch the order book for a trading pair.
        """
        endpoint = f"depth/{pair.replace('/', '_').lower()}"
        data = self._request(endpoint)
        return {
            "bids": [[float(order[0]), float(order[1])] for order in data["buy"]],
            "asks": [[float(order[0]), float(order[1])] for order in data["sell"]],
        }
