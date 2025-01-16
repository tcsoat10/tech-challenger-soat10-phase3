from typing import List
from src.core.domain.entities.product import Product
from src.core.domain.entities.order_item import OrderItem
from src.core.ports.order_item.i_order_item_repository import IOrderItemRepository
from sqlalchemy.orm import Session


class OrderItemRepository(IOrderItemRepository):
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create(self, order_item: OrderItem) -> OrderItem:
        self.db_session.add(order_item)
        self.db_session.commit()
        self.db_session.refresh(order_item)
        return order_item

    def get_by_order_id(self, order_id: int, include_deleted: bool = False) -> List[OrderItem]:
        query = self.db_session.query(OrderItem).filter(OrderItem.order_id == order_id)
        if not include_deleted:
            query = query.filter(OrderItem.inactivated_at.is_(None))
        return query.all()

    def get_by_product_name(self, order_id: int, product_name: str) -> OrderItem:
        return self.db_session.query(OrderItem).filter(
                OrderItem.order_id == order_id
            ).join(OrderItem.product).filter(
                Product.name == product_name
            ).first()

    def get_by_id(self, order_item_id: int) -> OrderItem:
        return self.db_session.query(OrderItem).filter(OrderItem.id == order_item_id).first()

    def get_all(self, include_deleted: bool = False) -> List[OrderItem]:
        query = self.db_session.query(OrderItem)
        if not include_deleted:
            query = query.filter(OrderItem.inactivated_at.is_(None))
        return query.all()
    
    def update(self, order_item: OrderItem) -> OrderItem:
        self.db_session.merge(order_item)
        self.db_session.commit()
        return order_item
    
    
    def delete(self, order_item: OrderItem) -> None:
        self.db_session.delete(order_item)
        self.db_session.commit()
