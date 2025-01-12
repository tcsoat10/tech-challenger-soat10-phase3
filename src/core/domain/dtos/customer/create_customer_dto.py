from pydantic import BaseModel, ConfigDict, Field


class CreateCustomerDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    person_id: int = Field(..., gt=0)