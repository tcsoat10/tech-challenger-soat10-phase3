from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from src.adapters.driver.api.v1.controllers.payment_controller import PaymentController
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
from src.core.ports.payment.i_payment_repository import IPaymentRepository


router = APIRouter()
    
def _get_payment_controller(db_session: Session = Depends(get_db)) -> PaymentController:
    payment_gateway: IPaymentRepository = PaymentRepository(db_session)
    payment_status_gateway: IPaymentStatusRepository = PaymentStatusRepository(db_session)
    payment_method_gateway: IPaymentMethodRepository = PaymentMethodRepository(db_session)
    order_gateway: IOrderRepository = OrderRepository(db_session)
    order_status_gateway: IOrderStatusRepository = OrderStatusRepository(db_session)
    payment_provider_gateway: IPaymentProviderGateway = MercadoPagoGateway()

    return PaymentController(
        payment_gateway=payment_gateway,
        payment_status_gateway=payment_status_gateway,
        payment_method_gateway=payment_method_gateway,
        order_gateway=order_gateway,
        order_status_gateway=order_status_gateway,
        payment_provider_gateway=payment_provider_gateway,
    )

@router.post("/webhook/payment", include_in_schema=False)
@bypass_auth()
async def webhook(request: Request, payment_controller: PaymentController = Depends(_get_payment_controller)):
    """
    Endpoint para processar webhooks enviados pelo payment provider.
    """
    try:
        payload = await request.json()

        payment_controller.payment_provider_webhook(payload)
        return JSONResponse(content={"message": "Webhook processado com sucesso!"}, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar webhook: {str(e)}")
