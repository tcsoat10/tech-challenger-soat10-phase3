from abc import ABC, abstractmethod
from typing import List

from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.dtos.customer.customer_dto import CustomerDTO
from src.core.domain.dtos.customer.update_customer_dto import UpdateCustomerDTO



class ICustomerService(ABC):
    @abstractmethod
    def create_customer(self, dto: CreateCustomerDTO) -> CustomerDTO:
        pass
    
    @abstractmethod
    def get_customer_by_id(self, customer_id: int, current_user: dict) -> CustomerDTO:
        pass

    @abstractmethod
    def get_customer_by_person_id(self, customer_id: int, current_user: dict) -> CustomerDTO:
        pass

    @abstractmethod
    def get_all_customers(self, current_user: dict, include_deleted: bool = False) -> List[CustomerDTO]:
        pass

    @abstractmethod
    def update_customer(self, customer_id: int, dto: UpdateCustomerDTO, current_user: dict) -> CustomerDTO:
        pass

    @abstractmethod
    def delete_customer(self, customer_id: int, current_user: dict) -> None:
        pass