from typing import List
from src.core.domain.entities.employee import Employee
from src.core.domain.entities.customer import Customer
from src.core.domain.entities.order import Order
from src.core.ports.order.i_order_repository import IOrderRepository
from sqlalchemy.orm import Session

class OrderRepository(IOrderRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, order: Order) -> Order:
        self.db_session.add(order)
        self.db_session.commit()
        self.db_session.refresh(order)
        return order

    def get_by_customer_id(self, id_customer: int) -> List[Order]:
        return self.db_session.query(Order).join(Customer).filter(Customer.id == id_customer, Order.inactivated_at.is_(None)).all()
    
    def get_by_employee_id(self, id_employee: int) -> List[Order]:
        return self.db_session.query(Order).join(Employee).filter(Employee.id == id_employee, Order.inactivated_at.is_(None)).all()

    def get_by_id(self, order_id: int) -> Order:
        return self.db_session.query(Order).filter(Order.id == order_id).first()

    def get_all(self) -> List[Order]:
        return self.db_session.query(Order).filter(Order.inactivated_at.is_(None)).all()

    def update(self, order: Order) -> Order:
        self.db_session.merge(order)
        self.db_session.commit()
        return order

    def delete(self, order: Order) -> None:
        self.db_session.delete(order)
        self.db_session.commit()
