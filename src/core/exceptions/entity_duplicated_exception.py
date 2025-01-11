from fastapi import status

from src.core.exceptions.utils import ErrorCode
from .base_exception import BaseAppException

class EntityDuplicatedException(BaseAppException):

    def __init__(self, entity_name: str, **kwargs):
        super().__init__(
            message=f"{entity_name} already exists.",
            status_code=status.HTTP_409_CONFLICT,
            error_code=ErrorCode.DUPLICATED_ENTITY,
            **kwargs
        )

__all__ = ["EntityDuplicatedException"]
