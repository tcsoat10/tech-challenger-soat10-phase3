from abc import ABC, abstractmethod
from typing import List

from src.core.domain.dtos.employee.create_employee_dto import CreateEmployeeDTO
from src.core.domain.dtos.employee.employee_dto import EmployeeDTO
from src.core.domain.dtos.employee.update_employee_dto import UpdateEmployeeDTO


class IEmployeeService(ABC):

    @abstractmethod
    def delete_employee(self, employee_id: int) -> None:
        pass