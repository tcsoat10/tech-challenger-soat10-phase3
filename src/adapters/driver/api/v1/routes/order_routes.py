from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Security, status
from sqlalchemy.orm import Session

from src.adapters.driver.api.v1.controllers.order_controller import OrderController
from src.constants.permissions import OrderPermissions
from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.dtos.order_item.order_item_dto import OrderItemDTO
from src.core.domain.dtos.product.product_dto import ProductDTO
from src.adapters.driven.repositories.product_repository import ProductRepository
from src.core.ports.product.i_product_repository import IProductRepository
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.core.ports.order_status.i_order_status_repository import IOrderStatusRepository
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from config.database import get_db
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.adapters.driven.repositories.order_repository import OrderRepository
from src.application.services.order_service import OrderService
from src.core.domain.dtos.order.order_dto import OrderDTO
from src.core.ports.order.i_order_repository import IOrderRepository
from src.core.ports.order.i_order_service import IOrderService

from src.core.auth.dependencies import get_current_user


router = APIRouter()

# Substituir por lib DI.
def _get_order_service(db_session: Session = Depends(get_db)) -> IOrderService:
    customer_repository: ICustomerRepository = CustomerRepository(db_session)
    order_status_repository: IOrderStatusRepository = OrderStatusRepository(db_session)
    employee_repository: IEmployeeRepository = EmployeeRepository(db_session)
    product_repository: IProductRepository = ProductRepository(db_session)
    repository: IOrderRepository = OrderRepository(db_session)


    return OrderService(
        repository,
        order_status_repository,
        customer_repository,
        employee_repository,
        product_repository
    )
    
def _get_order_controller(db_session: Session = Depends(get_db)) -> OrderController:
    return OrderController(db_session)

router = APIRouter()

# Criar um pedido
@router.post(
    "/orders",
    response_model=OrderDTO,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Security(get_current_user, scopes=[OrderPermissions.CAN_CREATE_ORDER])],
)
async def create_order(
    current_user: dict = Depends(get_current_user),
    controller: OrderController = Depends(_get_order_controller),
):
    return controller.create_order(current_user)

# Listar produtos com base no status do pedido
@router.get(
    "/orders/{order_id}/products",
    response_model=List[ProductDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[OrderPermissions.CAN_LIST_PRODUCTS_BY_ORDER_STATUS])],
)
async def list_products_by_order_status(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    controller: OrderController = Depends(_get_order_controller),
):
    return controller.list_products_by_order_status(order_id, current_user)

@router.get(
    "/orders/{order_id}",
    response_model=OrderDTO,
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[OrderPermissions.CAN_VIEW_ORDER])],
)
async def get_order_by_id(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    controller: OrderController = Depends(_get_order_controller),
):
    return controller.get_order_by_id(order_id, current_user)

# Adicionar item ao pedido
@router.post(
    "/orders/{order_id}/items",
    dependencies=[Security(get_current_user, scopes=[OrderPermissions.CAN_ADD_ITEM])],
    status_code=status.HTTP_201_CREATED,
)
async def add_item(
    order_id: int,
    dto: CreateOrderItemDTO,
    current_user: dict = Depends(get_current_user),
    controller: OrderController = Depends(_get_order_controller),
):
    controller.add_item(order_id, dto, current_user)
    return {"detail": "Item adicionado com sucesso."}

# Remover item do pedido
@router.delete(
    "/orders/{order_id}/items/{item_id}",
    dependencies=[Security(get_current_user, scopes=[OrderPermissions.CAN_REMOVE_ITEM])],
    status_code=status.HTTP_200_OK,
)
async def remove_item(
    order_id: int,
    item_id: int,
    current_user: dict = Depends(get_current_user),
    controller: OrderController = Depends(_get_order_controller),
):
    controller.remove_item(order_id, item_id, current_user)
    return {"detail": "Item removido com sucesso."}

# Atualizar quantidade de item do pedido
@router.put(
    "/orders/{order_id}/items/{item_id}/quantity",
    dependencies=[Security(get_current_user, scopes=[OrderPermissions.CAN_CHANGE_ITEM_QUANTITY])],
    status_code=status.HTTP_200_OK,
)
async def change_item_quantity(
    order_id: int,
    order_item_id: int,
    new_quantity: int,
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends(_get_order_service),
):
    service.change_item_quantity(order_id, order_item_id, new_quantity, current_user)
    return {"detail": "Quantidade atualizada com sucesso."}

# Atualizar observação de item do pedido
@router.put(
    "/orders/{order_id}/items/{item_id}/observation",
    dependencies=[Security(get_current_user, scopes=[OrderPermissions.CAN_CHANGE_ITEM_OBSERVATION])],
    status_code=status.HTTP_200_OK,
)
async def change_item_observation(
    order_id: int,
    item_id: int,
    new_observation: str,
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends(_get_order_service),
):
    service.change_item_observation(order_id, item_id, new_observation, current_user)
    return {"detail": "Observação atualizada com sucesso."}


# Listar itens do pedido
@router.get(
    "/orders/{order_id}/items",
    response_model=List[OrderItemDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[OrderPermissions.CAN_LIST_ORDER_ITEMS])],
)
async def list_order_items(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends(_get_order_service),
):
    return service.list_order_items(order_id, current_user)

# Cancelar pedido
@router.post(
    "/orders/{order_id}/cancel",
    dependencies=[Security(get_current_user, scopes=[OrderPermissions.CAN_CANCEL_ORDER])],
    status_code=status.HTTP_200_OK,
)
async def cancel_order(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends(_get_order_service),
):
    service.cancel_order(order_id, current_user)
    return {"detail": "Pedido cancelado com sucesso."}

# Avançar para o próximo passo no pedido
@router.post("/orders/{order_id}/next-step")
async def next_step(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends(_get_order_service),
):
    return service.next_step(order_id, current_user)

# Retornar ao passo anterior
@router.post(
    "/orders/{order_id}/go-back",
    dependencies=[Security(get_current_user, scopes=[OrderPermissions.CAN_GO_BACK])],
    status_code=status.HTTP_200_OK,
)
async def go_back(
    order_id: int,
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends(_get_order_service),
):
    service.go_back(order_id, current_user)
    return {"detail": "Pedido retornado ao passo anterior com sucesso."}

# Listar todos os pedidos
@router.get(
    "/orders",
    response_model=List[OrderDTO],
    status_code=status.HTTP_200_OK,
    dependencies=[Security(get_current_user, scopes=[OrderPermissions.CAN_LIST_ORDERS])],
)
async def list_orders(
    status: Optional[List[str]] = Query(
        default=[],
        description="Lista de status dos pedidos para filtrar, por exemplo: ?status=order_pending&status=order_paid"
    ),
    current_user: dict = Depends(get_current_user),
    service: OrderService = Depends(_get_order_service),
):
    return service.list_orders(current_user, status)
