import logging
import os
from datetime import datetime

_logger = None

def get_logger():
    global _logger

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

    # file
    fh = logging.FileHandler(logfile, encoding="utf-8")
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    _logger = logger
    return logger