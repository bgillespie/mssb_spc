from typing import Iterable, MutableMapping, List
from .common import Table, Cell, xlate_kv, without_empty_columns, content_rows

import pyexcel


def rsu_sheet_relevant_rows(rsuz: Iterable[List[Cell]]) -> Table:
    # Get the relevant rows from the sheet
    rows = list(content_rows(rsuz))
    return rows


def rsu_table_to_dicts(rsuz: Table) -> Iterable[MutableMapping[str, Cell]]:
    """ Conversion of a PyExcel Sheet representing RSU details. """
    rows = iter(rsuz)
    headings = next(rows)  # skip headers
    rsuz = [
        dict(xlate_kv(field_name, field)
             for field_name, field in zip(headings, row))
        for row in rows
    ]
    return rsuz


def rsu_sheet_to_rsus(rsu_sheet: pyexcel.Sheet) \
        -> List[MutableMapping[str, Cell]]:
    """ Convert an RSU sheet from Excel into records of RSUs involved in sale.

    :param rsu_sheet: sheet from PyExcel
    :return: list of k:v mappings of RSU data.
    """
    rows = rsu_sheet_relevant_rows(rsu_sheet.rows())
    rows = without_empty_columns(rows)
    rsuz = list(rsu_table_to_dicts(rows))
    return rsuz
