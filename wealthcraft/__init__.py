import logging


def logger_factory() -> logging.Logger:
    logger = logging.getLogger("wealthcraft")

    return logger


logger = logger_factory()
