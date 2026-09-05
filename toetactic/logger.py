"""Logger for toetactic."""

from conflog import Conflog

#: Module-level cache of the initialized logger, populated on first call
#: to :func:`init` and reused on every subsequent call.
LOGGER = None


def init():
    """Initialize logger.

    Logger is cached to prevent duplicate handlers
    from being added on repeated calls.

    :returns: Shared logger instance configured with the
        ``[toetactic] LEVEL message`` format.
    :rtype: logging.Logger
    """

    global LOGGER  # pylint: disable=global-statement
    if LOGGER is not None:
        return LOGGER

    cfl = Conflog(
        conf_dict={"level": "info", "format": "[toetactic] %(levelname)s %(message)s"}
    )

    LOGGER = cfl.get_logger(__name__)
    return LOGGER
