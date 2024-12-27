from fastapi import status
from .base_exception import BaseAppException

class EntityNotFoundException(BaseAppException):

    def __init__(self, entity_name: str):
        super().__init__(message=f"{entity_name} not found.", status_code=status.HTTP_404_NOT_FOUND)

__all__ = ["EntityNotFoundException"]