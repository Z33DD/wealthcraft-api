import logging
from wealthcraft.config import settings


def logger_factory() -> logging.Logger:
    config = settings.get()
    # python_levels = logging.getLevelNamesMapping()
    # log_level = python_levels[str(config.log_level)]

    logger = logging.getLogger("wealthcraft")

    # logger.setLevel(log_level)
    return logger


logger = logger_factory()
