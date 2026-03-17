import logging
import os
from datetime import datetime

_logger = None
_display_toggle = True
_console_handler = None

def displaytoggle(flag: bool):

    global _display_toggle, _logger, _console_handler

    _display_toggle = flag

    if _logger is None or _console_handler is None:
        return

    if flag:
        if _console_handler not in _logger.handlers:
            _logger.addHandler(_console_handler)

    else:
        if _console_handler in _logger.handlers:
            _logger.removeHandler(_console_handler)


def get_logger():

    global _logger, _console_handler

    if _logger:
        return _logger  # 二重防止

    os.makedirs("logs", exist_ok=True)

    logname = datetime.now().strftime("%Y%m%d_%H%M%S.log")
    logfile = os.path.join("logs", logname)

    logger = logging.getLogger("app")
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s"
    )

    # CLI
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    _console_handler = ch

    # file
    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setFormatter(formatter)

    if _display_toggle:
        logger.addHandler(ch)

    logger.addHandler(fh)

    _logger = logger
    return logger