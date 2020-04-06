from datetime import date
from decimal import Decimal

from . import fxrates
from fx.boiexcel import parse_single, parse_all


def test_parse_single(fxrates):
    loaded = tuple(parse_single('ABA', fxrates))
    assert loaded == (
        (date(2008, 1, 1), Decimal('2.1')),
        (date(2008, 1, 2), Decimal('2.2')),
        (date(2008, 1, 7), Decimal('2.5')),
        (date(2008, 1, 8), Decimal('2.6')),
    )


def test_parse_all(fxrates):
    loaded = tuple(parse_all(fxrates))
    assert loaded == (
        (date(2008, 1, 1), {'ABA': Decimal('2.1'), 'BIV': Decimal('3.1'),
                            'CRB': Decimal('4.1')}),
        (date(2008, 1, 2), {'ABA': Decimal('2.2'), 'BIV': Decimal('3.2'),
                            'CRB': Decimal('4.2')}),
        (date(2008, 1, 4), {'BIV': Decimal('3.4'), 'CRB': Decimal('4.4')}),
        (date(2008, 1, 7), {'ABA': Decimal('2.5'), 'CRB': Decimal('4.5')}),
        (date(2008, 1, 8), {'ABA': Decimal('2.6'), 'BIV': Decimal('3.6')}),
    )