from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from config.database import get_db
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.domain.dtos.order.update_order_dto import UpdateOrderDTO
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.application.services.order_service import OrderService
from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.domain.dtos.order.create_order_dto import CreateOrderDTO
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order.i_order_service import IOrderService

router = APIRouter()

# Substituir por lib DI.
def _get_order_service(db_session: Session = Depends(get_db)) -> IOrderService:
    customer_repository: ICustomerRepository = CustomerRepository(db_session)
    order_status_repository: IOrderStatusRepository = OrderStatusRepository(db_session)
    employee_repository: IEmployeeRepository = EmployeeRepository(db_session)
    repository: IOrderRepository = OrderRepository(db_session)
    return OrderService(repository, customer_repository, order_status_repository, employee_repository)

@router.post("/order", response_model=OrderDTO, status_code=status.HTTP_201_CREATED)
def create_order(dto: CreateOrderDTO, service: IOrderService = Depends(_get_order_service)):
    return service.create_order(dto)

@router.get("/orders/{id_customer}/id_customer", response_model=List[OrderDTO], status_code=status.HTTP_200_OK)
def get_order_by_customer_id(id_customer: int, service: IOrderService = Depends(_get_order_service)):
    return service.get_order_by_customer_id(id_customer=id_customer)

@router.get("/orders/{id_employee}/id_employee", response_model=List[OrderDTO], status_code=status.HTTP_200_OK)
def get_order_by_employee_id(id_employee: int, service: IOrderService = Depends(_get_order_service)):
    return service.get_order_by_employee_id(id_employee=id_employee)

@router.get("/order/{order_id}/id", response_model=OrderDTO, status_code=status.HTTP_200_OK)
def get_order_by_id(order_id: int, service: IOrderService = Depends(_get_order_service)):
    return service.get_order_by_id(order_id=order_id)

@router.get("/orders", response_model=List[OrderDTO])
def get_all_orders(service: IOrderService = Depends(_get_order_service)):
    return service.get_all_orders()

@router.put("/order/{order_id}", response_model=OrderDTO)
def update_order(order_id: int, dto: UpdateOrderDTO, service: IOrderService = Depends(_get_order_service)):
    return service.update_order(order_id, dto)

@router.delete("/order/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(order_id: int, service: IOrderService = Depends(_get_order_service)):
    service.delete_order(order_id)
