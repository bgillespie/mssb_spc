from typing import Iterable, MutableMapping
from .common import \
    Table, Row, Cell,\
    xlate_kv, rows_same_width, without_empty_columns,\
    to_single_table, split_table_at_heading

import pyexcel


#
# SALE SHEET SPECIFICS
#

def sale_sheet_relevant_rows(sheet: Iterable[Row]) -> Table:
    # Get the relevant rows from the sheet
    rows = []
    for row in sheet:
        if not rows and 'Order Details' not in row:
            # Only start recording at first row
            continue
        if all(not x for x in row):
            # An empty row marks the end.
            # break before recording last+1 row
            break
        rows.append(row)
    return rows


def sales_table_to_dict(table: Table) -> MutableMapping[str, Cell]:
    """ By this point every row is a single k/v pair. Now make a dict from it.

    :param table: rows of key, value pairs
    :returns: a mapping of normalized keys to normalized values
    :raises ValueError: if there is >0 duplicate headings
    """
    # Ensure no headings will be discarded
    if len(set(r[0] for r in table)) != len(table):
        raise ValueError("Non-unique heading(s) detected")
    return dict(xlate_kv(k, v) for k, v in table)


def sale_sheet_to_dict(sheet: pyexcel.Sheet) -> MutableMapping[str, Cell]:
    """ Conversion of a PyExcel Sheet representing a sale to a dict. """
    rows = sale_sheet_relevant_rows(sheet.rows())
    rows = rows_same_width(rows)
    rows = without_empty_columns(rows)
    table = to_single_table(split_table_at_heading(rows, 'Proceeds Details'))
    table = sales_table_to_dict(table)
    return table
