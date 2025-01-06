import sys
from loguru import logger

# Configure loguru
logger.remove()
logger.add(
    "debug.log",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="DEBUG",
    rotation="500 MB"
)
logger.add(sys.stderr, level="INFO")