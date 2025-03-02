
from typing import List
from sqlalchemy.orm import Session

from src.application.usecases.payment_status_usecase.get_all_payment_status_usecase import GetAllPaymentStatusUsecase
from src.application.usecases.payment_status_usecase.get_payment_status_by_id_usecase import GetPaymentStatusByIdUseCase
from src.application.usecases.payment_status_usecase.get_payment_status_by_name_usecase import GetPaymentStatusByNameUseCase
from src.adapters.driven.repositories.payment_status_repository import PaymentStatusRepository
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.payment_status_usecase.create_payment_status_usecase import CreatePaymentStatusUseCase
from src.core.domain.dtos.payment_status.create_payment_status_dto import CreatePaymentStatusDTO
from src.core.domain.dtos.payment_status.payment_status_dto import PaymentStatusDTO
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository


class PaymentStatusController:
    
    def __init__(self, db_session: Session):
        self.payment_status_gateway: IPaymentStatusRepository = PaymentStatusRepository(db_session)

    def create_payment_status(self, dto: CreatePaymentStatusDTO) -> PaymentStatusDTO:
        create_payment_status_use_case = CreatePaymentStatusUseCase.build(self.payment_status_gateway)
        payment_status = create_payment_status_use_case.execute(dto)
        return DTOPresenter.transform(payment_status, PaymentStatusDTO)
    
    def get_payment_status_by_name(self, name: str) -> PaymentStatusDTO:
        get_payment_status_by_name_use_case = GetPaymentStatusByNameUseCase.build(self.payment_status_gateway)
        payment_status = get_payment_status_by_name_use_case.execute(name)
        return DTOPresenter.transform(payment_status, PaymentStatusDTO)
    
    def get_payment_status_by_id(self, payment_status_id: int) -> PaymentStatusDTO:
        get_payment_status_by_id_use_case = GetPaymentStatusByIdUseCase.build(self.payment_status_gateway)
        payment_status = get_payment_status_by_id_use_case.execute(payment_status_id)
        return DTOPresenter.transform(payment_status, PaymentStatusDTO)

    def get_all_payment_status(self, include_deleted: bool = False) -> List[PaymentStatusDTO]:
        get_all_payment_status_use_case = GetAllPaymentStatusUsecase.build(self.payment_status_gateway)
        payment_statuses = get_all_payment_status_use_case.execute(include_deleted)
        return DTOPresenter.transform_list(payment_statuses, PaymentStatusDTO)
