from pydantic import BaseModel, ConfigDict, Field


class CreateOrderPaymentDTO(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')

    order_id: int = Field(..., gt=0)
    payment_id: int = Field(..., gt=0)