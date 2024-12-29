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
    officially supported by the Freqtrade development team. So some features
    may still not work as expected.
    """
    def fetch_ticker(self, symbol):
        """
        Fetch ticker data for a single trading pair.
        :param symbol: The trading pair symbol.
        :return: Ticker data.
        """
        try:
            return self._api.fetch_ticker(symbol)
        except Exception as e:
            raise RuntimeError(f"Failed to fetch ticker for {symbol}: {e}")
