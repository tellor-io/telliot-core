import logging
import sys
from logging.handlers import RotatingFileHandler

from telliot_core.utils.home import default_homedir

log_core = logging.getLogger("telliot_core")


def init_logging(level: int) -> logging.Logger:
    """Initialize logging to console and telliot logfile."""
    log_dir = default_homedir() / "logs"
    log_dir.mkdir(exist_ok=True)
    log_filename = log_dir / ("telliot_core.log")
    log_format = "%(levelname)-7s | %(name)s | %(message)s"
    formatter = logging.Formatter(log_format)

    log_core.setLevel(logging.DEBUG)

    # Log to file
    one_mb = 1024 * 1024
    fh = RotatingFileHandler(log_filename, maxBytes=one_mb * 5, backupCount=5)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    log_core.addHandler(fh)

    # Log to stdout
    stream = logging.StreamHandler(sys.stdout)
    stream.setLevel(level)
    stream.setFormatter(formatter)
    log_core.addHandler(stream)

    return log_core
