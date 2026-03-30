
import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    """
    Sets up and returns a logger that logs to both a rotating file and the console.
    The log file is rotated to prevent it from growing too large.
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("TradingBot")
    logger.setLevel(logging.INFO)

    # Rotating File Handler - prevents the log file from growing too large
    file_handler = RotatingFileHandler("trading_bot.log", maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Console Handler - displays logs in the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger

# Global logger instance for use throughout the project
logger = setup_logger()