from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.payment.i_payment_service import IPaymentService
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.adapters.driven.repositories.payment_repository import PaymentRepository
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.adapters.driven.repositories.payment_method_repository import PaymentMethodRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository
from src.adapters.driven.repositories.payment_status_repository import PaymentStatusRepository
from src.application.services.payment_service import PaymentService
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import PaymentPermissions
from src.core.ports.payment.i_payment_gateway import IPaymentGateway
from src.adapters.driven.payment_providers.mercado_pago_gateway import MercadoPagoGateway
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.core.ports.order.i_order_repository import IOrderRepository



router = APIRouter()


def _get_payment_service(db_session: Session = Depends(get_db)) -> IPaymentService:
    payment_repository: IPaymentRepository = PaymentRepository(db_session)
    payment_method_repository: IPaymentMethodRepository = PaymentMethodRepository(db_session)
    payment_status_repository: IPaymentStatusRepository = PaymentStatusRepository(db_session)
    payment_gateway: IPaymentGateway = MercadoPagoGateway()
    order_repository: IOrderRepository = OrderRepository(db_session)
    order_status_repository: IOrderStatusRepository = OrderStatusRepository(db_session)

    return PaymentService(
        payment_gateway,
        payment_repository,
        payment_status_repository,
        payment_method_repository,
        order_repository,
        order_status_repository
    )

# Criar pagamento para o pedido
@router.post(
    "/payments/{order_id}",
    dependencies=[Security(get_current_user, scopes=[PaymentPermissions.CAN_CREATE_PAYMENT])],
    status_code=status.HTTP_201_CREATED,
)
async def create_payment(
    order_id: int,
    payment_method: str,
    current_user: dict = Depends(get_current_user),
    service: IPaymentService = Depends(_get_payment_service),
):
    return service.process_payment(order_id, payment_method, current_user)