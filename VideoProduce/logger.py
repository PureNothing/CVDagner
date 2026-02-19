import os
import sys
from loguru import logger
from datetime import datetime

os.makedirs("logs", exist_ok=True)

filename = f"logs/video_produce.log"

logger.remove()

logger.add(
    filename,
    level = "DEBUG",
    rotation = "1 day",
    retention = 3,
    compression = zip,
    format = "{time} {level} {message} {function}"
)

logger.add(
    sys.stderr,
    level = "DEBUG",
    colorize = True,
    format = "<red>{time:HH:mm:ss}</red> | <level>{level: <8}</level> | <cyan>{message}</cyan> | {extra}"
)

logger = logger.bind(service="VideoProduce")
