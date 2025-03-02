from typing import Optional
from config.database import DELETE_MODE
from src.core.exceptions.entity_duplicated_exception import EntityDuplicatedException
from src.core.domain.dtos.payment_method.payment_method_dto import PaymentMethodDTO
from src.core.domain.dtos.payment_method.update_payment_method_dto import UpdatePaymentMethodDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.core.ports.payment_method.i_payment_method_service import IPaymentMethodService


class PaymentMethodService(IPaymentMethodService):
    def __init__(self, payment_method_repository: IPaymentMethodRepository):
        self.repository = payment_method_repository

    def delete_payment_method(self, payment_method_id):
        payment_method = self.repository.get_by_id(payment_method_id)
        
        if not payment_method:
            raise EntityNotFoundException(entity_name='Payment method')
        
        if DELETE_MODE == 'soft':
            if payment_method.is_deleted():
                raise EntityNotFoundException(entity_name="Payment method")

            payment_method.soft_delete()
            self.repository.update(payment_method)
        else:
            self.repository.delete(payment_method)