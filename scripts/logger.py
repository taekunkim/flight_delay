import logging

# Configure your root logger
logger = logging.getLogger("fare_tracker")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
)

handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Avoid adding multiple handlers if the script is imported multiple times
if not logger.handlers:
    logger.addHandler(handler)
