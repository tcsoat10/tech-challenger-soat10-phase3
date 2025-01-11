from abc import ABC, abstractmethod
from typing import List, Optional

from src.core.domain.dtos.person.update_person_dto import UpdatePersonDTO
from src.core.domain.dtos.person.person_dto import PersonDTO
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO


class IPersonService(ABC):

    @abstractmethod
    def create_person(self, dto: CreatePersonDTO) -> PersonDTO:
        pass

    @abstractmethod
    def get_person_by_cpf(self, cpf: str) -> PersonDTO:
        pass
    
    @abstractmethod
    def get_person_by_id(self, person_id: int) -> PersonDTO:
        pass

    @abstractmethod
    def get_all_persons(self, include_deleted: Optional[bool] = False) -> List[PersonDTO]:
        pass

    @abstractmethod
    def update_person(self, person_id: int, dto: UpdatePersonDTO) -> PersonDTO:
        pass

    @abstractmethod
    def delete_person(self, person_id: int, dto: UpdatePersonDTO) -> None:
        pass