from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.domain.entities.customer import Customer

from sqlalchemy.orm import Session
from typing import List


class CustomerRepository(ICustomerRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, customer: Customer) -> Customer:
        self.db_session.add(customer)
        self.db_session.commit()
        self.db_session.refresh(customer)
        return customer
    
    def get_by_id(self, customer_id: int) -> Customer:
        return self.db_session.query(Customer).filter(Customer.id == customer_id).first()
    
    def get_by_person_id(self, person_id: int) -> Customer:
        return self.db_session.query(Customer).filter(Customer.person_id == person_id).first()
    
    def get_all(self, include_deleted: bool = False) -> List[Customer]:
        query =  self.db_session.query(Customer)
        if not include_deleted:
            query = query.filter(Customer.inactivated_at.is_(None))
        return query.all()
    
    def update(self, customer: Customer) -> Customer:
        self.db_session.merge(customer)
        self.db_session.commit()
        return customer
    
    def delete(self, customer_id: int) -> None:
        customer = self.get_by_id(customer_id)
        if customer:
            self.db_session.delete(customer)
            self.db_session.commit()