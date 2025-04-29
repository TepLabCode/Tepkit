from ._logger import logger

# @deprecated("`logger_c` is deprecated, use `logger.color` or `logger.c` instead.")
from ._logger import logger_c


class InvalidArgumentError(Exception):
    """
    Raised when the arguments passed to command line functions are invalid.
    """
