import logging
from typing import Optional
from fastapi import HTTPException, status

from src.core.exceptions.utils import ErrorCode

class BaseAppException(HTTPException):
    def __init__(self, message: str = None, status_code: int = status.HTTP_400_BAD_REQUEST, error_code: Optional[ErrorCode] = None, details: Optional[dict] = None, headers: Optional[dict] = None):
        logging.error(f"Error {error_code}: {message} - Details: {details}")
        super().__init__(
            status_code=status_code,
            headers=headers,
            detail={
                "message": message or error_code.description,
                "code": str(error_code),
                "details": details
            }
        )

__all__ = ["BaseAppException"]