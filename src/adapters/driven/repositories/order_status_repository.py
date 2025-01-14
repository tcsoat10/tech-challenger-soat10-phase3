from typing import List
from sqlalchemy.sql import exists
from sqlalchemy.orm import Session
from src.core.domain.entities.order_status import OrderStatus
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository

class OrderStatusRepository(IOrderStatusRepository):

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, order_status: OrderStatus) -> OrderStatus:
        self.db_session.add(order_status)
        self.db_session.commit()
        self.db_session.refresh(order_status)
        return order_status

    def exists_by_status(self, status: str) -> bool:
        return self.db_session.query(exists().where(OrderStatus.status == status)).scalar()

    def get_by_status(self, status: str) -> OrderStatus:
        return self.db_session.query(OrderStatus).filter(OrderStatus.status == status).first()

    def get_by_id(self, order_status_id: int) -> OrderStatus:
        return self.db_session.query(OrderStatus).filter(OrderStatus.id == order_status_id).first()

    def get_all(self, include_deleted: bool = False) -> List[OrderStatus]:
        query = self.db_session.query(OrderStatus)
        if not include_deleted:
            query = query.filter(OrderStatus.inactivated_at.is_(None))
        return query.all()

    def update(self, order_status: OrderStatus) -> OrderStatus:
        self.db_session.merge(order_status)
        self.db_session.commit()
        return order_status

    def delete(self, order_status: OrderStatus) -> None:
        self.db_session.delete(order_status)
        self.db_session.commit()
