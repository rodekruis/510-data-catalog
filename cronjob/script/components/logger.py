import logging
from logging.handlers import RotatingFileHandler
from sys import stdout


def configure_global_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    file_handler = RotatingFileHandler("./log/app_log.log", maxBytes=512)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.ERROR)

    console_handler = logging.StreamHandler(stream=stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


logger = configure_global_logger()
