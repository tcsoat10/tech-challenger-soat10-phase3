from pydantic import BaseModel
from src.core.domain.dtos.employee.employee_dto import EmployeeDTO
from src.core.domain.dtos.order_status.order_status_dto import OrderStatusDTO
from src.core.domain.dtos.customer.customer_dto import CustomerDTO
from src.core.domain.entities.order import Order

class OrderDTO(BaseModel):
    id: int
    customer: CustomerDTO
    order_status: OrderStatusDTO
    employee: EmployeeDTO

    @classmethod
    def from_entity(cls, order: Order) -> "OrderDTO":
        return cls(
                id = order.id,
                customer = CustomerDTO.from_entity(order.customer),
                order_status = OrderStatusDTO.from_entity(order.order_status),
                employee = EmployeeDTO.from_entity(order.employee)
        )