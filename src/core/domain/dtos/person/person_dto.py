from datetime import date
from pydantic import BaseModel, ConfigDict, Field
from src.core.domain.entities.person import Person


class PersonDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    cpf: str = Field(..., min_length=11, max_length=11)
    name: str = Field(..., min_length=3, max_length=200)
    email: str = Field(..., min_length=3, max_length=150)
    birth_date: date

    @classmethod
    def from_entity(cls, person: Person) -> "PersonDTO":
        return cls(
            id=person.id,
            cpf=person.cpf,
            name=person.name,
            email=person.email,
            birth_date=person.birth_date
        )
    

    


