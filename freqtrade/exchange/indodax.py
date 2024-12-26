import ccxt

from freqtrade.exchange import Exchange


class Indodax(Exchange):
    """
    Custom implementation for the Indodax exchange.
    """

    def __init__(self, *args, validate=False, **kwargs):
        self.validate = validate
        self.exchange = ccxt.indodax(
            {
                "apiKey": kwargs.get("api_key"),
                "secret": kwargs.get("api_secret"),
            }
        )

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
        }

    @property
    def timeframes(self):
        """
        Returns the available timeframes for this exchange.
        """
        return self._timeframes

    def fetch_ticker(self, symbol):
        try:
            return self.exchange.fetch_ticker(symbol)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch ticker for {symbol}: {e}")

    def fetch_tickers(self, pairs=None):
        """
        Fetch all tickers from the exchange.
        :param pairs: Optional list of pairs to fetch tickers for.
        :return: Tickers as a dictionary.
        """
        try:
            return self.exchange.fetch_tickers(pairs)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch ticker for {pairs}: {e}")

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
        return self.exchange.fetch_ohlcv(pair, timeframe, since, limit)

    def ohlcv_candle_limit(self, timeframe: str) -> int:
        """
        Returns the maximum number of candles that the exchange supports for the given timeframe.

        :param timeframe: Timeframe in the format '1m', '1d', etc.
        :return: Integer indicating the maximum number of candles.
        """
        # Define candle limits based on Indodax capabilities (example values)
        candle_limits = {
            "1m": 1000,
            "15m": 1000,
            "30m": 1000,
            "1h": 1000,
            "4h": 1000,
            "1d": 365,
        }

        # Return the candle limit for the given timeframe or a default value
        return candle_limits.get(timeframe, 1000)  # Default to 1000 if timeframe is not in the dict
    
    def close(self):
        # Clean up resources if necessary
        pass
