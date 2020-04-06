""" Load the daily Excel FX rates book from the Central Bank of Ireland.

Available here: https://www.centralbank.ie/statistics/interest-rates-exchange-rates/exchange-rates
"""

from typing import Iterable, Iterator, Mapping, Tuple, Optional, Sequence, Any
from datetime import date as Date, datetime as DateTime
import decimal

from dictionaries import FrozenOrderedDict
import pyexcel

from . import Sym, Rate
from .memory import MemoryFxSingle

# typedefs
FxRow = Tuple[Date, Mapping[Sym, Rate]]

# Date format from BoI FX rates workbook
STRF_BOI = "%d %b %y"

# Number of digits after decimal point for Rate
RATE_ROUND_DIGITS = 5


def convert_rate(rate: str) -> Optional[Rate]:
    try:
        return round(Rate(rate), RATE_ROUND_DIGITS)
    except (TypeError, decimal.InvalidOperation):
        return None


def iter_excel(file_name: str) -> Iterator[FxRow]:
    """ Iterate over BoI fxrates Excel sheet.
    :param file_name: path and name of BoI fxrates Excel file.
    """
    book = pyexcel.get_book(file_name=file_name)
    sheet = book.sheet_by_index(0)  # The first sheet has the rates we want
    rows = iter(sheet.rows())       # Iterate over its rows
    next(rows)                      # Skip row of spoken names of currencies
    yield from rows


def parse_all(rows: Iterable[Sequence[Any]]) -> Iterable[FxRow]:
    """ Get exchange rates for all known currencies on all dates available.
    :param rows:
    :return: date, mapping of symbol to rate. If the rate is not known on a
        particular date or could not be parsed, the rate is None.
    """
    rows = iter(rows)
    symbols = next(rows)[2:]  # first row is symbols; we want these
    # now we get to dates -> rates
    for row in rows:
        if all(not str(c) for c in row):
            # exit at blank row
            break
        date, rates = row[1], row[2:]
        try:
            date = DateTime.strptime(date, STRF_BOI).date()
        except ValueError:
            continue
        fx = FrozenOrderedDict(
            zip(
                (sym.strip().upper() for sym in symbols),
                (convert_rate(c) for c in rates)
            )
        )
        fx = FrozenOrderedDict(
            (symbol, rate) for symbol, rate in fx.items() if symbol and rate
        )
        if fx:
            yield date, fx


def parse_single(symbol: Sym, rows: Iterable[FxRow]) \
        -> Iterator[Tuple[Date, Rate]]:
    """ Iterate over FX rates for only a single currency. """
    rows = iter(rows)

    # Get the symbols then find the index of column with desired symbol
    symbols = list(next(rows))
    symbols = [x.strip().upper() for x in symbols]
    try:
        sym_idx = symbols.index(symbol)
    except ValueError:
        raise ValueError(f"Symbol '{symbol}' not in {', '.join(symbols)}")

    # now we get to dates -> rates
    for row in rows:
        date, rate = row[1], row[sym_idx]
        if not date and not rate:
            break
        if not date or not rate:
            continue
        date = DateTime.strptime(date, STRF_BOI).date()
        rate = convert_rate(row[sym_idx])
        yield date, rate


def load_single(file_name, symbol: Sym):
    """ Load FX data from a BoI daily rates workbook for a single currency. """
    symbol = symbol.strip().upper()
    rates_src = iter_excel(file_name)
    rates = parse_single(symbol, rates_src)
    return MemoryFxSingle(symbol, rates)
