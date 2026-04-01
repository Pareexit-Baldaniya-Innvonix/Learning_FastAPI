# ----- library import -----
import logging
from logging import Logger
from logging.config import dictConfig

# ----- local import -----
from src.classes.Settings import settings

# unified format (same as logging module)
_LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"

# mapping levels from environment variables to logging constants
LEVEL_MAP: dict[str, int] = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

# determine log level based on settings, default is INFO
TARGET_LEVEL: int = LEVEL_MAP.get(settings.LOG_LEVEL, logging.INFO)

# Logic: Use JSON logs in production, Standard for local dev
SELECTED_FORMATTER: str = "json" if settings.ENV == "production" else "standard"

# centralized logging configuration dictionary
LOGGING_CONFIG: dict[str, any] = {
    "version": 1,
    "disable_existing_loggers": False,  # keeps default loggers active so we can override them
    "formatters": {
        "json": {
            "()": "pythonjsonlogger.json.JsonFormatter",
            "format": _LOG_FORMAT,
            "datefmt": _DATE_FORMAT,
        },
        "standard": {
            "format": _LOG_FORMAT,
            "datefmt": _DATE_FORMAT,
        },
    },
    "handlers": {
        # printing logs to the terminal
        "console": {
            "level": TARGET_LEVEL,
            "formatter": SELECTED_FORMATTER,
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        # redirect Uvicorn general logs to custom handlers
        "uvicorn": {
            "handlers": ["console"],
            "level": TARGET_LEVEL,
            "propagate": False,
        },
        # redirect Uvicorn error logs
        "uvicorn.error": {
            "level": TARGET_LEVEL,
            "handlers": ["console"],
            "propagate": False,
        },
        # redirect Uvicorn access logs
        "uvicorn.access": {
            "handlers": ["console"],
            "level": "WARNING",  # using WARNING for preventing other logs
            "propagate": False,
        },
    },
    "root": {
        # default logger for the rest of the application
        "handlers": ["console"],
        "level": TARGET_LEVEL,
        "propagate": True,
    },
}


# applies dictionary to the entire project
def setup_logging() -> None:
    dictConfig(LOGGING_CONFIG)


# returns a logger instance for a specific module
def get_logger(name: str) -> Logger:
    return logging.getLogger(name)
