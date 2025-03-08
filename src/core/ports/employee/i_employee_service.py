from abc import ABC, abstractmethod
from typing import List

from src.core.domain.dtos.employee.create_employee_dto import CreateEmployeeDTO
from src.core.domain.dtos.employee.employee_dto import EmployeeDTO
from src.core.domain.dtos.employee.update_employee_dto import UpdateEmployeeDTO


class IEmployeeService(ABC):

    @abstractmethod
    def get_all_employees(self, include_deleted: bool = False) -> List[EmployeeDTO]:
        pass
    
    @abstractmethod
    def update_employee(self, employee_id: int, dto: UpdateEmployeeDTO) -> EmployeeDTO:
        pass

    @abstractmethod
    def delete_employee(self, employee_id: int) -> None:
        pass