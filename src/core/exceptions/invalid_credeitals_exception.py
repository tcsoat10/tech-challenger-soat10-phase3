from fastapi import status

from .utils import ErrorCode
from .base_exception import BaseAppException

class InvalidCredentialsException(BaseAppException):

    def __init__(self, **kwargs):
        super().__init__(
            message="Usuário ou senha inválidos.",
            status_code=status.HTTP_401_UNAUTHORIZED,
            error_code=ErrorCode.INVALID_CREDENTIALS,
            **kwargs
        )

__all__ = ["InvalidCredentialsException"]
