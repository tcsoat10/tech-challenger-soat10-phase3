from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.orm import Session

from config.database import get_db
from src.adapters.driver.api.v1.controllers.payment_controller import PaymentController
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import PaymentPermissions


router = APIRouter()

def _get_payment_controller(db_session: Session = Depends(get_db)) -> PaymentController:
    return PaymentController(db_session)

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
