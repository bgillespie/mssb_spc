import sys
import os
from pprint import pprint
from datetime import date as Date

from mssb_spc.book import load_book
from mssb_spc.error import BookParseError
from fx.boiexcel import load_single

MSSB_PATH = os.environ.get('MSSB_DATA', '.')
BOI_FX_FILE = os.environ.get('BOI_FX_PATH', 'fxrates.xls')


def print_sales(folder: str):
    print(folder)
    for file_name in os.listdir(folder):
        if file_name.endswith('.xls'):
            try:
                book = load_book(file_name=os.path.join(folder, file_name))
            except BookParseError:
                print(f"\n\n... SKIPPING FILE '{file_name}'\n\n")
                continue
            print(file_name)
            pprint(book)


def print_eur_fx(file_name):
    eur_to_usd = load_single(file_name, 'USD')
    for date, rate in eur_to_usd.iter_rates_over_date_range(Date(2019, 1, 1),
                                                            Date(2020, 1, 1)):
        print(date, rate)


if __name__ == '__main__':
    print_eur_fx(BOI_FX_FILE)
