from fastapi import APIRouter, Depends, status, Security
from sqlalchemy.orm import Session
from typing import List

from config.database import get_db
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
from src.core.domain.dtos.payment.create_payment_dto import CreatePaymentDTO



router = APIRouter()


def _get_payment_service(db_session: Session = Depends(get_db)) -> IPaymentService:
    payment_repository: IPaymentRepository = PaymentRepository(db_session)
    payment_method_repository: IPaymentMethodRepository = PaymentMethodRepository(db_session)
    payment_status_repository: IPaymentStatusRepository = PaymentStatusRepository(db_session)
    return PaymentService(payment_repository, payment_method_repository, payment_status_repository)


@router.post(
    '/payments',
    response_model=PaymentDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[PaymentPermissions.CAN_CREATE_PAYMENT])]
)
def create_payment(
    dto: CreatePaymentDTO,
    service: IPaymentService = Depends(_get_payment_service),
    user: dict = Security(get_current_user)
):
    return service.create_payment(dto)


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