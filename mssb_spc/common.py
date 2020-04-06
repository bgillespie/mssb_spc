from typing import Union, Optional, Iterable, Iterator, List, Tuple, Mapping
from decimal import Decimal, InvalidOperation
from datetime import date as Date, datetime as DateTime
from re import compile as Re, sub as re_sub
from warnings import warn
import enum

from dictionaries import FrozenOrderedDict, FrozenDict

from .error import CellNotFoundError

# typedefs
Cell = Union[str, int, Decimal, Date]  # this is what can be in any table cell
Row = List[Optional[Cell]]             # this is how a row is made up
Table = List[Row]                      # a table is an ordered list of rows
Currency = Decimal                     # Just use a simple Decimal for now

# Regexen
RE_CURR_CONV_DESC = Re(
    r'^\s*(?P<src_amt>[0-9]+(?:\.[0-9]+)?)'  # source amount
    r'\s*(?P<src_sym>[A-Z]{3})\s*='          # source symbol (e.g. USD)
    r'\s*(?P<dst_amt>[0-9]+(?:\.[0-9]+)?)'   # dest amount
    r'\s*(?P<dst_sym>[A-Z]{3})\s*$'          # dest symbol (e.g. EUR)
)

# Datetime format conversions
STRF_US_DT  = "%m/%d/%Y"  # US middle-endian date format
STRF_ISO_DT = "%Y-%m-%d"  # ISO big-endian date format


class PlanType(enum.Enum):
    RSU  = enum.auto()
    ESPP = enum.auto()

    @classmethod
    def from_s(cls, src: str) -> "PlanType":
        norm = str(src).strip().lower()
        matches = FrozenDict({
            PlanType.RSU: ('restricted stock unit', 'restricted stock award',
                           'rsu'),
            PlanType.ESPP: ('espp',),
        })
        for stock_type, matchers in matches.items():
            if any(match in norm for match in matchers):
                return stock_type
        raise ValueError(f"Could not determine plan type for 'src'")

    def __str__(self):
        return str(self.name)

    def __repr__(self):
        return str(self.name)


#
# TRANSLATORS
#

def str_us_to_date(us_date_str: str) -> Date:
    """ Convert a US-format date string to a date object. """
    return DateTime.strptime(us_date_str, STRF_US_DT).date()


def str_iso_to_date(iso_date_str: str) -> Date:
    """ Convert an ISO-format date string to a date object. """
    return DateTime.strptime(iso_date_str, STRF_ISO_DT).date()


def currency(c: float) -> Optional[Currency]:
    """ Convert the source sheets' floats to Decimals """
    try:
        return Currency(str(c))
    except InvalidOperation:
        # this is usually where the source sheet cell isn't in expected form
        warn(f"Couldn't convert '{c}' to currency")
        return None


def cc_rate(v: str) -> Optional[Decimal]:
    """ Convert the currency conversion field. """
    m = RE_CURR_CONV_DESC.match(v)
    if not m:
        return None
    m = m.groupdict()
    return Decimal(m['dst_amt'])


def norm_key(k: str) -> str:
    """ Normalize a key name """
    norm = \
        str(k)\
        .lower()\
        .strip()\
        .translate(
            str.maketrans({'/': '_', '(': '', ')': '', '{': '', '}': ''})
        )
    norm = re_sub(r'\s+', '_', norm)
    norm = re_sub(r'_+', '_', norm)
    norm = re_sub(r'(^_|_$)', '', norm)
    return norm


