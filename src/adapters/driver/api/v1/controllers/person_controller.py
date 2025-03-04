from sqlalchemy.orm import Session

from src.core.ports.person.i_person_repository import IPersonRepository
from src.adapters.driven.repositories.person_repository import PersonRepository
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO
from src.core.domain.dtos.person.person_dto import PersonDTO
from src.application.usecases.person_usecase.create_person_usecase import CreatePersonUsecase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.person_usecase.get_person_by_cpf_usecase import GetPersonByCpfUsecase


class PersonController:
    def __init__(self, db_connection: Session):
        self.person_gateway: IPersonRepository = PersonRepository(db_connection)

    def create_person(self, dto: CreatePersonDTO) -> PersonDTO:
        create_person_usecase = CreatePersonUsecase.build(self.person_gateway)
        person = create_person_usecase.execute(dto)
        return DTOPresenter.transform(person, PersonDTO)
    
    def get_person_by_cpf(self, cpf: str) -> PersonDTO:
        person_by_cpf_usecase = GetPersonByCpfUsecase.build(self.person_gateway)
        person = person_by_cpf_usecase.execute(cpf)
        return DTOPresenter.transform(person, PersonDTO)