from loguru import logger
import os
import sys

os.makedirs("logs", exist_ok=True)
file_name = f"logs/alerts_service.log"

logger.remove()

logger.add(
    file_name,
    level="DEBUG",
    rotation = "1 day",
    retention = 3,
    compression = zip,
    format = "{time} {level} {message} {function} {file}:{line}"
)

logger.add(
    sys.stderr,
    level="DEBUG",
    colorize=True,
    format="<red>{time:HH:mm:ss}</red> | <level>{level: <8}</level> | <cyan>{message}</cyan> | {extra} <yellow>{file}:{line}</yellow>"
)

logger = logger.bind(service = "AlertsService")







