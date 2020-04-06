from pathlib import Path

import pytest

DATA_PATH = Path(__file__).parent.parent / 'data'
DATA_FILE = DATA_PATH / 'fxrates.tsv'


@pytest.fixture(scope='module')
def fxrates():
    with open(DATA_FILE) as fh:
        lines = list(fh)
    rows = tuple(x.split('\t') for x in lines)
    return rows[1:]


