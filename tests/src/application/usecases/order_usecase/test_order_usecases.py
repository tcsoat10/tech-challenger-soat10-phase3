import pytest
from pycpfcnpj import gen

from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.exceptions.bad_request_exception import BadRequestException
from src.constants.order_status import OrderStatusEnum
from src.constants.product_category import ProductCategoryEnum

from src.core.domain.dtos.order_item.create_order_item_dto import CreateOrderItemDTO
from src.core.domain.dtos.product.create_product_dto import CreateProductDTO
from src.core.domain.dtos.category.create_category_dto import CreateCategoryDTO
from src.core.domain.dtos.customer.create_customer_dto import CreateCustomerDTO
from src.core.domain.dtos.person.create_person_dto import CreatePersonDTO

from src.adapters.driven.repositories.order_repository import OrderRepository
from src.adapters.driven.repositories.order_status_repository import OrderStatusRepository
from src.adapters.driven.repositories.customer_repository import CustomerRepository
from src.adapters.driven.repositories.employee_repository import EmployeeRepository
from src.adapters.driven.repositories.product_repository import ProductRepository
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.adapters.driven.repositories.person_repository import PersonRepository

from src.application.usecases.order_usecase.create_order_usecase import CreateOrderUseCase
from src.application.usecases.order_usecase.add_order_item_in_order_usecase import AddOrderItemInOrderUseCase
from src.application.usecases.order_usecase.list_orders_usecase import ListOrdersUseCase
from src.application.usecases.order_usecase.list_order_item_usecase import ListOrderItemsUseCase
from src.application.usecases.order_usecase.remove_order_item_from_order_usecase import RemoveOrderItemFromOrderUseCase
from src.application.usecases.order_usecase.change_item_quantity_usecase import ChangeItemQuantityUseCase
from src.application.usecases.order_usecase.clear_order_usecase import ClearOrderUseCase
from src.application.usecases.order_usecase.advance_order_status_usecase import AdvanceOrderStatusUseCase
from src.application.usecases.order_usecase.revert_order_status_usecase import RevertOrderStatusUseCase
from src.application.usecases.order_usecase.list_products_by_order_status_usecase import ListProductsByOrderStatusUseCase
from src.application.usecases.order_usecase.get_order_status_usecase import GetOrderStatusUsecase

from src.application.usecases.customer_usecase.create_customer_usecase import CreateCustomerUsecase
from src.application.usecases.category_usecase.create_category_usecase import CreateCategoryUseCase
from src.application.usecases.product_usecase.create_product_usecase import CreateProductUsecase
from src.application.usecases.person_usecase.create_person_usecase import CreatePersonUsecase


