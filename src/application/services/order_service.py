from datetime import datetime
from typing import List
from config.database import DELETE_MODE
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.domain.dtos.order.update_order_dto import UpdateOrderDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.domain.dtos.order.create_order_dto import CreateOrderDTO
from src.core.domain.entities.order import Order
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order.i_order_service import IOrderService


class OrderService(IOrderService):

    def __init__(self, repository: IOrderRepository, order_status_repository: IOrderStatusRepository, customer_repository: ICustomerRepository, employee_repository:IEmployeeRepository):
        self.repository = repository
        self.order_status_repository = order_status_repository
        self.customer_repository = customer_repository
        self.employee_repository = employee_repository
    
    def create_order(self, dto: CreateOrderDTO) -> OrderDTO:
        order_status = self.order_status_repository.get_by_id(dto.id_order_status)
        if not order_status:
            raise EntityNotFoundException(entity_name="OrderStatus")
        
        customer = self.customer_repository.get_by_id(dto.id_customer)
        if not customer:
            raise EntityNotFoundException(entity_name="Customer")
        #TODO incluir employee
        
        order = Order(id_customer=dto.id_customer, id_employee=dto.id_employee, id_order_status=dto.id_order_status)
        order = self.repository.create(order)
        return OrderDTO.from_entity(order)
    
    def get_order_by_customer_id(self, id_customer: int) -> List[OrderDTO]:
        orders = self.repository.get_by_customer_id(id_customer=id_customer)
        if not orders:
            raise EntityNotFoundException(entity_name="Order")
        return [OrderDTO.from_entity(order) for order in orders]
    
    def get_order_by_employee_id(self, id_employee: int) -> List[OrderDTO]:
        orders = self.repository.get_by_employee_id(id_employee=id_employee)
        if not orders:
            raise EntityNotFoundException(entity_name="Order")
        return [OrderDTO.from_entity(order)for order in orders]

    def get_order_by_id(self, order_id: int) -> OrderDTO:
        order = self.repository.get_by_id(order_id=order_id)
        if not order:
            raise EntityNotFoundException(entity_name="Order")
        return OrderDTO.from_entity(order)

    def get_all_orders(self) -> List[OrderDTO]:
        orders = self.repository.get_all()
        return [OrderDTO.from_entity(order) for order in orders]

    def update_order(self, order_id: int, dto: UpdateOrderDTO) -> OrderDTO:
        order = self.repository.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException(entity_name="Order")

        order.id_customer = dto.id_customer
        order.id_employee = dto.id_employee
        order.id_order_status = dto.id_order_status
        updated_order = self.repository.update(order)
        return OrderDTO.from_entity(updated_order)

    def delete_order(self, order_id: int) -> OrderDTO:
        order = self.repository.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException(entity_name="Order")

        if DELETE_MODE == 'soft':
            if order.is_deleted():
                raise EntityNotFoundException(entity_name="Order")

            order.soft_delete()
            self.repository.update(order)
        else:
            self.repository.delete(order)

__all__ = ["OrderService"]
