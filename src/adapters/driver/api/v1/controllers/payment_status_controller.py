
from sqlalchemy.orm import Session

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
