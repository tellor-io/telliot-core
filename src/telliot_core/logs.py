import logging
import sys
from logging.handlers import RotatingFileHandler

from telliot_core.utils.home import default_homedir

# from telliot_core.plugin.discover import telliot_plugins

log_core = logging.getLogger("telliot_core")


def init_logging(level: int) -> logging.Logger:
    """Initialize logging to console and telliot logfile."""
    log_dir = default_homedir() / "logs"
    log_dir.mkdir(exist_ok=True)
    log_filename = log_dir / ("telliot.log")
    log_format = "%(levelname)-7s | %(name)s | %(message)s"
    formatter = logging.Formatter(log_format)

    log_core.setLevel(logging.DEBUG)

    # File Handler
    one_mb = 1024 * 1024
    fh = RotatingFileHandler(log_filename, maxBytes=one_mb * 5, backupCount=5)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    # Console handler
    stream = logging.StreamHandler(sys.stdout)
    stream.setLevel(level)
    stream.setFormatter(formatter)

    # Add handlers to core logger
    log_core.addHandler(fh)
    log_core.addHandler(stream)

    # # Add handlers to plugins
    # for plugin_name in telliot_plugins.keys():
    #     plugin_logger = logging.getLogger(plugin_name)
    #     plugin_logger.setLevel(logging.DEBUG)
    #     plugin_logger.addHandler(stream)
    #     plugin_logger.addHandler(fh)
    #     log_core.debug(f"Configured logging for {plugin_name} plugin")

    return log_core
