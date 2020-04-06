from pathlib import Path
from datetime import date
from decimal import Decimal

import pytest

from fx.error import RateNotAvailableError
from fx.memory import MemoryFxSingle
from fx.boiexcel import parse_single


DATA_PATH = Path(__file__).parent.parent / 'data'
DATA_FILE = DATA_PATH / 'fxrates.tsv'


@pytest.fixture(scope='module')
def memory_fx_single():
    with open(DATA_FILE) as fh:
        lines = list(fh)
    rows = tuple(x.split('\t') for x in lines)
    fxrates = rows[1:]

    table = parse_single('ABA', fxrates)
    return MemoryFxSingle(symbol='EUR', table=table)


def test_memory_fx_single(memory_fx_single):
    assert memory_fx_single.rate_at_date(date(2008, 1, 2)) == Decimal('2.2')

    with pytest.raises(RateNotAvailableError):
        memory_fx_single.rate_at_date(date(2008, 1, 3))


def test_iter_rates_over_date_range(memory_fx_single):
    assert list(
            memory_fx_single.iter_rates_over_date_range(
                date(2008, 1, 3), date(2008, 1, 13)
            )
        ) == [(date(2008, 1, 7), Decimal('2.5')),
              (date(2008, 1, 8), Decimal('2.6'))]
