
from typing import List
from src.core.domain.entities.order import Order
from src.core.ports.order.i_order_repository import IOrderRepository


class ListOrdersUseCase:
    
    def __init__(self, order_gateway: IOrderRepository):
        self.order_gateway = order_gateway
        
    @classmethod
    def build(cls, order_gateway: IOrderRepository):
        return cls(order_gateway)
        
    def execute(self, current_user: dict, status: List[str] = None) -> List[Order]:
        customer_id = int(current_user['person']['id']) if current_user['profile']['name'] == 'customer' else None
        orders = self.order_gateway.get_all(status=status, customer_id=customer_id)
        return orders
