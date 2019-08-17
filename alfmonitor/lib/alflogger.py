""" Logger module for alfmonitor."""

import logging
import sys

from alfmonitor.settings import (
    LOGGING_LEVEL, LOG_FILE, LOG_WRITE_MODE, WRITE_TO_CONSOLE
)


LOGGING_FORMAT = '%(asctime)s [%(levelname)s]' + \
    ' [%(name)s.%(funcName)s]:%(lineno)s' + \
    ' %(message)s'


def get_log_level():
    level = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warn': logging.WARN,
        'error': logging.ERROR,
        'critical': logging.CRITICAL,
    }
    return level[LOGGING_LEVEL.lower()]


def logger(name):

    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(get_log_level())

    log_format = logging.Formatter(
        LOGGING_FORMAT
    )

    file_handler = logging.FileHandler(
        filename=LOG_FILE, mode=LOG_WRITE_MODE
    )
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    if WRITE_TO_CONSOLE:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

    return logger
