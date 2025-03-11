from fastapi import status

from .utils import ErrorCode
from .base_exception import BaseDomainException

class ValidationException(BaseDomainException):
    def __init__(self, field: str, expected_format: str, **kwargs):
        super().__init__(
            message=f"Invalid input for field {field}",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            error_code=ErrorCode.VALIDATION_ERROR,
            details={"field": field, "expected_format": expected_format},
            **kwargs
        )

__all__ = ["ValidationException"]
