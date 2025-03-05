from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.adapters.driven.repositories.order_repository import OrderRepository
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.adapters.driven.repositories.payment_repository import PaymentRepository
from src.adapters.driver.api.v1.decorators.bypass_auth import bypass_auth
from src.adapters.driven.payment_providers.mercado_pago_gateway import MercadoPagoGateway
from src.adapters.driven.repositories.payment_method_repository import PaymentMethodRepository
from src.adapters.driven.repositories.payment_status_repository import PaymentStatusRepository
from config.database import get_db
from src.core.ports.payment.i_payment_provider_gateway import IPaymentProviderGateway
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.payment_status.i_payment_status_repository import IPaymentStatusRepository
from src.application.services.payment_service import PaymentService
from src.core.ports.payment.i_payment_repository import IPaymentRepository

from src.core.ports.payment.i_payment_service import IPaymentService


router = APIRouter()


def _get_payment_service(db_session: Session = Depends(get_db)) -> IPaymentService:
    repository: IPaymentRepository = PaymentRepository(db_session)
    payment_method_repository: IPaymentMethodRepository = PaymentMethodRepository(db_session)
    payment_status_repository: IPaymentStatusRepository = PaymentStatusRepository(db_session)
    payment_gateway: IPaymentProviderGateway = MercadoPagoGateway()
    order_repository: IOrderRepository = OrderRepository(db_session)
    order_status_repository: IOrderStatusRepository = OrderStatusRepository(db_session)

    return PaymentService(
        gateway=payment_gateway,
        repository=repository,
        payment_method_repository=payment_method_repository,
        payment_status_repository=payment_status_repository,
        order_repository=order_repository,
        order_status_repository=order_status_repository,
    )

@router.post("/webhook/payment", include_in_schema=False)
@bypass_auth()
async def webhook(request: Request, payment_service: IPaymentService = Depends(_get_payment_service)):
    """
    Endpoint para processar webhooks enviados pelo payment provider.
    """
    try:
        payload = await request.json()

        payment_service.handle_webhook(payload)
        return JSONResponse(content={"message": "Webhook processado com sucesso!"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar webhook: {str(e)}")
