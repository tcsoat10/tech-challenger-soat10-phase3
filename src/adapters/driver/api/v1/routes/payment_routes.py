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
from src.core.domain.dtos.payment.payment_dto import PaymentDTO
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import PaymentPermissions
from src.core.domain.dtos.payment.update_payment_dto import UpdatePaymentDTO
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


@router.get(
    '/payments/{payment_id}/id',
    response_model=PaymentDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PaymentPermissions.CAN_VIEW_PAYMENTS])]
)
def get_payment_by_id(
    payment_id: int,
    service: IPaymentService = Depends(_get_payment_service),
    user: dict = Security(get_current_user)
):
    return service.get_payment_by_id(payment_id)


@router.get(
    '/payments/{method_id}/method_id',
    response_model=List[PaymentDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PaymentPermissions.CAN_VIEW_PAYMENTS])]
)
def get_payments_by_method_id(
    method_id: int,
    service: IPaymentService = Depends(_get_payment_service),
    user: dict = Security(get_current_user)
):
    return service.get_payments_by_method_id(method_id)


@router.get(
    '/payments/{status_id}/status_id',
    response_model=List[PaymentDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PaymentPermissions.CAN_VIEW_PAYMENTS])]
)
def get_payments_by_status_id(
    status_id: int,
    service: IPaymentService = Depends(_get_payment_service),
    user: dict = Security(get_current_user)
):
    return service.get_payments_by_status_id(status_id)


@router.get(
    '/payments',
    response_model=List[PaymentDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PaymentPermissions.CAN_VIEW_PAYMENTS])]
)
def get_all_payments(
    include_deleted: bool = False,
    service: IPaymentService = Depends(_get_payment_service),
    user: dict = Security(get_current_user)
):
    return service.get_all_payments(include_deleted=include_deleted)


@router.put(
    '/payments/{payment_id}',
    response_model=PaymentDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[PaymentPermissions.CAN_UPDATE_PAYMENT])]
)
def update_payment(
    payment_id: int,
    dto: UpdatePaymentDTO,
    service: IPaymentService = Depends(_get_payment_service),
    user: dict = Security(get_current_user)
):
    return service.update_payment(payment_id, dto)


@router.delete(
    '/payments/{payment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Security(get_current_user, scopes=[PaymentPermissions.CAN_DELETE_PAYMENT])]
)
def delete_payment(
    payment_id: int,
    service: IPaymentService = Depends(_get_payment_service),
    user: dict = Security(get_current_user)
):
    return service.delete_payment(payment_id)

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