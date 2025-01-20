from pydantic import BaseModel, ConfigDict, Field


class UpdateOrderPaymentDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    id: int
    order_id: int = Field(..., gt=0)
    payment_id: int = Field(..., gt=0)