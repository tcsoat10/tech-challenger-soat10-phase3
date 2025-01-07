from typing import List, Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.database import get_db

from src.core.domain.dtos.payment_status.update_payment_status_dto import UpdatePaymentStatusDTO
from src.core.domain.dtos.payment_status.create_payment_status_dto import CreatePaymentStatusDTO
from src.core.domain.dtos.payment_status.payment_status_dto import PaymentStatusDTO
from src.core.ports.payment_status.i_payment_status_service import IPaymentStatusService
from src.application.services.payment_status_service import PaymentStatusService
from src.adapters.driven.repositories.payment_status_repository import PaymentStatusRepository


router = APIRouter()

def _get_payment_status_service(db_session: Session = Depends(get_db)) -> IPaymentStatusService:
    repository = PaymentStatusRepository(db_session)
    return PaymentStatusService(repository)

@router.post("/payment-status", response_model=PaymentStatusDTO, status_code=status.HTTP_201_CREATED)
def create_payment_status(dto: CreatePaymentStatusDTO, service: IPaymentStatusService = Depends(_get_payment_status_service)):
    return service.create_payment_status(dto)

@router.get("/payment-status/{payment_status_name}/name", response_model=PaymentStatusDTO, status_code=status.HTTP_200_OK)
def get_payment_status_by_name(payment_status_name: str, service: IPaymentStatusService = Depends(_get_payment_status_service)):
    return service.get_payment_status_by_name(name=payment_status_name)

@router.get("/payment-status/{payment_status_id}/id", response_model=PaymentStatusDTO, status_code=status.HTTP_200_OK)
def get_payment_status_by_id(payment_status_id: int, service: IPaymentStatusService = Depends(_get_payment_status_service)):
    return service.get_payment_status_by_id(payment_status_id=payment_status_id)

@router.get("/payment-status", response_model=List[PaymentStatusDTO])
def get_all_payment_status(include_deleted: Optional[bool] = False, service: IPaymentStatusService = Depends(_get_payment_status_service)):
    return service.get_all_payment_status(include_deleted=include_deleted)

@router.put("/payment-status/{payment_status_id}", response_model=PaymentStatusDTO)
def update_payment_status(payment_status_id: int, dto: UpdatePaymentStatusDTO, service: IPaymentStatusService = Depends(_get_payment_status_service)):
    return service.update_payment_status(payment_status_id, dto)

@router.delete("/payment-status/{payment_status_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment_status(payment_status_id: int, service: IPaymentStatusService = Depends(_get_payment_status_service)):
    service.delete_payment_status(payment_status_id=payment_status_id)
