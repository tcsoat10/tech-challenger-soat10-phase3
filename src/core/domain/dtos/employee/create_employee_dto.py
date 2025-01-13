from pydantic import BaseModel, ConfigDict, Field


class CreateEmployeeDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    person_id: int = Field(..., gt=0)
    role_id: int = Field(..., gt=0)
    user_id: int = Field(..., gt=0)
    