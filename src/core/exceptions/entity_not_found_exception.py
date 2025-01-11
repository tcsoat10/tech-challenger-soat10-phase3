from fastapi import status

from src.core.exceptions.utils import ErrorCode
from .base_exception import BaseAppException

class EntityNotFoundException(BaseAppException):

    def __init__(self, entity_name: str, **kwargs):
        super().__init__(
            message=f"{entity_name} not found.",
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCode.ENTITY_NOT_FOUND,
            **kwargs            
        )

__all__ = ["EntityNotFoundException"]