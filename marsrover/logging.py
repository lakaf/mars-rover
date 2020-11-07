"""Logger configuration"""

logging_config = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "[%(asctime)s][%(name)s][%(levelname)s] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "cli": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "simple",
            "stream": "ext://sys.stdout"
        }
    },
    "loggers": {
        "marsrover": {
            "level": "INFO",
            "handlers": ["cli"],
            "propagate": "no"
        }
    }
}