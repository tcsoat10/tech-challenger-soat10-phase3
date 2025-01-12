from pydantic import BaseModel, ConfigDict, Field


class UpdateCustomerDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    person_id: int = Field(..., gt=0)