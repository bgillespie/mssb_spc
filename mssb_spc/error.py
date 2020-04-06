class Error(Exception):
    """ Base class for all `mssb_spc` exceptions. """


class BookParseError(Error):
    """ The given book can't be parsed as a sale book. """


class SaleSheetParseError(BookParseError):
    """ The given sheet couldn't be parsed as a Sale. """


class TableError(Error):
    """ On operation on a table failed. """


class CellNotFoundError(TableError):
    """ A Cell could not be found, e.g. whilst splitting on header. """

