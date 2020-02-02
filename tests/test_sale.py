import pytest

from mssb_spc.sale import *


def test_sale_sheet_relevant_rows():
    table = [
        'a b c'.split(),
        'c d'.split() + ['Order Details'],
        'e f g'.split(),
        'h i j'.split(),
        ['', '', ''],
        'k l m'.split(),
    ]
    assert len(sale_sheet_relevant_rows(table)) == 3


def test_sales_table_to_dict():
    # ensure duplicate keys barf
    table = [
        ['hello', 2],
        ['hello', 3],
    ]
    with pytest.raises(ValueError):
        sales_table_to_dict(table)
