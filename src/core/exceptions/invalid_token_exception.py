from fastapi import HTTPException, status

from src.core.exceptions.utils import ErrorCode

class InvalidTokenException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            code=str(ErrorCode.INVALID_TOKEN),
            message="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
            **kwargs,
        )
