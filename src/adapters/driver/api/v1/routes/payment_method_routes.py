from fastapi import APIRouter, Depends, status, Security

from sqlalchemy.orm import Session
from config.database import get_db
from src.adapters.driven.repositories.payment_method_repository import PaymentMethodRepository
from src.application.services.payment_method_service import PaymentMethodService
from src.core.domain.dtos.payment_method.create_payment_method_dto import CreatePaymentMethodDTO
from src.core.domain.dtos.payment_method.payment_method_dto import PaymentMethodDTO
from src.core.domain.dtos.payment_method.update_payment_method_dto import UpdatePaymentMethodDTO
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.payment_method.i_payment_method_service import IPaymentMethodService
from src.constants.permissions import PaymentMethodPermissions
from src.core.auth.dependencies import get_current_user


router = APIRouter()

# Substituir por lib DI.
def _get_payment_method_service(db_session: Session = Depends(get_db)) -> IPaymentMethodService:
    repository: IPaymentMethodRepository = PaymentMethodRepository(db_session)
    return PaymentMethodService(repository)


@router.post(
        "/payment-methods",
        response_model=PaymentMethodDTO,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_CREATE_PAYMENT_METHOD])]
)
def create_payment_method(
    dto: CreatePaymentMethodDTO,
    service: IPaymentMethodService = Depends(_get_payment_method_service),
    user: dict = Security(get_current_user)
):
    return service.create_payment_method(dto)

@router.get(
        "/payment-methods/{payment_method_name}/name",
        response_model=PaymentMethodDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_VIEW_PAYMENT_METHODS])]
)
def get_payment_method_by_name(
    payment_method_name: str,
    service: IPaymentMethodService = Depends(_get_payment_method_service),
    user: dict = Security(get_current_user)
):
    return service.get_payment_method_by_name(name=payment_method_name)

@router.get(
        "/payment-methods/{payment_method_id}/id",
        response_model=PaymentMethodDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_VIEW_PAYMENT_METHODS])]
)
def get_payment_method_by_id(
    payment_method_id: int,
    service: IPaymentMethodService = Depends(_get_payment_method_service),
    user: dict = Security(get_current_user)
):
    return service.get_payment_method_by_id(payment_method_id)

@router.get(
        "/payment-methods",
        response_model=list[PaymentMethodDTO],
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_VIEW_PAYMENT_METHODS])]
)
def get_all_payment_methods(
    include_deleted: bool = False,
    service: IPaymentMethodService = Depends(_get_payment_method_service),
    user: dict = Security(get_current_user)
):
    return service.get_all_payment_methods(include_deleted=include_deleted)

@router.put(
        "/payment-methods/{payment_method_id}",
        response_model=PaymentMethodDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_UPDATE_PAYMENT_METHOD])]
)
def update_payment_method(
    payment_method_id: int,
    dto: UpdatePaymentMethodDTO,
    service: IPaymentMethodService = Depends(_get_payment_method_service),
    user: dict = Security(get_current_user)
):
    return service.update_payment_method(payment_method_id, dto)

@router.delete(
        "/payment-methods/{payment_method_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_DELETE_PAYMENT_METHOD])]
)
def delete_payment_method(
    payment_method_id: int,
    service: IPaymentMethodService = Depends(_get_payment_method_service),
    user: dict = Security(get_current_user)
):
    return service.delete_payment_method(payment_method_id)