class TestOrderUseCases:
    
    @pytest.fixture(autouse=True)
    def setup(self, db_session, populate_order_status):
        self.order_gateway = OrderRepository(db_session)
        self.order_status_gateway = OrderStatusRepository(db_session)
        self.customer_gateway = CustomerRepository(db_session)
        self.employee_gateway = EmployeeRepository(db_session)
        self.product_gateway = ProductRepository(db_session)
        self.category_gateway = CategoryRepository(db_session)
        self.person_gateway = PersonRepository(db_session)
        
        self.create_order_usecase = CreateOrderUseCase.build(
            order_gateway=self.order_gateway,
            order_status_gateway=self.order_status_gateway,
            customer_gateway=self.customer_gateway
        )
        
        self.add_order_item_usecase = AddOrderItemInOrderUseCase.build(
            order_gateway=self.order_gateway,
            product_gateway=self.product_gateway
        )
        
        self.list_orders_usecase = ListOrdersUseCase.build(
            order_gateway=self.order_gateway
        )
        
        self.list_order_items_usecase = ListOrderItemsUseCase.build(
            order_gateway=self.order_gateway
        )
        
        self.remove_order_item_usecase = RemoveOrderItemFromOrderUseCase.build(
            order_gateway=self.order_gateway
        )
        
        self.change_item_quantity_usecase = ChangeItemQuantityUseCase.build(
            order_gateway=self.order_gateway
        )
        
        self.clear_order_usecase = ClearOrderUseCase.build(
            order_gateway=self.order_gateway,
            order_status_gateway=self.order_status_gateway
        )
        
        self.advance_order_status_usecase = AdvanceOrderStatusUseCase.build(
            order_gateway=self.order_gateway,
            order_status_gateway=self.order_status_gateway,
            employee_gateway=self.employee_gateway
        )
        
        self.revert_order_status_usecase = RevertOrderStatusUseCase.build(
            order_gateway=self.order_gateway,
            order_status_gateway=self.order_status_gateway
        )
        
        self.list_products_by_order_status_usecase = ListProductsByOrderStatusUseCase.build(
            order_gateway=self.order_gateway,
            product_gateway=self.product_gateway
        )

        self.get_order_status_usecase = GetOrderStatusUsecase.build(
            order_gateway=self.order_gateway, order_status_gateway=self.order_status_gateway
        )
          
        self.create_customer_usecase = CreateCustomerUsecase(
            customer_gateway=self.customer_gateway,
            person_gateway=self.person_gateway
        )
        
        self.create_category_usecase = CreateCategoryUseCase(
            category_gateway=self.category_gateway
        )
        
        self.create_product_usecase = CreateProductUsecase(
            product_gateway=self.product_gateway,
            category_gateway=self.category_gateway
        )
        
        self.create_person_usecase = CreatePersonUsecase(
            person_gateway=self.person_gateway
        )
        
        self._create_test_data()
    
    def _create_test_data(self):
        person_dto = CreatePersonDTO(
            name="Test Customer",
            email="customer@test.com",
            cpf=gen.cpf(),
            birth_date="1990-01-01"
        )
        
        self.test_person = self.create_person_usecase.execute(person_dto)
        
        customer_dto = CreateCustomerDTO(person=person_dto)
        
        self.test_customer = self.create_customer_usecase.execute(customer_dto)
        
        burger_category_dto = CreateCategoryDTO(
            name=ProductCategoryEnum.BURGERS.name,
            description="Hamburgers"
        )
        
        sides_category_dto = CreateCategoryDTO(
            name=ProductCategoryEnum.SIDES.name,
            description="Side dishes"
        )
        
        drinks_category_dto = CreateCategoryDTO(
            name=ProductCategoryEnum.DRINKS.name,
            description="Drinks"
        )
        
        desserts_category_dto = CreateCategoryDTO(
            name=ProductCategoryEnum.DESSERTS.name,
            description="Desserts"
        )
        
        self.burger_category = self.create_category_usecase.execute(burger_category_dto)
        self.sides_category = self.create_category_usecase.execute(sides_category_dto)
        self.drinks_category = self.create_category_usecase.execute(drinks_category_dto)
        self.desserts_category = self.create_category_usecase.execute(desserts_category_dto)
        
        burger_dto = CreateProductDTO(
            name="Test Burger",
            description="A tasty burger",
            price=15.0,
            category_id=self.burger_category.id
        )
        
        sides_dto = CreateProductDTO(
            name="Test Fries",
            description="Crispy fries",
            price=8.0,
            category_id=self.sides_category.id
        )
        
        drink_dto = CreateProductDTO(
            name="Test Soda",
            description="Refreshing soda",
            price=5.0,
            category_id=self.drinks_category.id
        )
        
        dessert_dto = CreateProductDTO(
            name="Test Ice Cream",
            description="Sweet ice cream",
            price=7.0,
            category_id=self.desserts_category.id
        )
        
        self.burger_product = self.create_product_usecase.execute(burger_dto)
        self.sides_product = self.create_product_usecase.execute(sides_dto)
        self.drink_product = self.create_product_usecase.execute(drink_dto)
        self.dessert_product = self.create_product_usecase.execute(dessert_dto)
    
    @pytest.fixture
    def customer_user(self):
        return {
            "profile": {"name": "customer"},
            "person": {"id": str(self.test_customer.person.id)}
        }
    
    def test_create_order_usecase(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)
        
        assert order.id is not None
        assert order.customer.id == self.test_customer.id
        assert order.order_status.status == OrderStatusEnum.ORDER_PENDING.status
    
    def test_create_order_when_open_order_exists(self, customer_user):
        self.create_order_usecase.execute(current_user=customer_user)
        
        with pytest.raises(BadRequestException, match="Já existe um pedido em aberto para este cliente"):
            self.create_order_usecase.execute(current_user=customer_user)
    
    def test_list_orders_usecase(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)
        
        orders = self.list_orders_usecase.execute(current_user=customer_user)
        
        assert len(orders) == 1
        assert orders[0].id == order.id
    
    def test_advance_order_status_to_waiting_burgers(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)
        
        updated_order = self.advance_order_status_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status
    
    def test_add_order_item_in_order_usecase(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)
        
        self.advance_order_status_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_product.id,
            quantity=2,
            observation="No pickles"
        )
        
        updated_order = self.add_order_item_usecase.execute(
            order_id=order.id,
            order_item_dto=order_item_dto,
            current_user=customer_user
        )
        
        assert len(updated_order.order_items) == 1
        assert updated_order.order_items[0].product.id == self.burger_product.id
        assert updated_order.order_items[0].quantity == 2
        assert updated_order.order_items[0].observation == "No pickles"
    
    def test_list_order_items_usecase(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)
        
        self.advance_order_status_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_product.id,
            quantity=2,
            observation="No pickles"
        )
        
        self.add_order_item_usecase.execute(
            order_id=order.id,
            order_item_dto=order_item_dto,
            current_user=customer_user
        )
        
        order_items = self.list_order_items_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        assert len(order_items) == 1
        assert order_items[0].product.id == self.burger_product.id
        assert order_items[0].quantity == 2
    
    def test_change_item_quantity_usecase(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)
        
        self.advance_order_status_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_product.id,
            quantity=2,
            observation="No pickles"
        )
        
        updated_order = self.add_order_item_usecase.execute(
            order_id=order.id,
            order_item_dto=order_item_dto,
            current_user=customer_user
        )
        
        order_item_id = updated_order.order_items[0].id
        
        self.change_item_quantity_usecase.execute(
            order_id=order.id,
            order_item_id=order_item_id,
            new_quantity=3,
            current_user=customer_user
        )
        
        order_items = self.list_order_items_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        assert order_items[0].quantity == 3
    
    def test_remove_order_item_from_order_usecase(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)
        
        self.advance_order_status_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_product.id,
            quantity=1,
            observation="No pickles"
        )
        
        updated_order = self.add_order_item_usecase.execute(
            order_id=order.id,
            order_item_dto=order_item_dto,
            current_user=customer_user
        )
        
        order_item_id = updated_order.order_items[0].id
        
        self.remove_order_item_usecase.execute(
            order_id=order.id,
            order_item_id=order_item_id,
            current_user=customer_user
        )
        
        order_items = self.list_order_items_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        assert len(order_items) == 0
    
    def test_clear_order_usecase(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)
        
        self.advance_order_status_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        order_item_dto = CreateOrderItemDTO(
            product_id=self.burger_product.id,
            quantity=2,
            observation="No pickles"
        )
        
        self.add_order_item_usecase.execute(
            order_id=order.id,
            order_item_dto=order_item_dto,
            current_user=customer_user
        )
        
        self.clear_order_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        order_items = self.list_order_items_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        assert len(order_items) == 0
    
    def test_revert_order_status_usecase_when_order_is_waiting_burgers_and_return_error(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)
        
        updated_order = self.advance_order_status_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status
        
        with pytest.raises(BadRequestException) as exc:
            self.revert_order_status_usecase.execute(
                order_id=order.id,
                current_user=customer_user
            )
        
        assert exc.value.args[0] == "O status atual 'order_waiting_burgers' não permite voltar."
        
    def test_revert_order_status_usecase_when_order_is_waiting_side_dishes_and_return_success(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)
        
        updated_order = self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)
        updated_order = self.advance_order_status_usecase.execute(order_id=order.id, current_user=customer_user)
        
        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_SIDES.status

        self.revert_order_status_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        assert updated_order.order_status.status == OrderStatusEnum.ORDER_WAITING_BURGERS.status
    
    def test_list_products_by_order_status_usecase(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)
        
        self.advance_order_status_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        products = self.list_products_by_order_status_usecase.execute(
            order_id=order.id,
            current_user=customer_user
        )
        
        assert len(products) == 1
        assert products[0].id == self.burger_product.id
    
    def test_access_non_existent_order(self, customer_user):
        with pytest.raises(EntityNotFoundException):
            self.list_order_items_usecase.execute(
                order_id=999,
                current_user=customer_user
            )

    def test_get_order_status_usecase(self, customer_user):
        order = self.create_order_usecase.execute(current_user=customer_user)

        status = self.get_order_status_usecase.execute(order.id, current_user=customer_user)

        assert status == order.order_status
        