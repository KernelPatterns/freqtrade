"""Indodax exchange subclass"""

import logging

import ccxt

from freqtrade.enums import CandleType
from freqtrade.exchange import Exchange
from freqtrade.exchange.exchange_types import FtHas


logger = logging.getLogger(__name__)


class Indodax(Exchange):
    """
    Indodax exchange class. Contains adjustments needed for Freqtrade to work
    with this exchange.
    """

    _ft_has: FtHas = {
        "ohlcv_candle_limit": 100,
    }

    def __init__(self, *args, validate=False, **kwargs):
        super().__init__(*args, **kwargs)  # Initialize parent class
        self.validate = validate
        self.exchange = ccxt.indodax(
            {
                "apiKey": kwargs.get("api_key"),
                "secret": kwargs.get("api_secret"),
            }
        )

        self._markets = None  # Initialize _markets as None
        self._timeframes = {
            "1m": "1m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "4h": "4h",
            "1d": "1d",
        }
        self._ccxt_has = {
            "fetchOHLCV": True,
            "fetchTicker": True,
            "fetchTickers": True,
            "fetchTrades": True,
            "fetchBalance": True,
            "fetchMarkets": True,
        }

    @property
    def markets(self):
        """
        Returns the markets available on the exchange. Fetches and caches markets if not already cached.
        """
        if not self._markets:
            self._markets = self.fetch_markets()
        return self._markets

    def fetch_markets(self):
        """
        Fetch and return market data from the exchange.
        """
        try:
            markets = self.exchange.fetch_markets()
            return {market["symbol"]: market for market in markets}
        except Exception as e:
            raise RuntimeError(f"Failed to fetch markets: {e}")

    def fetch_ticker(self, symbol):
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch ticker for {symbol}: {e}")

    def fetch_tickers(self, pairs=None):
        try:
            return self.exchange.fetch_tickers(pairs)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch ticker for {pairs}: {e}")

    def fetch_ohlcv(self, pair, timeframe, since=None, limit=None):
        if timeframe not in self.timeframes:
            raise ValueError(f"Timeframe {timeframe} is not supported.")
        return self.exchange.fetch_ohlcv(pair, timeframe, since, limit)

    def ohlcv_candle_limit(
        self, timeframe: str, candle_type: CandleType, since_ms: int | None = None
    ) -> int:
        candle_limits = {
            "1m": 1440,
            "15m": 96,
            "30m": 48,
            "1h": 24,
            "4h": 7,
            "1d": 365,
        }
        return candle_limits.get(timeframe, 100)

    def close(self):
        pass
