import pytest

from mssb_spc.common import *


def test_str_us_to_date():
    assert str_us_to_date('12/20/2019') == date(year=2019, month=12, day=20)


def test_str_iso_to_date():
    assert str_iso_to_date('2019-12-20') == date(year=2019, month=12, day=20)


def test_record_to_cc():
    assert cc_rate('1 USD = 0.87 EUR') == Decimal('0.87')


def test_currency():
    assert currency(0.22) == Decimal('0.22')
    with pytest.warns(None):
        currency('hello')


def test_norm_key():
    assert norm_key('Net Proceeds ({reqCurr})') == 'net_proceeds_reqcurr'


def test_xlate_kv():
    tests = (
        (('Acquired   Date ', '12/20/2019'),
         ('acquired_date', date(year=2019, month=12, day=20))),
        ((' Acquired Price', 12.34),
         ('acquired_price', Decimal('12.34'))),
        (('Final Currency Conversion Rate', '1 USD = 0.87 EUR'),
         ('conversion_rate', Decimal('0.87'))),
        (('Final Currency Conversion Rate', '1 spondoolic'),
         ('conversion_rate', None)),
        (('Net Proceeds ({reqCurr})', 1.01),
         ('net_proceeds_reqcurr', Decimal('1.01'))),
        (('Order Number', 12),
         ('order_number', 12)),
        (('Order Source', 'Web'),
         ('order_source', 'Web')),
    )
    for (test_key, test_value), (expected_key, expected_value) in tests:
        assert xlate_kv(test_key, test_value) == (expected_key, expected_value)


def test_rows_same_width():
    table = [
        '1'.split(),
        '2 3 4'.split(),
        '5 6'.split(),
    ]
    expected = [['1', '', ''], ['2', '3', '4'], ['5', '6', '']]
    assert rows_same_width(table) == expected


def test_without_empty_rows():
    table = [
            [],
            ['1', '', ''],
            ['2', '3', '4'],
            ['', '', ''],
            ['5', '6', ''],
        ]
    expected = [['1', '', ''], ['2', '3', '4'], ['5', '6', '']]
    assert without_empty_rows(table) == expected


def test_without_empty_columns():
    table = [
            ['1', '', '', ''],
            ['2', '', '3', '4'],
            ['5', '', '6', ''],
        ]
    expected = [['1', '', ''], ['2', '3', '4'], ['5', '6', '']]
    assert without_empty_columns(table) == expected


def test_split_table_at_heading():
    table = [
        ['F', 'A', 'D', 'G'],
        [1, 2, 3, 4],
        [5, 6, 7, 8],
    ]
    expected = [
        ([1, 2], [3, 4]),
        ([5, 6], [7, 8]),
    ]
    assert list(split_table_at_heading(table, 'D')) == expected

    expected = [
        (['F', 'A', 'D'], ['G']),
        ([1, 2, 3], [4]),
        ([5, 6, 7], [8]),
    ]
    assert list(split_table_at_heading(table, 'G', remove_heading=False)) \
        == expected

    expected = [
        ([], [1, 2, 3, 4]),
        ([], [5, 6, 7, 8]),
    ]
    assert list(split_table_at_heading(table, 'F')) == expected


def test_to_single_table():
    tables = [
        (['a', '1'], ['b', '2']),
        (['c', '3'], ['d', '4']),
    ]
    expected = [['a', '1'], ['c', '3'], ['b', '2'], ['d', '4']]
    assert to_single_table(tables) == expected


def test_plan_type():
    tests = {
        'ESPP': PlanType.ESPP,
        'RESTRICTED STOCK AWARDS/UNITS': PlanType.RSU,
    }
    for test, expected in tests.items():
        assert PlanType.from_s(test) is expected
