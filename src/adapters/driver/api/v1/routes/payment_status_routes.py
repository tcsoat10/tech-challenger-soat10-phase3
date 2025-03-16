from typing import List, Optional
from fastapi import APIRouter, Depends, status, Security
from dependency_injector.wiring import inject, Provide

from src.adapters.driver.api.v1.controllers.payment_status_controller import PaymentStatusController
from src.core.domain.dtos.payment_status.update_payment_status_dto import UpdatePaymentStatusDTO
from src.core.domain.dtos.payment_status.create_payment_status_dto import CreatePaymentStatusDTO
from src.core.domain.dtos.payment_status.payment_status_dto import PaymentStatusDTO
from src.core.auth.dependencies import get_current_user
from src.constants.permissions import PaymentStatusPermissions
from src.core.containers import Container


router = APIRouter()


@router.post(
        "/payment-status",
        response_model=PaymentStatusDTO,
        status_code=status.HTTP_201_CREATED,
        dependencies=[Security(get_current_user, scopes=[PaymentStatusPermissions.CAN_CREATE_PAYMENT_STATUS])]
)
@inject
def create_payment_status(
    dto: CreatePaymentStatusDTO,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller]),
    user: dict = Security(get_current_user)
):
    return controller.create_payment_status(dto)

@router.get(
        "/payment-status/{payment_status_name}/name",
        response_model=PaymentStatusDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[PaymentStatusPermissions.CAN_VIEW_PAYMENT_STATUSES])]
)
@inject
def get_payment_status_by_name(
    payment_status_name: str,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_payment_status_by_name(name=payment_status_name)

@router.get(
        "/payment-status/{payment_status_id}/id",
        response_model=PaymentStatusDTO,
        status_code=status.HTTP_200_OK,
        dependencies=[Security(get_current_user, scopes=[PaymentStatusPermissions.CAN_VIEW_PAYMENT_STATUSES])]
)
@inject
def get_payment_status_by_id(
    payment_status_id: int,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_payment_status_by_id(payment_status_id=payment_status_id)

@router.get(
        "/payment-status",
        response_model=List[PaymentStatusDTO],
        dependencies=[Security(get_current_user, scopes=[PaymentStatusPermissions.CAN_VIEW_PAYMENT_STATUSES])]
)
@inject
def get_all_payment_status(
    include_deleted: Optional[bool] = False,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller]),
    user: dict = Security(get_current_user)
):
    return controller.get_all_payment_status(include_deleted=include_deleted)

@router.put(
        "/payment-status/{payment_status_id}",
        response_model=PaymentStatusDTO,
        dependencies=[Security(get_current_user, scopes=[PaymentStatusPermissions.CAN_UPDATE_PAYMENT_STATUS])]
)
@inject
def update_payment_status(
    payment_status_id: int,
    dto: UpdatePaymentStatusDTO,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller]),
    user: dict = Security(get_current_user)
):
    return controller.update_payment_status(payment_status_id, dto)

@router.delete(
        "/payment-status/{payment_status_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        dependencies=[Security(get_current_user, scopes=[PaymentStatusPermissions.CAN_DELETE_PAYMENT_STATUS])]
)
@inject
def delete_payment_status(
    payment_status_id: int,
    controller: PaymentStatusController = Depends(Provide[Container.payment_status_controller]),
    user: dict = Security(get_current_user)
):
    controller.delete_payment_status(payment_status_id=payment_status_id)
