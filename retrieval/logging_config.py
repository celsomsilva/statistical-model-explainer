"""
Logging configuration used across the Statistical Model Explainer.

The goal here is simple: provide consistent, readable logs without forcing
each module to reinvent logging setup.

This module exposes a single helper: setup_logging().

It respects the LOG_LEVEL environment variable so verbosity can be increased
during debugging without changing code.

This is intentionally lightweight. No file logging, no complexity.
Just enough to support development and troubleshooting.
"""



import logging
import os

		
		
"""
Create and configure a logger for a given module.
This prevents duplicated handlers and keeps formatting consistent.

Parameters
----------
name : str
    Logger name, usually the module name.

Returns
-------
logging.Logger
    Configured logger instance.
"""

def setup_logging(name: str = "stat_explainer") -> logging.Logger:
    level_name = os.getenv("LOG_LEVEL", "INFO").upper()
    level = getattr(logging, level_name, logging.INFO)

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # already configured

    logger.setLevel(level)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

