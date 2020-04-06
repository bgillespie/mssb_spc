class Error(Exception):
    """ Fx error """


class RateNotAvailableError(Error):
    """ The requested conversion rate is not available from this source. """

