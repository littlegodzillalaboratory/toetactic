"""Logger for toetactic."""

from conflog import Conflog

LOGGER = None


def init():
    """Initialize logger.

    Logger is cached to prevent duplicate handlers
    from being added on repeated calls.
    """

    global LOGGER  # pylint: disable=global-statement
    if LOGGER is not None:
        return LOGGER

    cfl = Conflog(
        conf_dict={"level": "info", "format": "[toetactic] %(levelname)s %(message)s"}
    )

    LOGGER = cfl.get_logger(__name__)
    return LOGGER
