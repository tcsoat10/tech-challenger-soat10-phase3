
from typing import List, Optional
from sqlalchemy.orm import Session

from src.application.usecases.order_status_usecase.update_order_stauts_usecase import UpdateOrderStatusUseCase
from src.core.domain.dtos.order_status.update_order_status_dto import UpdateOrderStatusDTO
from src.application.usecases.order_status_usecase.get_all_order_status_usecase import GetAllOrderStatusUseCase
from src.application.usecases.order_status_usecase.get_order_status_by_id_usecase import GetOrderStatusByIdUseCase
from src.application.usecases.order_status_usecase.get_order_status_by_status_usecase import GetOrderStatusByStatusUseCase
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.application.usecases.order_status_usecase.create_order_status_usecase import CreateOrderStatusUseCase
from src.core.domain.dtos.order_status.create_order_status_dto import CreateOrderStatusDTO
from src.core.domain.dtos.order_status.order_status_dto import OrderStatusDTO
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository


class OrderStatusController: 
    
    def __init__(self, db_session: Session):
        self.order_status_gateway: IOrderStatusRepository = OrderStatusRepository(db_session)
        
    def create_order_status(self, dto: CreateOrderStatusDTO) -> OrderStatusDTO:
        create_order_status_use_case = CreateOrderStatusUseCase.build(self.order_status_gateway)
        order_status = create_order_status_use_case.execute(dto)
        return DTOPresenter.transform(order_status, OrderStatusDTO)

    def get_order_status_by_status(self, status: str) -> OrderStatusDTO:
        get_order_status_by_status_use_case = GetOrderStatusByStatusUseCase.build(self.order_status_gateway)
        order_status = get_order_status_by_status_use_case.execute(status)
        return DTOPresenter.transform(order_status, OrderStatusDTO)
    
    def get_order_status_by_id(self, order_status_id: int) -> OrderStatusDTO:
        get_order_status_by_id_use_case = GetOrderStatusByIdUseCase.build(self.order_status_gateway)
        order_status = get_order_status_by_id_use_case.execute(order_status_id)
        return DTOPresenter.transform(order_status, OrderStatusDTO)

    def get_all_orders_status(self, include_deleted: Optional[bool] = False) -> List[OrderStatusDTO]:
        get_all_order_status_use_case = GetAllOrderStatusUseCase.build(self.order_status_gateway)
        order_status = get_all_order_status_use_case.execute(include_deleted=include_deleted)
        return DTOPresenter.transform_list(order_status, OrderStatusDTO)

    def update_order_status(self, order_status_id: int, dto: UpdateOrderStatusDTO) -> OrderStatusDTO:
        update_order_status_use_case = UpdateOrderStatusUseCase.build(self.order_status_gateway)
        order_status = update_order_status_use_case.execute(order_status_id, dto)
        return DTOPresenter.transform(order_status, OrderStatusDTO)
