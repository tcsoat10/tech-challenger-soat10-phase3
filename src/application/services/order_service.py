from typing import List, Optional
from src.core.ports.payment_method.i_payment_method_repository import IPaymentMethodRepository
from src.constants.product_category import ProductCategoryEnum
from src.core.domain.dtos.product.product_dto import ProductDTO
from src.core.ports.product.i_product_repository import IProductRepository
from src.constants.order_status import OrderStatusEnum
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.bad_request_exception import BadRequestException
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.domain.entities.order import Order
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order.i_order_service import IOrderService
from src.core.ports.payment.i_payment_service import IPaymentService
from src.application.services.payment_service import PaymentService


class OrderService(IOrderService):

    def __init__(
        self,
        repository: IOrderRepository,
        order_status_repository: IOrderStatusRepository,
        customer_repository: ICustomerRepository,
        employee_repository:IEmployeeRepository,
        product_repository: IProductRepository,
        payment_method_repository: IPaymentMethodRepository,
        payment_service: IPaymentService
    ):
        self.order_repository = repository
        self.order_status_repository = order_status_repository
        self.customer_repository = customer_repository
        self.employee_repository = employee_repository
        self.product_repository = product_repository
        self.payment_method_repository = payment_method_repository
        self.payment_service = payment_service

    def create_order(self, current_user: dict) -> OrderDTO:
        open_statuses = [
            OrderStatusEnum.ORDER_PENDING.status,
            OrderStatusEnum.ORDER_WAITING_BURGERS.status,
            OrderStatusEnum.ORDER_WAITING_SIDES.status,
            OrderStatusEnum.ORDER_WAITING_DRINKS.status,
            OrderStatusEnum.ORDER_WAITING_DESSERTS.status,
            OrderStatusEnum.ORDER_PLACED.status,
            OrderStatusEnum.ORDER_PAID.status,
            OrderStatusEnum.ORDER_PREPARING.status,
            OrderStatusEnum.ORDER_READY.status
        ]

        open_orders = self.order_repository.get_all(status=open_statuses, customer_id=int(current_user['person']['id']))
        if open_orders:
            raise BadRequestException("Já existe um pedido em aberto para este cliente")

        order_status = self.order_status_repository.get_by_status(OrderStatusEnum.ORDER_PENDING.status)
        if not order_status:
            raise EntityNotFoundException(entity_name="OrderStatus")

        customer = self.customer_repository.get_by_id(int(current_user['person']['id']))
        if not customer:
            raise EntityNotFoundException(entity_name="Customer")

        order = Order(
            customer=customer,
            order_status=order_status
        )
        order = self.order_repository.create(order)
        return OrderDTO.from_entity(order)
    
    def list_products_by_order_status(self, order_id: int, current_user: dict) -> List[ProductDTO]:
        order = self._get_order(order_id, current_user)

        order_status_to_category = {
            OrderStatusEnum.ORDER_WAITING_BURGERS.status: ProductCategoryEnum.BURGERS.name,
            OrderStatusEnum.ORDER_WAITING_SIDES.status: ProductCategoryEnum.SIDES.name,
            OrderStatusEnum.ORDER_WAITING_DRINKS.status: ProductCategoryEnum.DRINKS.name,
            OrderStatusEnum.ORDER_WAITING_DESSERTS.status: ProductCategoryEnum.DESSERTS.name,
        }
        
        if order.order_status.status not in order_status_to_category:
            raise BadRequestException("Não existem produtos disponíveis para este status de pedido.")

        products = self.product_repository.get_all(categories=[order_status_to_category[order.order_status.status]])
        return [ProductDTO.from_entity(product) for product in products]

    def get_order_by_id(self, order_id: int, current_user: dict) -> OrderDTO:
        order = self._get_order(order_id, current_user)
        return OrderDTO.from_entity(order)

    def add_item(self, order_id: int, order_item_dto: CreateOrderItemDTO, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)
        product = self.product_repository.get_by_id(order_item_dto.product_id)
        if not product:
            raise EntityNotFoundException(f"Product ID '{order_item_dto.product_id}'")
        
        order_item = OrderItem(
            order=order,
            product=product,
            quantity=order_item_dto.quantity,
            observation=order_item_dto.observation
        )
        order.add_item(order_item)
        
        # Agrupar itens
        # existing_item = next((order_item for order_item in order.order_items if order_item.product_id == order_item_dto.product_id), None)
        # if existing_item:
        #     order.change_item_quantity(existing_item, existing_item.quantity + order_item_dto.quantity) # Adiciona a quantidade ao item existente
        #     order.change_item_observation(existing_item, order_item_dto.observation) # Substitui a observação anterior pela nova
        # else:
        #     # Adiciona um novo item ao pedido
        #     order_item = OrderItem(
        #         order=order,
        #         product=product,
        #         quantity=order_item_dto.quantity,
        #         observation=order_item_dto.observation
        #     )
        #     order.add_item(order_item)

        self.order_repository.update(order)

    def remove_item(self, order_id: int, order_item_id: int, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)
        item = self._get_item_from_order(order, order_item_id)
        order.remove_item(item)
        self.order_repository.update(order)

    def change_item_quantity(self, order_id: int, item_id: int, new_quantity: int, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)
        item = self._get_item_from_order(order, item_id)
        order.change_item_quantity(item, new_quantity)
        self.order_repository.update(order)

    def change_item_observation(self, order_id: int, order_item_id: int, new_observation: str, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)
        item = self._get_item_from_order(order, order_item_id)
        order.change_item_observation(item, new_observation)
        self.order_repository.update(order)

    def clear_order(self, order_id: int, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)
        order.clear_order(self.order_status_repository)
        self.order_repository.update(order)

    def list_order_items(self, order_id: int, current_user: dict) -> List[OrderItemDTO]:
        order = self._get_order(order_id, current_user)
        return [OrderItemDTO.from_entity(item) for item in order.list_order_items()]

    def cancel_order(self, order_id: int, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)
        order.cancel_order(self.order_status_repository)
        order.soft_delete()
        self.order_repository.update(order)

    
    def process_payment(self, order_id: int, method_payment: str, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)
        payment_method = self.payment_method_repository.get_by_name(method_payment)
        if not payment_method:
            raise EntityNotFoundException(message="Não foi possível encontrar o método de pagamento informado.")

        order.process_payment(self.payment_service, payment_method.id)
        self.order_repository

    def next_step(self, order_id: int, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)

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
        employee = self.employee_repository.get_by_id(employee_id)
        order.next_step(self.order_status_repository, employee=employee)
        self.order_repository.update(order)

    def go_back(self, order_id: int, current_user: dict) -> None:
        order = self._get_order(order_id, current_user)
        order.go_back(self.order_status_repository)
        self.order_repository.update(order)

    def list_orders(self, current_user: dict, status: Optional[List[str]] = None) -> List[OrderDTO]:
        if current_user['profile']['name'] == 'customer':
            customer_id = int(current_user['person']['id'])
            orders = self.order_repository.get_all(status=status, customer_id=customer_id)
        else:
            orders = self.order_repository.get_all(status=status)

        return [OrderDTO.from_entity(order) for order in orders]

    def _get_order(self, order_id: int, current_user: dict) -> Order:
        order = self.order_repository.get_by_id(order_id)
        if not order:
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")

        if current_user['profile']['name'] in ['customer', 'anonymous'] and order.id_customer != int(current_user['person']['id']):
            raise EntityNotFoundException(message=f"O pedido com ID '{order_id}' não foi encontrado.")
        
        return order

    def _get_item_from_order(self, order: Order, item_id: int) -> OrderItem:
        order_item = next((order_item for order_item in order.order_items if order_item.id == item_id), None)
        if not order_item:
            raise EntityNotFoundException(message=f"O item com ID '{item_id}' não foi encontrado no pedido.")
        return order_item

__all__ = ["OrderService"]
