from http import HTTPStatus
from .base_exception import BaseAppException

class EntityNotFoundException(BaseAppException):

    def __init__(self, entity_name: str):
        super().__init__(message=f"{entity_name} not found.", status_code=HTTPStatus.NOT_FOUND)

__all__ = ["EntityNotFoundException"]