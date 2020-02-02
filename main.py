import sys
import os
from pprint import pprint

from mssb_spc.book import load_book

# Example of loading a book and getting the sheet names
DATA_PATH = os.environ.get('MSSB_DATA')
print(DATA_PATH)
for file_name in os.listdir(DATA_PATH):
    if not(file_name.startswith('Sale') and file_name.endswith('.xls')):
        continue
    book = load_book(file_name=f"{DATA_PATH}/{file_name}")
    print(file_name)
    pprint(book)
