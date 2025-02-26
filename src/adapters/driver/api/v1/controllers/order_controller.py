from typing import List
from sqlalchemy.orm import Session

from src.application.usecases.order_usecase.add_order_item_in_order_usecase import AddOrderItemInOrderUseCase
from src.application.usecases.order_usecase.get_order_by_id_usecase import GetOrderByIdUseCase
from src.application.usecases.order_usecase.list_products_by_order_status_usecase import ListProductsByOrderStatusUseCase
from src.core.domain.dtos.product.product_dto import ProductDTO
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.adapters.driven.repositories.product_repository import ProductRepository
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.order_usecase.create_order_usecase import CreateOrderUseCase
from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.product.i_product_repository import IProductRepository


class OrderController:

    def __init__(self, db_session: Session):
        self.customer_gateway: ICustomerRepository = CustomerRepository(db_session)
        self.order_status_gateway: IOrderStatusRepository = OrderStatusRepository(db_session)
        self.employee_gateway: IEmployeeRepository = EmployeeRepository(db_session)
        self.product_gateway: IProductRepository = ProductRepository(db_session)
        self.order_gateway: IOrderRepository = OrderRepository(db_session)
        
    def create_order(self, current_user: dict) -> OrderDTO:
        create_order_usecase = CreateOrderUseCase.build(self.order_gateway, self.order_status_gateway, self.customer_gateway)
        order = create_order_usecase.execute(current_user)
        return DTOPresenter.transform(order, OrderDTO)

    def list_products_by_order_status(self, order_id: int, current_user: dict) -> List[ProductDTO]:
        list_products_by_order_status_usecase = ListProductsByOrderStatusUseCase.build(self.order_gateway, self.product_gateway)
        products = list_products_by_order_status_usecase.execute(order_id, current_user)
        return DTOPresenter.transform_list(products, ProductDTO)

    def get_order_by_id(self, order_id: int, current_user: dict) -> OrderDTO:
        order_by_id_usecase = GetOrderByIdUseCase.build(self.order_gateway)
        order = order_by_id_usecase.execute(order_id, current_user)
        return DTOPresenter.transform(order, OrderDTO)

    def add_item(self, order_id: int, order_item_dto: dict, current_user: dict) -> OrderDTO:
        add_order_item_in_order_usecase = AddOrderItemInOrderUseCase.build(self.order_gateway, self.product_gateway)
        order = add_order_item_in_order_usecase.execute(order_id, order_item_dto, current_user)
        return DTOPresenter.transform(order, OrderDTO)
        
