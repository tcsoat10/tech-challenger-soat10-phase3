from pydantic import BaseModel

class CategoryDTO(BaseModel):
    id: int
    name: str
    description: str
