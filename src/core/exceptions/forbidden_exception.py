from typing import Optional
from fastapi import status

from .utils import ErrorCode
from .base_exception import BaseDomainException

class ForbiddenException(BaseDomainException):
    def __init__(self, message: Optional[str] = "Forbidden", **kwargs):
        super().__init__(
            message=message,
            status_code=status.HTTP_403_FORBIDDEN,
            error_code=ErrorCode.FORBIDDEN,
            **kwargs
        )

__all__ = ["ForbiddenException"]
