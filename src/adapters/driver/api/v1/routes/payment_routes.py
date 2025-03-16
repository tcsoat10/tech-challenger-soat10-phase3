from fastapi import APIRouter, Depends, status, Security
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.payment_controller import PaymentController
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import PaymentPermissions
from src.core.containers import Container


router = APIRouter()


# Criar pagamento para o pedido
@router.post(
    "/payments/{order_id}",
    dependencies=[Security(get_current_user, scopes=[PaymentPermissions.CAN_CREATE_PAYMENT])],
    status_code=status.HTTP_201_CREATED,
)
@inject
async def create_payment(
    order_id: int,
    payment_method: str,
    current_user: dict = Depends(get_current_user),
    controller: PaymentController = Depends(Provide[Container.payment_controller]),
):
    return controller.process_payment(order_id, payment_method, current_user)
