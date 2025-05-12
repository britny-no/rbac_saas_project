from loguru import logger
import sys

logger.remove() 
logger.add(
    sys.stdout,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO",
    enqueue=True,  
    backtrace=True, 
    diagnose=True, 
)

logger.add(
    "logs/info.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    serialize=True,
    filter=lambda record: record["level"].name == "INFO"
)

logger.add(
    "logs/error.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    serialize=True,
    filter=lambda record: record["level"].name == "ERROR"
)

logger.add(
    "logs/debug.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    serialize=True,
    filter=lambda record: record["level"].name == "DEBUG"
)

def get_logger(name: str):
    return logger.bind(context=name)
