from typing import Iterable, MutableMapping, List
from .common import Table, Cell, xlate_kv, without_empty_columns, content_rows

import pyexcel


def espp_sheet_relevant_rows(esppz: Iterable[List[Cell]]) -> Table:
    # Get the relevant rows from the sheet
    rows = list(content_rows(esppz))
    return rows


def espp_table_to_dicts(esppz: Table) -> Iterable[MutableMapping[str, Cell]]:
    """ Conversion of a PyExcel Sheet representing ESPP details. """
    rows = iter(esppz)
    headings = next(rows)  # skip headers
    esppz = [
        dict(xlate_kv(field_name, field)
             for field_name, field in zip(headings, row))
        for row in rows
    ]
    return esppz


def espp_sheet_to_espps(espp_sheet: pyexcel.Sheet) \
        -> List[MutableMapping[str, Cell]]:
    """ Convert an ESPP sheet from Excel into records of ESPPs involved in sale.

    :param espp_sheet: sheet from PyExcel
    :return: list of k:v mappings of ESPP data.
    """
    rows = espp_sheet_relevant_rows(espp_sheet.rows())
    rows = without_empty_columns(rows)
    esppz = list(espp_table_to_dicts(rows))
    return esppz
