from datetime import datetime, timezone
from typing import List, Optional, Dict, Any
import uuid
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped

from src.constants.order_transition import PRODUCT_CATEGORY_TO_ORDER_STATUS, ORDER_STATUS_TRANSITIONS, ORDER_STATUSES_ALLOWING_REVERSAL_TRANSITIONS
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.constants.product_category import ProductCategoryEnum
from src.core.domain.entities.employee import Employee
from src.core.domain.entities.order_status import OrderStatus
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.bad_request_exception import BadRequestException
from src.constants.order_status import OrderStatusEnum
from .base_entity import BaseEntity


class Order(BaseEntity):
    __tablename__ = 'orders'

    id_customer = Column('id_customer', Integer, ForeignKey('customers.id'), nullable=False)
    customer = relationship('Customer')

    id_order_status = Column('id_order_status', Integer, ForeignKey('order_status.id'), nullable=False, default=1)
    order_status = relationship('OrderStatus')

    id_employee = Column('id_employee', Integer, ForeignKey('employees.id'), nullable=True)
    employee = relationship('Employee')

    id_payment = Column(ForeignKey('payments.id'), nullable=True)
    payment = relationship('Payment', back_populates='order')

    order_items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')

    status_history = relationship(
        'OrderStatusMovement',
        back_populates='order',
        cascade='all, delete-orphan',
        order_by='OrderStatusMovement.changed_at',
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        initial_status = OrderStatusMovement(
            order=self,
            old_status=None,
            new_status=OrderStatusEnum.ORDER_PENDING.status,
            changed_at=datetime.now(timezone.utc),
            changed_by="System",
        )
        self.status_history.append(initial_status)

    @property
    def customer_name(self) -> Optional[str]:
        if self.customer and self.customer.person:
            return self.customer.person.name
        
        return None

    @property
    def employee_name(self) -> Optional[str]:
        if self.employee and self.employee.person:
            return self.employee.person.name
        
        return None

    @property
    def total(self) -> float:
        if not hasattr(self, "_total"):
            self._total = sum(item.total for item in self.order_items)
        return self._total

    @property
    def is_paid(self) -> bool:
        if self.payment:
            return self.payment.is_completed()
        return False


    def _validate_status(self, valid_statuses: List[OrderStatusEnum], action: str) -> None:
        '''
        Validates if the current status of the order is in the list of valid statuses.

        :param valid_statuses: List of valid statuses.
        '''
        if self.order_status.status not in [order_status.status for order_status in valid_statuses]:
            raise BadRequestException(f"O pedido não está em um estado válido para {action}.")

    def _validate_category_for_status(self, category_name: str) -> None:
        '''
        Validates if the category of the item is valid for the current status of the order.

        The correct order is:
        - Burgers
        - Sides
        - Drinks
        - Desserts

        :param category: The category of the item.
        '''
        expected_status = PRODUCT_CATEGORY_TO_ORDER_STATUS.get(category_name)
        if not expected_status:
            raise BadRequestException(f"Categoria inválida: {category_name}.")

        if self.order_status.status != expected_status.status:
            raise BadRequestException(
                f"Não é possível adicionar itens da categoria '{category_name}' no status atual "
                f"'{self.order_status.status}'."
            )
        
    def _sort_order_items(self) -> None:
        '''
        Sorts the order items based on the category sequence.

        The category sequence is defined in the `category_sequence`.
        '''
        category_sequence = [
            ProductCategoryEnum.BURGERS.name,
            ProductCategoryEnum.SIDES.name,
            ProductCategoryEnum.DRINKS.name,
            ProductCategoryEnum.DESSERTS.name,
        ]
        
        categorized_items = {category: [] for category in category_sequence}

        for item in self.order_items:
            category = item.product.category
            if category.name in categorized_items:
                categorized_items[category.name].append(item)
            else:
                raise BadRequestException(f"Item com categoria inválida: {item.product.name}")

        sorted_items = []
        for name in category_sequence:
            sorted_items.extend(categorized_items[name])

        self.order_items = sorted_items

    def _record_status_change(self, new_status: OrderStatus, changed_by: str) -> None:
        '''
        Records a status change in the status history.

        :param new_status: The new status of the order.
        :param changed_by: The name of the user who changed the status.
        '''

        order_snapshot = {
            "id": self.id,
            "id_customer": self.id_customer,
            "customer_name": self.customer_name,
            "id_employee": self.id_employee,
            "employee_name": self.employee_name,
            "total": self.total,
            "current_status": self.order_status.status,
            "is_paid": self.is_paid,
            "order_items": [
                {
                    "id": item.id,
                    "product_id": item.product_id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "unit_price": item.product.price,
                    "total": item.total,
                    "observation": item.observation,
                }
                for item in self.order_items
            ],
        }
        
        movement = OrderStatusMovement(
            order_snapshot=order_snapshot,
            old_status=self.order_status.status,
            new_status=new_status.status,
            changed_at=datetime.now(timezone.utc),
            changed_by=changed_by,
        )
        self.status_history.append(movement)

    def add_item(self, item: OrderItem) -> None:
        self._validate_status([*PRODUCT_CATEGORY_TO_ORDER_STATUS.values()], "adicionar itens")
        self._validate_category_for_status(item.product.category.name)

        self.order_items.append(item)
        self._sort_order_items()

    def remove_item(self, order_item: OrderItem) -> None:
        self._validate_status([*PRODUCT_CATEGORY_TO_ORDER_STATUS.values()], "remover itens")
        if order_item.quantity > 1:
            order_item.quantity -= 1
        else:    
            self.order_items.remove(order_item)

    def change_item_quantity(self, item: OrderItem, new_quantity: int) -> None:
        self._validate_status([*PRODUCT_CATEGORY_TO_ORDER_STATUS.values()], "alterar a quantidade de itens")

        if new_quantity <= 0:
            raise BadRequestException("A quantidade do item deve ser maior que zero.")

        item.quantity = new_quantity

    def change_item_observation(self, item: OrderItem, new_observation: str) -> None:
        self._validate_status([*PRODUCT_CATEGORY_TO_ORDER_STATUS.values()], "alterar a observação do item")
        item.observation = new_observation

    def clear_order(self, order_status_repository: IOrderStatusRepository) -> None:
        self._validate_status([*PRODUCT_CATEGORY_TO_ORDER_STATUS.values(), OrderStatusEnum.ORDER_READY_TO_PLACE], "limpar o pedido")
        self.order_items = []

        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_BURGERS.status)

    def list_order_items(self) -> List[OrderItem]:
        return self.order_items

    def cancel_order(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        self._validate_status(
            [
                OrderStatusEnum.ORDER_PENDING,
                *PRODUCT_CATEGORY_TO_ORDER_STATUS.values(),
                OrderStatusEnum.ORDER_READY_TO_PLACE,
                OrderStatusEnum.ORDER_PLACED
            ], "cancelar o pedido"
        )

        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_CANCELLED.status)
        owner = movement_owner or self.customer_name or "Cliente Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def set_status_waiting_burguer(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_PENDING.status, OrderStatusEnum.ORDER_WAITING_SIDES.status]:
            raise BadRequestException("Não é possível selecionar sanduíches neste momento.")
        
        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_BURGERS.status)

    def set_status_waiting_sides(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_WAITING_BURGERS.status, OrderStatusEnum.ORDER_WAITING_DRINKS.status]:
            raise BadRequestException("Não é possível selecionar acompanhamentos neste momento.")
        
        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_SIDES.status)

    def set_status_waiting_drinks(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_WAITING_SIDES.status, OrderStatusEnum.ORDER_WAITING_DESSERTS.status]:
            raise BadRequestException("Não é possível selecionar bebidas neste momento.")
        
        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_DRINKS.status)
    
    def set_status_waiting_desserts(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status not in [OrderStatusEnum.ORDER_WAITING_DRINKS.status, OrderStatusEnum.ORDER_READY_TO_PLACE.status]:
            raise BadRequestException("Não é possível selecionar sobremesas neste momento.")
        
        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_WAITING_DESSERTS.status)
    
    def set_status_ready_to_place(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_WAITING_DESSERTS.status:
            raise BadRequestException("Não é possível confirmar o pedido neste momento.")
        
        self.order_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_READY_TO_PLACE.status)

    def set_status_placed(
            self,
            order_status_repository: IOrderStatusRepository,
            movement_owner: Optional[str] = None,
        ) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_READY_TO_PLACE.status:
            raise BadRequestException("Não é possível finalizar o pedido neste momento.")

        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_PLACED.status)
        owner = movement_owner or self.customer_name or "Cliente Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def set_status_paid(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_PLACED.status:
            raise BadRequestException("Não é possível confirmar o pagamento neste momento.")
        
        if not self.is_paid:
            raise BadRequestException("O pedido ainda não foi pago. Não é possível avançar o status do pedido.")
        
        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_PAID.status)
        owner = "System"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def set_status_preparing(self, order_status_repository: IOrderStatusRepository, employee: Employee, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_PAID.status:
            raise BadRequestException("Não é possível preparar o pedido neste momento.")

        if not employee:
            raise BadRequestException("É necessário um funcionário para preparar o pedido.")
        
        self.id_employee = employee.id
        self.employee = employee

        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_PREPARING.status)
        owner = movement_owner or self.employee_name or "Funcionário Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def set_status_ready(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_PREPARING.status:
            raise BadRequestException("Não é possível finalizar o pedido neste momento.")
        
        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_READY.status)
        owner = movement_owner or self.employee_name or "Funcionário Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def set_status_completed(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        if self.order_status.status != OrderStatusEnum.ORDER_READY.status:
            raise BadRequestException("Não é possível completar o pedido neste momento.")
        
        new_status = order_status_repository.get_by_status(OrderStatusEnum.ORDER_COMPLETED.status)
        owner = movement_owner or self.employee_name or "Funcionário Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    
    def advance_order_status(
        self,
        order_status_repository: IOrderStatusRepository,
        movement_owner: Optional[str] = None,
        employee: Optional[Employee] = None,
    ) -> None:
        '''
        Advances the order to the next step based on the current status.

        :param movement_owner: The name of the user who is advancing the order.
        :param employee: The employee responsible for preparing the order. this parameter is required when the order is being prepared.
        '''

        current_status = OrderStatusEnum.from_status(self.order_status.status)

        if current_status not in ORDER_STATUS_TRANSITIONS:
            raise BadRequestException(f"O estado atual {current_status.status} não permite transições.")

        expected_next_status = ORDER_STATUS_TRANSITIONS[current_status]

        if expected_next_status == OrderStatusEnum.ORDER_WAITING_BURGERS:
            self.set_status_waiting_burguer(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_WAITING_SIDES:
            self.set_status_waiting_sides(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_WAITING_DRINKS:
            self.set_status_waiting_drinks(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_WAITING_DESSERTS:
            self.set_status_waiting_desserts(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_READY_TO_PLACE:
            self.set_status_ready_to_place(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_PLACED:
            self.set_status_placed(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_PAID:
            self.set_status_paid(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_PREPARING:
            self.set_status_preparing(order_status_repository, employee, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_READY:
            self.set_status_ready(order_status_repository, movement_owner)
        elif expected_next_status == OrderStatusEnum.ORDER_COMPLETED:
            self.set_status_completed(order_status_repository, movement_owner)
        else:
            raise BadRequestException(f"Status não suportado: {expected_next_status.status}")

    def revert_order_status(self, order_status_repository: IOrderStatusRepository, movement_owner: Optional[str] = None) -> None:
        '''
        Reverts the order to the previous status.
        
        This operation is only allowed for statuses:
        - ORDER_WAITING_SIDES
        - ORDER_WAITING_DRINKS
        - ORDER_WAITING_DESSERTS
        - ORDER_READY_TO_PLACE

        Raises:
        - BadRequestException: If the current status does not allow going back.
        - BadRequestException: If the previous status cannot be determined.
        '''

        current_status = OrderStatusEnum.from_status(self.order_status.status)
        if current_status not in ORDER_STATUSES_ALLOWING_REVERSAL_TRANSITIONS:
            raise BadRequestException(
                f"O status atual '{current_status.status}' não permite voltar."
            )

        previous_status = None
        for status, next_status in ORDER_STATUS_TRANSITIONS.items():
            if next_status == current_status:
                previous_status = status
                break

        if not previous_status:
            raise BadRequestException("Não foi possível determinar o status anterior.")

        if previous_status == OrderStatusEnum.ORDER_WAITING_BURGERS:
            self.set_status_waiting_burguer(order_status_repository, movement_owner)
        elif previous_status == OrderStatusEnum.ORDER_WAITING_SIDES:
            self.set_status_waiting_sides(order_status_repository, movement_owner)
        elif previous_status == OrderStatusEnum.ORDER_WAITING_DRINKS:
            self.set_status_waiting_drinks(order_status_repository, movement_owner)
        elif previous_status == OrderStatusEnum.ORDER_WAITING_DESSERTS:
            self.set_status_waiting_desserts(order_status_repository, movement_owner)
        elif previous_status == OrderStatusEnum.ORDER_READY_TO_PLACE:
            self.set_status_ready_to_place(order_status_repository, movement_owner)
        else:
            raise BadRequestException(f"Transição de status não suportada: {previous_status.status}")
        
    def validate_payment(self, current_user: dict) -> Dict[str, Any]:
        if self.id_customer != int(current_user["person"]["id"]):
            raise BadRequestException("Você não tem permissão para acessar este pedido.")
        
        if self.payment and (
            self.payment.is_pending() or self.payment.is_completed()
        ):
            return {
                "payment_id": self.payment.id,
                "transaction_id": self.payment.transaction_id,
                "qr_code_link": self.payment.qr_code
            }

        if self.order_status.status != OrderStatusEnum.ORDER_PLACED.status:
            raise BadRequestException("Não é possível processar o pagamento neste momento.")

    def prepare_payment_data(self, webhook_url: str) -> Dict[str, Any]:
        return {
            "external_reference": f"order-{self.id}-{uuid.uuid4()}",
            "notification_url": f"{webhook_url}/api/v1/webhook/payment",
            "total_amount": self.total,
            "items": [
                {
                    "category": order_item.product.category.name,
                    "title": order_item.product.name,
                    "description": order_item.product.description,
                    "quantity": order_item.quantity,
                    "unit_measure": "unit",
                    "unit_price": order_item.product.price,
                    "total_amount": order_item.total
                }
                for order_item in self.order_items
            ],
            "title": f"Compra do pedido {self.id}",
            "description": f"Compra do pedido {self.id}"
        }

class OrderStatusMovement(BaseEntity):
    __tablename__ = 'order_status_movements'

    id_order: Mapped[int] = Column(Integer, ForeignKey('orders.id'), nullable=False)
    order = relationship('Order', back_populates='status_history')

    order_snapshot: Mapped[dict] = Column(JSON, nullable=False, default=[])
    
    old_status: Mapped[Optional[str]] = Column(String(100), nullable=True)
    new_status: Mapped[str] = Column(String(100), nullable=False)

    changed_at: Mapped[datetime] = Column(
        DateTime(timezone=True), default=datetime.now(timezone.utc), nullable=False
    )
    changed_by: Mapped[str] = Column(String(300), nullable=True)

__all__ = ['Order', 'OrderStatusMovement']
