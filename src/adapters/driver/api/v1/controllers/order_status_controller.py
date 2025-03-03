
from sqlalchemy.orm import Session

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
