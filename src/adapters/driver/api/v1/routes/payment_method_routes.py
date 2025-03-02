from fastapi import APIRouter, Depends, status, Security

from sqlalchemy.orm import Session
from config.database import get_db
from src.adapters.driver.api.v1.controllers.payment_method_controller import PaymentMethodController
from src.core.domain.dtos.payment_method.create_payment_method_dto import CreatePaymentMethodDTO
from src.core.domain.dtos.payment_method.payment_method_dto import PaymentMethodDTO
from src.core.domain.dtos.payment_method.update_payment_method_dto import UpdatePaymentMethodDTO
from src.constants.permissions import PaymentMethodPermissions
from src.core.auth.dependencies import get_current_user


router = APIRouter()


def _get_payment_method_controller(db_session: Session = Depends(get_db)) -> PaymentMethodController:
    return PaymentMethodController(db_session)

@router.post(
        "/payment-methods",
        response_model=PaymentMethodDTO,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_CREATE_PAYMENT_METHOD])]
)
def create_payment_method(
    dto: CreatePaymentMethodDTO,
    controller: PaymentMethodController = Depends(_get_payment_method_controller),
    user: dict = Security(get_current_user)
):
    return controller.create_payment_method(dto)

@router.get(
        "/payment-methods/{payment_method_name}/name",
        response_model=PaymentMethodDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_VIEW_PAYMENT_METHODS])]
)
def get_payment_method_by_name(
    payment_method_name: str,
    controller: PaymentMethodController = Depends(_get_payment_method_controller),
    user: dict = Security(get_current_user)
):
    return controller.get_payment_method_by_name(name=payment_method_name)

@router.get(
        "/payment-methods/{payment_method_id}/id",
        response_model=PaymentMethodDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_VIEW_PAYMENT_METHODS])]
)
def get_payment_method_by_id(
    payment_method_id: int,
    controller: PaymentMethodController = Depends(_get_payment_method_controller),
    user: dict = Security(get_current_user)
):
    return controller.get_payment_method_by_id(payment_method_id)

@router.get(
        "/payment-methods",
        response_model=list[PaymentMethodDTO],
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_VIEW_PAYMENT_METHODS])]
)
def get_all_payment_methods(
    include_deleted: bool = False,
    controller: PaymentMethodController = Depends(_get_payment_method_controller),
    user: dict = Security(get_current_user)
):
    return controller.get_all_payment_methods(include_deleted=include_deleted)

@router.put(
        "/payment-methods/{payment_method_id}",
        response_model=PaymentMethodDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_UPDATE_PAYMENT_METHOD])]
)
def update_payment_method(
    payment_method_id: int,
    dto: UpdatePaymentMethodDTO,
    controller: PaymentMethodController = Depends(_get_payment_method_controller),
    user: dict = Security(get_current_user)
):
    return controller.update_payment_method(payment_method_id, dto)

@router.delete(
        "/payment-methods/{payment_method_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Security(get_current_user, scopes=[PaymentMethodPermissions.CAN_DELETE_PAYMENT_METHOD])]
)
def delete_payment_method(
    payment_method_id: int,
    controller: PaymentMethodController = Depends(_get_payment_method_controller),
    user: dict = Security(get_current_user)
):
    return controller.delete_payment_method(payment_method_id)
