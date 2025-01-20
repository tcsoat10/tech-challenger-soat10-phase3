from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.orm import Session

from config.database import get_db
from src.core.ports.order_payment.i_order_payment_service import IOrderPaymentService
from src.core.ports.order_payment.i_order_payment_repository import IOrderPaymentRepository
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.payment.i_payment_repository import IPaymentRepository
from src.adapters.driven.repositories.order_payment_repository import OrderPaymentRepository
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.adapters.driven.repositories.payment_repository import PaymentRepository
from src.application.services.order_payment_service import OrderPaymentService
from src.core.domain.dtos.order_payment.order_payment_dto import OrderPaymentDTO
from src.constants.permissions import OrderPaymentPermissions
from src.core.auth.dependencies import get_current_user
from src.core.domain.dtos.order_payment.create_order_payment_dto import CreateOrderPaymentDTO


router = APIRouter()


def _get_order_payment_service(db_session: Session = Depends(get_db)) -> IOrderPaymentService:
    order_payment_repository: IOrderPaymentRepository = OrderPaymentRepository(db_session)
    order_repository: IOrderRepository = OrderRepository(db_session)
    payment_repository: IPaymentRepository = PaymentRepository(db_session)
    return OrderPaymentService(order_payment_repository, order_repository, payment_repository)


@router.post(
    '/order_payments',
    response_model=OrderPaymentDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[OrderPaymentPermissions.CAN_CREATE_ORDER_PAYMENT])]
)
def create_employee(
    dto: CreateOrderPaymentDTO,
    service: IOrderPaymentService = Depends(_get_order_payment_service),
    user: dict = Security(get_current_user)
):
    return service.create_order_payment(dto)


@router.get(
    '/order_payments/{order_payment_id}/id',
    response_model=OrderPaymentDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[OrderPaymentPermissions.CAN_VIEW_ORDER_PAYMENTS])]
)
def get_order_payment_by_id(
    order_payment_id: int,
    service: IOrderPaymentService = Depends(_get_order_payment_service),
    user: dict = Security(get_current_user)
):
    return service.get_order_payment_by_id(order_payment_id)


@router.get(
    '/order_payments/{order_id}/order_id',
    response_model=OrderPaymentDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[OrderPaymentPermissions.CAN_VIEW_ORDER_PAYMENTS])]
)
def get_order_payment_by_order_id(
    order_id: int,
    service: IOrderPaymentService = Depends(_get_order_payment_service),
    user: dict = Security(get_current_user)
):
    return service.get_order_payment_by_order_id(order_id)


@router.get(
    '/order_payments/{payment_id}/payment_id',
    response_model=OrderPaymentDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[OrderPaymentPermissions.CAN_VIEW_ORDER_PAYMENTS])]
)
def get_order_payment_by_payment_id(
    payment_id: int,
    service: IOrderPaymentService = Depends(_get_order_payment_service),
    user: dict = Security(get_current_user)
):
    return service.get_order_payment_by_payment_id(payment_id)