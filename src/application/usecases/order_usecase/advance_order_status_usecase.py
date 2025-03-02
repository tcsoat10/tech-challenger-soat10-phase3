
from src.constants.order_status import OrderStatusEnum
from src.core.domain.entities.order import Order
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository


class AdvanceOrderStatusUseCase:
    def __init__(self, order_gateway: IOrderRepository, order_status_gateway: IOrderStatusRepository, employee_gateway: IEmployeeRepository):
        self.order_gateway = order_gateway
        self.order_status_gateway = order_status_gateway
        self.employee_gateway = employee_gateway
    
    @classmethod
    def build(cls, order_gateway: IOrderRepository, order_status_gateway: IOrderStatusRepository, employee_gateway: IEmployeeRepository):
        return cls(order_gateway, order_status_gateway, employee_gateway)
    
    def execute(self, order_id: int, current_user: dict) -> Order:
        order = self.order_gateway.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")
        
        if current_user['profile']['name'] in ['customer', 'anonymous'] and order.id_customer != int(current_user['person']['id']):
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")

        if order.order_status.status in [
            OrderStatusEnum.ORDER_PAID.status,
            OrderStatusEnum.ORDER_PREPARING.status,
            OrderStatusEnum.ORDER_READY.status,
        ] and current_user['profile']['name'] not in ['employee', 'manager']:
            raise BadRequestException("Você não tem permissão para avançar o pedido para o próximo passo.")

        if order.order_status.status in [
            OrderStatusEnum.ORDER_PENDING.status,
            OrderStatusEnum.ORDER_WAITING_BURGERS.status,
            OrderStatusEnum.ORDER_WAITING_SIDES.status,
            OrderStatusEnum.ORDER_WAITING_DRINKS.status,
            OrderStatusEnum.ORDER_WAITING_DESSERTS.status,
            OrderStatusEnum.ORDER_READY_TO_PLACE.status,
            OrderStatusEnum.ORDER_PLACED.status,
        ] and current_user['profile']['name'] not in ['customer', 'anonymous']:
            raise BadRequestException("Você não tem permissão para avançar o pedido para o próximo passo.")

        employee_id = int(current_user['person']['id']) if current_user['profile']['name'] in ['employee', 'manager'] else None
        employee = self.employee_gateway.get_by_id(employee_id)
        order.next_step(self.order_status_gateway, employee=employee)
        order = self.order_gateway.update(order)

        return order