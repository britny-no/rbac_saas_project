import traceback
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse

from app.logging_config import get_logger

logger = get_logger("Exception")

async def sqlalchemy_exception_handler(request, exc: SQLAlchemyError):
    error_trace = traceback.format_exception(type(exc), exc, exc.__traceback__)
    logger.error(f"Database error occurred: {''.join(error_trace)}")

    return JSONResponse(
        status_code=500,
        content={"message": "Database error occurred"}
    )

async def http_exception_handler(request, exc: HTTPException):
    error_trace = traceback.format_exception(type(exc), exc, exc.__traceback__)
    logger.error(f"Http error occurred: {''.join(error_trace)}")

    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )
