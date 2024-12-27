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

    Please note that this exchange is not included in the list of exchanges
    officially supported by the Freqtrade development team. Some features
    may not work as expected.
    """

    _ft_has: FtHas = {
        "ohlcv_candle_limit": 100,
    }

    def __init__(self, *args, validate=False, **kwargs):
        super().__init__(*args, validate=validate, **kwargs)

        self.validate = validate
        self.exchange = ccxt.indodax(
            {
                "apiKey": kwargs.get("api_key"),
                "secret": kwargs.get("api_secret"),
            }
        )
        self._markets = None  # Cache for market data
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
    def timeframes(self):
        """Return the available timeframes for this exchange."""
        return self._timeframes

    @property
    def markets(self):
        """
        Return the markets available on the exchange.
        Fetches and caches markets if not already cached.
        """
        if not self._markets:
            try:
                self._markets = {
                    market["symbol"]: market for market in self.exchange.fetch_markets()
                }
            except Exception as exc:
                raise RuntimeError(f"Failed to fetch markets: {exc}") from exc
        return self._markets

    def fetch_ticker(self, symbol):
        """Fetch ticker data for a symbol."""
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as exc:
            raise RuntimeError(f"Failed to fetch ticker for {symbol}: {exc}") from exc

    def fetch_tickers(self, pairs=None):
        """
        Fetch all tickers from the exchange.

        :param pairs: Optional list of pairs to fetch tickers for.
        :return: Tickers as a dictionary.
        """
        try:
            return self.exchange.fetch_tickers(pairs)
        except Exception as exc:
            raise RuntimeError(f"Failed to fetch tickers for {pairs}: {exc}") from exc

    def fetch_ohlcv(self, pair, timeframe, since=None, limit=None):
        """
        Fetch OHLCV data for a trading pair.

        :param pair: The pair to fetch OHLCV for.
        :param timeframe: The timeframe to fetch.
        :param since: Timestamp in ms to fetch data from.
        :param limit: Number of data points to fetch.
        :return: OHLCV data as a list.
        """
        if timeframe not in self.timeframes:
            raise ValueError(f"Timeframe {timeframe} is not supported.")
        try:
            return self.exchange.fetch_ohlcv(pair, timeframe, since, limit)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch OHLCV for {pair} with timeframe {timeframe}: {e}")

    def ohlcv_candle_limit(
        self, timeframe: str, candle_type: CandleType, since_ms: int | None = None
    ) -> int:
        """
        Return the maximum number of candles that the exchange supports for the given timeframe.

        :param timeframe: Timeframe in the format '1m', '5m', '1d', etc.
        :param candle_type: The type of candle (specific to freqtrade configuration).
        :param since_ms: Timestamp in milliseconds (optional).
        :return: Integer indicating the maximum number of candles.
        """
        candle_limits = {
            "1m": 1440,  # Example: 1440 1-minute candles (24 hours)
            "15m": 96,  # Example: 96 15-minute candles (24 hours)
            "30m": 48,  # Example: 48 30-minute candles (24 hours)
            "1h": 24,  # Example: 24 hourly candles (24 hours)
            "4h": 7,  # Example: 7 4-hour candles (28 hours)
            "1d": 365,  # Example: 365 daily candles (1 year)
        }
        return candle_limits.get(timeframe, 100)  # Default to 100 if timeframe is not in the dict

    def close(self):
        """Clean up resources if necessary."""
        pass
