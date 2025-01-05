from fastapi import APIRouter, Depends, status

from sqlalchemy.orm import Session
from config.database import get_db
from src.adapters.driven.repositories.payment_method_repository import PaymentMethodRepository
from src.application.services.payment_method_service import PaymentMethodService
from src.core.domain.dtos.payment_method.create_payment_method_dto import CreatePaymentMethodDTO
from src.core.domain.dtos.payment_method.payment_method_dto import PaymentMethodDTO
from src.core.domain.dtos.payment_method.update_payment_method_dto import UpdatePaymentMethodDTO
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.payment_method.i_payment_method_service import IPaymentMethodService


router = APIRouter()

# Substituir por lib DI.
def _get_payment_method_service(db_session: Session = Depends(get_db)) -> IPaymentMethodService:
    repository: IPaymentMethodRepository = PaymentMethodRepository(db_session)
    return PaymentMethodService(repository)


@router.post("/payment-methods", response_model=PaymentMethodDTO, status_code=status.HTTP_201_CREATED)
def create_payment_method(dto: CreatePaymentMethodDTO, service: IPaymentMethodService = Depends(_get_payment_method_service)):
    return service.create_payment_method(dto)

@router.get("/payment-methods/{payment_method_name}/name", response_model=PaymentMethodDTO, status_code=status.HTTP_200_OK)
def get_payment_method_by_name(payment_method_name: str, service: IPaymentMethodService = Depends(_get_payment_method_service)):
    return service.get_payment_method_by_name(name=payment_method_name)

@router.get("/payment-methods/{payment_method_id}/id", response_model=PaymentMethodDTO, status_code=status.HTTP_200_OK)
def get_payment_method_by_id(payment_method_id: int, service: IPaymentMethodService = Depends(_get_payment_method_service)):
    return service.get_payment_method_by_id(payment_method_id)

@router.get("/payment-methods", response_model=list[PaymentMethodDTO], status_code=status.HTTP_200_OK)
def get_all_payment_methods(include_deleted: bool = False, service: IPaymentMethodService = Depends(_get_payment_method_service)):
    return service.get_all_payment_methods(include_deleted=include_deleted)

@router.put("/payment-methods/{payment_method_id}", response_model=PaymentMethodDTO, status_code=status.HTTP_200_OK)
def update_payment_method(payment_method_id: int, dto: UpdatePaymentMethodDTO, service: IPaymentMethodService = Depends(_get_payment_method_service)):
    return service.update_payment_method(payment_method_id, dto)

@router.delete("/payment-methods/{payment_method_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment_method(payment_method_id: int, service: IPaymentMethodService = Depends(_get_payment_method_service)):
    return service.delete_payment_method(payment_method_id)
