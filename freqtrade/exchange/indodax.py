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
 
        super().__init__(config)
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
            "fetchTickers": True,
            "fetchTicker": True,
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
        return super().fetch_tickers(pairs)

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
        return super().fetch_ohlcv(pair, timeframe, since, limit)

    def close(self):
        # Clean up resources if necessary
        pass
