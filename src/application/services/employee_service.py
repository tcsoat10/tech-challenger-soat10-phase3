from src.core.domain.entities.person import Person
from src.core.ports.employee.i_employee_service import IEmployeeService
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.person.i_person_repository import IPersonRepository
from src.core.ports.role.i_role_repository import IRoleRepository
from src.core.ports.user.i_user_repository import IUserRepository
from src.core.domain.dtos.employee.employee_dto import EmployeeDTO
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.entities.employee import Employee
from src.core.domain.dtos.employee.update_employee_dto import UpdateEmployeeDTO
from config.database import DELETE_MODE

from typing import List


class EmployeeService(IEmployeeService):
    def __init__(
            self, repository: IEmployeeRepository,
            person_repository: IPersonRepository,
            role_repository: IRoleRepository,
            user_repository: IUserRepository
    ):
        self.repository = repository
        self.person_repository = person_repository
        self.role_repository = role_repository
        self.user_repository = user_repository
    
    def get_employee_by_id(self, employee_id: int) -> EmployeeDTO:
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise EntityNotFoundException(entity_name='Employee')
        return EmployeeDTO.from_entity(employee)
    
    def get_employee_by_person_id(self, person_id: int) -> EmployeeDTO:
        employee = self.repository.get_by_person_id(person_id)
        if not employee:
            raise EntityNotFoundException(entity_name='Employee')
        return EmployeeDTO.from_entity(employee)
    
    def get_employee_by_user_id(self, user_id: int) -> EmployeeDTO:
        employee = self.repository.get_by_user_id(user_id)
        if not employee:
            raise EntityNotFoundException(entity_name='Employee')
        return EmployeeDTO.from_entity(employee)
    
    def get_employees_by_role_id(self, role_id: int) -> List[EmployeeDTO]:
        employees = self.repository.get_by_role_id(role_id)
        return [EmployeeDTO.from_entity(employee) for employee in employees]
    
    def get_all_employees(self, include_deleted: bool = False) -> List[EmployeeDTO]:
        employees = self.repository.get_all(include_deleted=include_deleted)
        return [EmployeeDTO.from_entity(employee) for employee in employees]
    
    def update_employee(self, employee_id: int, dto: UpdateEmployeeDTO) -> EmployeeDTO:
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise EntityNotFoundException(entity_name='Employee')
        
        if employee.is_deleted():
            raise EntityNotFoundException(entity_name='Employee')
        
        person = self.person_repository.get_by_id(dto.person_id)
        if not person:
            raise EntityNotFoundException(entity_name='Person')
        
        role = self.role_repository.get_by_id(dto.role_id)
        if not role:
            raise EntityNotFoundException(entity_name='Role')
        
        user = self.user_repository.get_by_id(dto.user_id)
        if not user:
            raise EntityNotFoundException(entity_name='User')
        
        employee.person = person
        employee.role = role
        employee.user = user

        employee = self.repository.update(employee)

        return EmployeeDTO.from_entity(employee)
    
    def delete_employee(self, employee_id: int) -> None:
        employee = self.repository.get_by_id(employee_id)
        if not employee:
            raise EntityNotFoundException(entity_name='Employee')
        
        if DELETE_MODE == 'soft':
            if employee.is_deleted():
                raise EntityNotFoundException(entity_name='Employee')
            employee.soft_delete()
            self.repository.update(employee)
        else:
            self.repository.delete(employee_id)
            
    