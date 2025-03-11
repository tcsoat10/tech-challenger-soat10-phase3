from fastapi import status

from src.core.exceptions.base_exception import BaseDomainException
from src.core.exceptions.utils import ErrorCode

class InvalidTokenException(BaseDomainException):
    def __init__(self, **kwargs):
        message = kwargs.pop("message")
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.INVALID_TOKEN,
            message= message or "Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
            **kwargs,
        )
