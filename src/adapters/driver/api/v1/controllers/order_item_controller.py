
from sqlalchemy.orm import Session

from src.application.usecases.order_item_usecase.get_order_item_by_id import GetOrderItemByIdUseCase
from src.application.usecases.order_item_usecase.create_order_item_usecase import CreateOrderItemUseCase
from src.adapters.driven.repositories.order_item_repository import OrderItemRepository
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.adapters.driven.repositories.product_repository import ProductRepository
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository
from src.core.ports.product.i_product_repository import IProductRepository

class OrderItemController:
    def __init__(self, db_session: Session):
        self.order_item_gateway: IOrderItemRepository = OrderItemRepository(db_session)
        self.product_gateway: IProductRepository = ProductRepository(db_session)
        self.order_gateway: IOrderRepository = OrderRepository(db_session)
        
    def create_order_item(self, dto: CreateOrderItemDTO) -> OrderItemDTO:
        create_order_item_usecase = CreateOrderItemUseCase.build(self.order_item_gateway, self.product_gateway, self.order_gateway)
        order_item = create_order_item_usecase.execute(dto)
        return DTOPresenter.transform(order_item, OrderItemDTO)

    def get_order_item_by_id(self, order_item_id: int) -> OrderItemDTO:
        order_item_by_id = GetOrderItemByIdUseCase.build(self.order_item_gateway)
        order_item = order_item_by_id.execute(order_item_id)
        return DTOPresenter.transform(order_item, OrderItemDTO)
