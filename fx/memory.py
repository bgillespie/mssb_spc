from datetime import date as Date
from typing import Iterable, Tuple, Iterator

from dictionaries import FrozenOrderedDict

from .fx import FxSingle, Sym, Rate
from .error import RateNotAvailableError


class MemoryFxSingle(FxSingle):
    """ Load a table in memory. """

    def __init__(self, symbol: Sym, table: Iterable[Tuple[Date, Rate]]):
        """ Keep an FX rate table in memory.

        :param symbol: the Fx symbol of the "primary" currency, e.g. "EUR"
        :param table: iterable over tuples of date to rate.
        """
        super().__init__(symbol)
        loaded = list(table)
        loaded.sort()
        self._table = FrozenOrderedDict(loaded)

    def rate_at_date(self, date: Date) -> Rate:
        """ Get the exchange rate at the given date. """
        try:
            return self._table[date]
        except KeyError:
            raise RateNotAvailableError(
                f"Exchange rate at {date} for {self._symbol} not available"
            )

    def iter_rates_over_date_range(self, start: Date, end: Date) \
            -> Iterator[Tuple[Date, Rate]]:
        """ Get all the rates of the currency between two dates, inclusive. """
        rows = iter(self._table.items())
        # skip all before start
        for date, rate in rows:
            if date >= start:
                if date <= end:
                    yield date, rate
                break
        for date, rate in rows:
            if date >= end:
                break
            yield date, rate