# Mapping of normalized original name to (new name, value translator)
XLATORS = FrozenOrderedDict({
    'acquired_date'                 : ('acquired_date'       , str_us_to_date),
    'acquisition_date'              : ('acquired_date'       , str_us_to_date),
    'acquisition_fair_market_value_fmv'
                                    : ('acquired_fmv'        , currency),
    'acquired_price'                : ('acquired_price'      , currency),
    'backup_withholding'            : ('backup_withholding'  , currency),
    'commissions'                   : ('commissions'         , currency),
    'final_currency_conversion_rate': ('conversion_rate'     , cc_rate),
    'gross_proceeds'                : ('gross_proceeds'      , currency),
    'net_proceeds'                  : ('net_proceeds_usd'    , currency),
    'net_proceeds_reqcurr'          : ('net_proceeds_reqcurr', currency),
    'order_number'                  : ('order_number'        , int),
    'order_source'                  : ('order_source'        , str),
    'order_status'                  : ('status'              , str),
    'order_type'                    : ('order_type'          , str),
    'plan_name'                     : ('plan_type'           , PlanType.from_s),
    'proceeds_delivery_fee'         : ('delivery_fee'        , currency),
    'proceeds_delivery_method'      : ('delivery_method'     , str),
    'proceeds_delivery_methods'     : ('delivery_method'     , str),
    'proceeds_type'                 : ('proceeds_type'       , str),
    'processing_fee'                : ('processing_fee'      , currency),
    'realized_capital_gain_loss'    : ('gain'                , currency),
    'requested_currency'            : ('requested_currency'  , str),
    'sale_price'                    : ('sale_price'          , currency),
    'settlement_date'               : ('settlement_date'     , str_us_to_date),
    'shares'                        : ('shares'              , int),
    'shares_sold'                   : ('shares'              , int),
    'status'                        : ('status'              , str),
    'stock_symbol'                  : ('stock_symbol'        , str),
    'supplemental_transaction_fee'  : ('supplemental_fee'    , currency),
    'total_fees'                    : ('total_fees'          , currency),
    'trade_date'                    : ('trade_date'          , str_us_to_date),
    'transaction_date'              : ('trade_date'          , str_us_to_date),
    'transaction_type'              : ('transaction_type'    , str),
})


def xlate_kv(k: str, v: Cell, translators: Mapping[str, Cell] = XLATORS) \
        -> Tuple[str, Optional[Cell]]:
    """ Take a key and a value and translate both according to the rules above.
    :returns: translated key and translated value
    """
    k, translator = translators[norm_key(k)]
    return k, translator(v)


#
# Table mangling
#

def rows_same_width(rows: Table, fill_val='') -> Table:
    """ Get a copy of the Table where all rows are the same width. """
    width = max(len(row) for row in rows)
    return [row + [fill_val] * (width - len(row)) for row in rows]


def without_empty_rows(rows: Table) -> Table:
    """ Get a copy of the Table without empty rows. """
    return [row for row in rows if any(not not x for x in row)]


def without_empty_columns(rows: Table) -> Table:
    """ Get copy of a Table without empty columns. """
    cols = [list(x) for x in zip(*rows)]    # transpose
    cols = without_empty_rows(cols)         # now just use empty row filter
    cols = [list(x) for x in (zip(*cols))]  # transpose back again
    return cols


def split_table_at_heading(table: Table, heading: str, remove_heading=True) \
        -> Iterator[Tuple[Row, Row]]:
    """ Find the column with given heading and split into two tables.

    This is needed because the sale sheet contains two tables that are
    side-by-side for easy reading in Excel, but for our purposes need to be
    placed one atop the other.

    :param table: the data to split into two
    :param heading: what cell value to split at in the first row
    :param remove_heading: throw away the first row?
    :return: iterator over 2-tuple of rows from each separated table.
    """
    table_iter = iter(table)
    row = next(table_iter)
    if heading not in row:
        raise CellNotFoundError(
            f"Couldn't find column named '{heading}'"
        )
    col_index = row.index(heading)
    if not remove_heading:
        yield row[:col_index], row[col_index:]
    for row in table_iter:
        yield row[:col_index], row[col_index:]


def to_single_table(tables: Iterable[Tuple[Row, Row]]) -> Table:
    """ Merge two halves of table into single table omitting empty rows.

    The usual sale sheet is one table split into two tables side-by-side.
    This merges them (after having been parsed) into one k/v table.
    """
    table_a, table_b = zip(*tables)
    table_a = [list(row) for row in without_empty_rows(table_a)]
    table_b = [list(row) for row in without_empty_rows(table_b)]
    return table_a + table_b


def content_rows(rows: Iterable[Row]) -> Iterator[Row]:
    """ Get the content from a certain kind of sheet.

    Some sheets' content can be extracted by waiting for the first row with
    something in the leftmost cell, then stopping when a completely empty row
    is returned.
    """
    # Get the relevant rows from the sheet
    reading = False
    for row in rows:
        row = ['' if cell is None else cell for cell in row]
        row = [cell.strip() if isinstance(cell, str) else cell for cell in row]
        if not reading:
            if not (row[0] and row[0].strip()):
                # a row with a value in the leftmost cell marks the beginning
                continue
            else:
                reading = True
                # fall through...
        if all(not x for x in row):
            # an empty row marks the end
            break
        yield list(row)
