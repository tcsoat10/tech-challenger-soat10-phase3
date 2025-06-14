
from src.constants.order_status import OrderStatusEnum
from src.core.domain.entities.order import Order
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository


class CreateOrderUseCase:
    
    def __init__(self, order_gateway: IOrderRepository, order_status_gateway: IOrderStatusRepository, customer_gateway: ICustomerRepository):
        self.order_gateway = order_gateway
        self.order_status_gateway = order_status_gateway
        self.customer_gateway = customer_gateway
        
    @classmethod
    def build(
        cls,
        order_gateway: IOrderRepository,
        order_status_gateway: IOrderStatusRepository,
        customer_gateway: ICustomerRepository
    ) -> 'CreateOrderUseCase':
        return cls(order_gateway, order_status_gateway, customer_gateway)
    
    def execute(self, current_user: dict) -> Order:
        """
        Creates a new order for the current user if no open orders exist.

        Args:
            current_user (dict): The current user's information.

        Returns:
            Order: The newly created order.

        Raises:
            BadRequestException: If there is already an open order for the customer.
            EntityNotFoundException: If the order status or customer is not found.
        """
        
        if 'person' not in current_user or 'id' not in current_user['person']:
            raise BadRequestException("Invalid current_user data: 'person' or 'id' key is missing")
        
        open_statuses = [
            OrderStatusEnum.ORDER_PENDING.status,
            OrderStatusEnum.ORDER_WAITING_BURGERS.status,
            OrderStatusEnum.ORDER_WAITING_SIDES.status,
            OrderStatusEnum.ORDER_WAITING_DRINKS.status,
            OrderStatusEnum.ORDER_WAITING_DESSERTS.status,
            OrderStatusEnum.ORDER_READY_TO_PLACE.status   
        ]
        
        open_orders = self.order_gateway.get_all(status=open_statuses, customer_id=int(current_user['person']['id']), include_deleted=False)
        if open_orders:
            raise BadRequestException("Já existe um pedido em aberto para este cliente")

        order_status = self.order_status_gateway.get_by_status(OrderStatusEnum.ORDER_PENDING.status)
        if not order_status:
            raise EntityNotFoundException(entity_name="OrderStatus")

        customer = self.customer_gateway.get_by_id(int(current_user['person']['id']))
        if not customer:
            raise EntityNotFoundException(entity_name="Customer")

        order = Order(
            customer=customer,
            order_status=order_status
        )
        
        created_order = self.order_gateway.create(order)
        return created_order
