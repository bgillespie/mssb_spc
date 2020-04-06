import pytest

from mssb_spc.espp import espp_sheet_relevant_rows


def test_espp_sheet_relevant_rows():
    source = [
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, 'Name:', None, 'DAVE      WAVES           '],
        [None, None, None, 'CompanyName:', None, 'BERKLEY                    '],
        [None, None, None, 'PlanName:', None, 'ESPP'],
        ['Acquisition Date', 'Acquired Price',
         'Acquisition Fair Market Value (FMV)', 'Transaction Type',
         'Shares Sold', 'Realized Capital Gain/Loss'],
        ['01/31/2018', 85.442, 130.96, 'Share Deposit', 81, 6438.41],
        ['01/30/2018', 107.3465, 164, 'Share Deposit', 44, 2533.61],
        ['1/30/2018', 107.3465, 164, 'Share Deposit', 19, 1094.06],
        ['', None, None, None, None, ],
        ['Sun Jan 02 07:26:41 EDT 2019', None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        [None, None, None, None, None, None],
        ['Bish Bosh Bash LLC. Member MUMBA.', None, None, None, None, None]
    ]
    expected = [
        ['Acquisition Date', 'Acquired Price',
         'Acquisition Fair Market Value (FMV)', 'Transaction Type',
         'Shares Sold', 'Realized Capital Gain/Loss'],
        ['01/31/2018', 85.442, 130.96, 'Share Deposit', 81, 6438.41],
        ['01/30/2018', 107.3465, 164, 'Share Deposit', 44, 2533.61],
        ['1/30/2018', 107.3465, 164, 'Share Deposit', 19, 1094.06],
    ]
    assert espp_sheet_relevant_rows(source) == expected
