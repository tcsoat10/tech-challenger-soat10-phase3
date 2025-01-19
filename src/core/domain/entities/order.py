from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, Mapped

from src.core.domain.entities.employee import Employee
from src.core.domain.entities.order_status import OrderStatus
from src.core.domain.entities.order_item import OrderItem
from src.core.exceptions.bad_request_exception import BadRequestException
from src.constants.order_status import OrderStatusEnum
from .base_entity import BaseEntity

STATUS_TRANSITIONS = {
    OrderStatusEnum.ORDER_PENDING: OrderStatusEnum.ORDER_PLACED,
    OrderStatusEnum.ORDER_PLACED: OrderStatusEnum.ORDER_PAID,
    OrderStatusEnum.ORDER_PAID: OrderStatusEnum.ORDER_PREPARING,
    OrderStatusEnum.ORDER_PREPARING: OrderStatusEnum.ORDER_READY,
    OrderStatusEnum.ORDER_READY: OrderStatusEnum.ORDER_COMPLETED,
}

class Order(BaseEntity):
    __tablename__ = 'orders'

    id_customer = Column('id_customer', Integer, ForeignKey('customers.id'), nullable=False)
    customer = relationship('Customer')
    id_order_status = Column('id_order_status', Integer, ForeignKey('order_status.id'), nullable=False, default=1)
    order_status = relationship('OrderStatus')
    id_employee = Column('id_employee', Integer, ForeignKey('employees.id'), nullable=True)
    employee = relationship('Employee')

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
    def order_status_name(self) -> str:
        return self.order_status.status

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
        # TODO: Validar status do pagamento. Por enquanto, considera-se que o pedido está pago. Integrar o pagamento com o pedido.
        return True

    def _validate_status(self, valid_statuses: List[OrderStatusEnum], action: str) -> None:
        if self.order_status.status not in [status.status for status in valid_statuses]:
            raise BadRequestException(f"O pedido não está em um estado válido para {action}.")

    def _record_status_change(self, new_status: OrderStatus, changed_by: str) -> None:
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
        self._validate_status([OrderStatusEnum.ORDER_PENDING], "adicionar itens")
        self.order_items.append(item)

    def remove_item(self, item: OrderItem) -> None:
        self._validate_status([OrderStatusEnum.ORDER_PENDING], "remover itens")
        self.order_items.remove(item)

    def place_order(self, movement_owner: Optional[str] = None) -> None:
        self._validate_status([OrderStatusEnum.ORDER_PENDING], "realizar o pedido")
        new_status = OrderStatus(status=OrderStatusEnum.ORDER_PLACED.status, description=OrderStatusEnum.ORDER_PLACED.description)

        owner = movement_owner or self.customer_name or "Cliente Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def cancel_order(self, movement_owner: Optional[str] = None) -> None:
        self._validate_status(
            [OrderStatusEnum.ORDER_PENDING, OrderStatusEnum.ORDER_PLACED], "cancelar o pedido"
        )

        new_status = OrderStatus(status=OrderStatusEnum.ORDER_CANCELLED.status, description=OrderStatusEnum.ORDER_CANCELLED.description)
        owner = movement_owner or self.customer_name or "Cliente Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def mark_as_paid(self, movement_owner: Optional[str] = None) -> None:
        self._validate_status([OrderStatusEnum.ORDER_PLACED], "marcar o pedido como pago")
        new_status = OrderStatus(status=OrderStatusEnum.ORDER_PAID.status, description=OrderStatusEnum.ORDER_PAID.description)

        owner = movement_owner or self.customer_name or "Cliente Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def prepare_order(self, employee: Employee, movement_owner: Optional[str] = None) -> None:
        self._validate_status([OrderStatusEnum.ORDER_PAID], "preparar o pedido")
        new_status = OrderStatus(status=OrderStatusEnum.ORDER_PREPARING.status, description=OrderStatusEnum.ORDER_PREPARING.description)

        if not self.is_paid:
            raise BadRequestException("O pedido ainda não foi pago. Não é possível preparar o pedido.")

        if not employee:
            raise BadRequestException("É necessário um funcionário para preparar o pedido.")

        self.id_employee = employee.id
        self.employee = employee

        owner = movement_owner or self.employee_name
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def mark_as_ready(self, movement_owner: Optional[str] = None) -> None:
        self._validate_status([OrderStatusEnum.ORDER_PREPARING], "finalizar o pedido")
        new_status = OrderStatus(status=OrderStatusEnum.ORDER_READY.status, description=OrderStatusEnum.ORDER_READY.description)

        owner = movement_owner or self.employee_name
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def complete_order(self, movement_owner: Optional[str] = None) -> None:
        self._validate_status([OrderStatusEnum.ORDER_READY], "completar o pedido")
        new_status = OrderStatus(status=OrderStatusEnum.ORDER_COMPLETED.status, description=OrderStatusEnum.ORDER_COMPLETED.description)

        owner = movement_owner or self.customer_name or "Cliente Anônimo"
        self._record_status_change(new_status, owner)
        self.order_status = new_status

    def next_step(
        self,
        movement_owner: Optional[str] = None,
        employee: Optional[Employee] = None,
    ) -> None:
        current_status = OrderStatusEnum.from_status(self.order_status.status)

        if current_status not in STATUS_TRANSITIONS:
            raise BadRequestException(f"O estado atual {current_status.status} não permite transições.")

        expected_next_status = STATUS_TRANSITIONS[current_status]

        if expected_next_status == OrderStatusEnum.ORDER_PAID:
            if not self.is_paid:
                raise BadRequestException("O pedido ainda não foi pago. Não é possível avançar o status.")

        if expected_next_status == OrderStatusEnum.ORDER_PREPARING:
            
            if not employee:
                raise BadRequestException("É necessário um funcionário para preparar o pedido.")

            self.id_employee = employee.id
            self.employee = employee

        new_status = OrderStatus(status=expected_next_status.status, description=expected_next_status.description)

        if expected_next_status in [OrderStatusEnum.ORDER_PLACED, OrderStatusEnum.ORDER_PAID, OrderStatusEnum.ORDER_COMPLETED]:
            owner = movement_owner or self.customer_name or "Cliente Anônimo"
        elif expected_next_status in [OrderStatusEnum.ORDER_PREPARING, OrderStatusEnum.ORDER_READY]:
            owner = movement_owner or self.employee_name or "Funcionário Anônimo"
        else:
            owner = movement_owner or "System"

        self._record_status_change(new_status, owner)
        self.order_status = new_status

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
