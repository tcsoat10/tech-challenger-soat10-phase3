from pydantic import BaseModel, ConfigDict, Field

class CreateOrderItemDTO(BaseModel):

    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    # order_id: int = Field(..., gt=0) # TODO: Add this field to the DTO
    product_id: int = Field(..., gt=0)
    quantity: float = Field(..., ge=0.0)
    observation: str = Field(..., min_length=3, max_length=300)

