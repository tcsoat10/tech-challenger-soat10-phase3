
from sqlalchemy.orm import Session

from src.core.domain.dtos.payment_method.payment_method_dto import PaymentMethodDTO
from src.adapters.driven.repositories.payment_method_repository import PaymentMethodRepository
from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.application.usecases.payment_method_usecase.create_payment_method_usecase import CreatePaymentMethodUseCase
from src.core.domain.dtos.payment_method.create_payment_method_dto import CreatePaymentMethodDTO
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository


class PaymentMethodController:
    
    def __init__(self, db_connection: Session):
        self.payment_method_gateway: IPaymentMethodRepository = PaymentMethodRepository(db_connection)

    def create_payment_method(self, dto: CreatePaymentMethodDTO) -> PaymentMethodDTO:
        create_payment_method_use_case = CreatePaymentMethodUseCase.build(self.payment_method_gateway)
        payment_method = create_payment_method_use_case.execute(dto)
        return DTOPresenter.transform(payment_method, PaymentMethodDTO)
        