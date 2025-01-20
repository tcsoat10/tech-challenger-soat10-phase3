from typing import Optional
from fastapi import status

from src.core.exceptions.utils import ErrorCode
from .base_exception import BaseAppException

class EntityNotFoundException(BaseAppException):

    def __init__(self, entity_name: Optional[str] = None, message: Optional[str] = None, **kwargs):
        if not message:
            message = f"{entity_name} not found." if entity_name else "Entity not found."
        
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            error_code=ErrorCode.ENTITY_NOT_FOUND,
            **kwargs            
        )

__all__ = ["EntityNotFoundException"]