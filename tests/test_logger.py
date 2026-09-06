# pylint: disable=missing-module-docstring,missing-class-docstring,missing-function-docstring,duplicate-code,too-many-locals
import logging
import unittest

import toetactic.logger as logger_module


class TestLogger(unittest.TestCase):

    def test_init(self):
        logger_module.LOGGER = None
        logger = logger_module.init()
        assert isinstance(logger, logging.LoggerAdapter) is True

    def test_init_returns_cached_logger(self):
        logger_module.LOGGER = None
        first_logger = logger_module.init()
        second_logger = logger_module.init()

        assert first_logger is second_logger
