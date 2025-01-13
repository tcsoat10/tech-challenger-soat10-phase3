from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.domain.entities.employee import Employee

from sqlalchemy.orm import Session
from typing import List


class EmployeeRepository(IEmployeeRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, employee: Employee) -> Employee:
        self.db_session.add(employee)
        self.db_session.commit()
        self.db_session.refresh(employee)
        return employee
    
    def get_by_id(self, employee_id: int) -> Employee:
        return self.db_session.query(Employee).filter(Employee.id == employee_id).first()
    
    def get_by_person_id(self, person_id: int) -> Employee:
        return self.db_session.query(Employee).filter(Employee.person_id == person_id).first()
    
    def get_by_user_id(self, user_id: int) -> Employee:
        return self.db_session.query(Employee).filter(Employee.user_id == user_id).first()
    
    def get_by_role_id(self, role_id: int) -> List[Employee]:
        return self.db_session.query(Employee).filter(Employee.role_id == role_id).all()
    
    def get_all(self, include_deleted: bool = False) -> List[Employee]:
        query = self.db_session.query(Employee)
        if not include_deleted:
            query = query.filter(Employee.inactivated_at.is_(None))
        return query.all()
    
    def update(self, employee: Employee) -> Employee:
        self.db_session.merge(employee)
        self.db_session.commit()
        return employee
    
    def delete(self, employee_id: int) -> None:
        employee = self.get_by_id(employee_id)
        if employee:
            self.db_session.delete(employee)
            self.db_session.commit()
            