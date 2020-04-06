import pytest

from mssb_spc.rsu import rsu_sheet_relevant_rows


def test_rsu_sheet_relevant_rows():
    source = \
        [['', '', '', '', '', ''],
         ['', '', '', '', '', ''],
         ['', '', '', 'Name:', '', 'DAVE            WAVES           '],
         ['', '', '', 'CompanyName:', '', 'BERKLEY                       '],
         ['', '', '', 'PlanName:', '', 'RESTRICTED STOCK AWARDS/UNITS'],
         ['Acquired Date',
          'Transaction Type',
          'Acquired Price',
          'Shares',
          'Realized Capital Gain/Loss',
          ''],
         ['10/15/2019', 'Release', 180.24, 18, 82.71, ''],
         ['10/15/2019', 'Release', 180.24, 33, 151.64, ''],
         ['10/15/2019', 'Release', 180.24, 11, 50.55, ''],
         ['', '', '', '', '', ''],
         ['Sun Jan 26 10:11:07 EST 2020', '', '', '', '', ''],
         ['', '', '', '', '', ''],
         [
             'This is not an official statement.\xa0 '
             + 'Information is general in nature.',
             '',
             '',
             '',
             '',
             ''],
         ['', '', '', '', '', ''],
         ['Bish Bosh Bash LLC. Member MUMBA.', '', '', '', '', '']]
    expected = [
        ['Acquired Date',  'Transaction Type', 'Acquired Price', 'Shares',
         'Realized Capital Gain/Loss', ''],
        ['10/15/2019', 'Release', 180.24, 18, 82.71, ''],
        ['10/15/2019', 'Release', 180.24, 33, 151.64, ''],
        ['10/15/2019', 'Release', 180.24, 11, 50.55, '']]
    assert rsu_sheet_relevant_rows(source) == expected
