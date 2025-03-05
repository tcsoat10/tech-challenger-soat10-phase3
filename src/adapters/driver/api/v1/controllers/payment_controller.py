from sqlalchemy.orm import Session

from src.adapters.driver.api.v1.presenters.dto_presenter import DTOPresenter
from src.core.domain.dtos.payment.qr_code_payment_dto import QrCodePaymentDTO
from src.adapters.driven.payment_providers.mercado_pago_gateway import MercadoPagoGateway
from src.application.usecases.payment_usecase.process_payment_usecase import ProcessPaymentUseCase
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.adapters.driven.repositories.payment_method_repository import PaymentMethodRepository
from src.adapters.driven.repositories.payment_status_repository import PaymentStatusRepository
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository
from src.adapters.driven.repositories.payment_repository import PaymentRepository
from src.core.ports.payment.i_payment_repository import IPaymentRepository


class PaymentController:
    
    def __init__(self, db_session: Session):
        self.payment_provider_gateway: IPaymentProviderGateway = MercadoPagoGateway()
        self.payment_gateway: IPaymentRepository = PaymentRepository(db_session)
        self.payment_status_gateway: IPaymentStatusRepository = PaymentStatusRepository(db_session)
        self.payment_method_gateway: IPaymentMethodRepository = PaymentMethodRepository(db_session)
        self.order_gateway: IOrderRepository = OrderRepository(db_session)
        self.order_status_gateway: IOrderStatusRepository = OrderStatusRepository(db_session)
        
    def process_payment(self, order_id: int, method_payment: str, current_user: dict) -> QrCodePaymentDTO:
        process_payment_use_case = ProcessPaymentUseCase.build(
            payment_gateway=self.payment_gateway,
            payment_status_gateway=self.payment_status_gateway,
            payment_method_gateway=self.payment_method_gateway,
            order_gateway=self.order_gateway,
            order_status_gateway=self.order_status_gateway,
            payment_provider_gateway=self.payment_provider_gateway,
        )
        payment = process_payment_use_case.execute(order_id, method_payment, current_user)
        return DTOPresenter.transform_from_dict(payment, QrCodePaymentDTO)
