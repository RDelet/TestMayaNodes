# coding=ascii

import os
import logging
import sys


_kLoggerName = "Nodes"
_kLogLevel = logging.DEBUG

_formatter_str = f"[{_kLoggerName} %(levelname)s] - "
_formatter_str += "[%(asctime)s] - [%(module)s.%(funcName)s, ln.%(lineno)d] -> %(message)s"
_formatter = logging.Formatter(_formatter_str)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(_formatter)


def set_output_path(logger: logging.Logger, path: str, formatter: logging.Formatter = _formatter):
    path = os.path.normpath(path)
    if os.path.isdir(path):
        path = os.path.normpath(os.path.join(path, f"{_kLoggerName}.log"))

    # make sure directory exists
    directory = os.path.split(path)[0]
    if not os.path.exists(directory):
        os.mkdir(directory)

    # make sure file exists
    if not os.path.exists(path):
        with open(path, "w") as stream:
            stream.write("")

    file_handler = logging.FileHandler(path, "w")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def set_log_level(logger: logging.Logger, log_level: int):
    logger.setLevel(log_level)
    stream_handler.setLevel(log_level)


stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setLevel(_kLogLevel)
stream_handler.setFormatter(_formatter)

log = logging.getLogger(_kLoggerName)
log.setLevel(_kLogLevel)
log.addHandler(stream_handler)
log.propagate = False
