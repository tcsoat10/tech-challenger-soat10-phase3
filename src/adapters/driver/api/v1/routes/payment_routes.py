from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.orm import Session

from src.adapters.driven.payment_providers.mercado_pago_gateway import MercadoPagoGateway
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.adapters.driven.repositories.payment_method_repository import PaymentMethodRepository
from src.adapters.driven.repositories.payment_repository import PaymentRepository
from src.adapters.driven.repositories.payment_status_repository import PaymentStatusRepository
from config.database import get_db
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository
from src.adapters.driver.api.v1.controllers.payment_controller import PaymentController
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import PaymentPermissions


router = APIRouter()

def _get_payment_controller(db_session: Session = Depends(get_db)) -> PaymentController:
    payment_provider_gateway: IPaymentProviderGateway = MercadoPagoGateway(db_session)
    payment_gateway: IPaymentRepository = PaymentRepository(db_session)
    payment_status_gateway: IPaymentStatusRepository = PaymentStatusRepository(db_session)
    payment_method_gateway: IPaymentMethodRepository = PaymentMethodRepository(db_session)
    order_gateway: IOrderRepository = OrderRepository(db_session)
    order_status_gateway: IOrderStatusRepository = OrderStatusRepository(db_session)

    return PaymentController(
        payment_provider_gateway,
        payment_gateway,
        payment_status_gateway,
        payment_method_gateway,
        order_gateway,
        order_status_gateway,
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
    controller: PaymentController = Depends(_get_payment_controller),
):
    return controller.process_payment(order_id, payment_method, current_user)
