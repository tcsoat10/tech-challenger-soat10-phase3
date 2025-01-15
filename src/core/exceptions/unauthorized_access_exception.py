from typing import Optional
from fastapi import status
from src.core.exceptions.utils import ErrorCode
from src.core.exceptions.base_exception import BaseAppException


class UnauthorizedAccessException(BaseAppException):
    def __init__(self, message: Optional[str] = "Unauthorized", **kwargs):
        super().__init__(
            message=message,
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.UNAUTHORIZED,
            **kwargs
        )

__all__ = ["UnauthorizedAccessException"]
    