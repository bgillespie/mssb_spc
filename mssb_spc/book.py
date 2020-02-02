from typing import MutableMapping
import pyexcel

from .sale import sale_sheet_to_dict
from .espp import espp_sheet_to_espps
from .rsu import rsu_sheet_to_rsus
from .common import PlanType


def book_to_sale(book: pyexcel.Book) -> MutableMapping:
    """ Extracts RSU/ESPP sale data from a SPC Sale Excel workbook.

    :param book: the loaded workbook
    :return: all the data relevant to the sale.
    """
    # Convert the sale sheet
    sale_sheet = book.sheet_by_index(0)
    sale: MutableMapping = sale_sheet_to_dict(sale_sheet)

    if sale['plan_type'] is PlanType.RSU:
        rsu_sheet = book.sheet_by_index(1)
        sale['rsus'] = rsu_sheet_to_rsus(rsu_sheet)
    elif sale['plan_type'] is PlanType.ESPP:
        espp_sheet = book.sheet_by_index(1)
        sale['espps'] = espp_sheet_to_espps(espp_sheet)
    else:
        raise ValueError("Couldn't determine sale type of book")

    return sale


def load_book(file_name):
    """ Load sale data from a workbook. Convert it to a sale. """
    book = pyexcel.get_book(file_name=file_name)
    sale = book_to_sale(book)
    sale['_from_file'] = file_name
    return sale

