from http import HTTPStatus
from .base_exception import BaseAppException

class EntityDuplicatedException(BaseAppException):

    def __init__(self, entity_name: str):
        super().__init__(message=f"{entity_name} already exists.", status_code=HTTPStatus.CONFLICT)

__all__ = ["EntityDuplicatedException"]
