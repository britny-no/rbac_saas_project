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
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    compression="zip",
    serialize=True,  # JSON 직렬화
)

def get_logger(name: str):
    return logger.bind(context=name)
