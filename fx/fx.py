""" Currency exchange interface.
"""

from abc import ABC, abstractmethod
from datetime import date as Date
from typing import Iterator, Tuple

from . import Sym, Rate, Currency
from .error import RateNotAvailableError


class FxSingle(ABC):
    """ Foreign exchange abstract class.

    For my purposes I only needed to convert between Euro and Dollar, so this
    class just assumes all conversions will be between two (unspecified)
    currencies: a "primary" currency (in my case, Euro) and another.
    """

    def __init__(self, symbol: Sym):
        """
        :param symbol: the Fx symbol of the "primary" currency, e.g. "EUR"
        """
        self._symbol = symbol.strip().upper()

    def convert_to(self, date: Date, amount: Currency) -> Currency:
        """ Convert from the "primary" currency to the other at the given date.
        :param date: the date at which the exchange was made.
        :param amount: the amount in the "primary" currency.
        :return: the equivalent amount in the target currency at the date given.
        """
        rate = self.rate_at_date(date)
        return amount * rate

    def convert_from(self, date: Date, amount: Currency) -> Currency:
        """ Convert to the "primary" currency from the other at the given date.
        :param date: the date at which the exchange was made.
        :param amount: the amount in the "other" currency.
        :return: the equivalent amount in the primary currency at the date.
        """
        rate = self.rate_at_date(date)
        return amount / rate

    @abstractmethod
    def rate_at_date(self, date: Date) -> Rate:
        """ Get the ratio of primary:other currency values at the given date.
        :param date: the date in question.
        :return: the ratio of primary:other currency values at the given date.
        :raises RateNotAvailableError: if the rate couldn't be obtained.
        """
        raise RateNotAvailableError("Not implemented") \
            from NotImplementedError()

    @abstractmethod
    def iter_rates_over_date_range(self, start: Date, end: Date) \
            -> Iterator[Tuple[Date, Rate]]:
        """ Iterate over all the exchange rates between two dates, in order. """
        raise NotImplementedError()
