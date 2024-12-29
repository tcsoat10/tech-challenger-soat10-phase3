import pytest
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from src.core.domain.entities.product import Product
from src.adapters.driven.repositories.product_repository import ProductRepository
from tests.factories.category_factory import CategoryFactory
from tests.factories.product_factory import ProductFactory


class TestProductRepository:

    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = ProductRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(Product).delete()
        self.db_session.commit()

    def test_create_product_success(self):
        category = CategoryFactory()
        product = Product(
            name="Cheeseburger",
            description="A delicious cheeseburger.",
            category_id=category.id,
            price=39.90,
            sla_product="Standard SLA"
        )

        created_product = self.repository.create(product)

        assert created_product.id is not None
        assert created_product.name == "Cheeseburger"
        assert created_product.description == "A delicious cheeseburger."
        assert created_product.category_id == category.id
        assert created_product.price == 39.90
        assert created_product.sla_product == "Standard SLA"

    def test_repository_create_category_duplicate_error(self, db_session):
        category = CategoryFactory()
        ProductFactory(name="Cheeseburger", category=category)

        product2 = Product(
            name="Cheeseburger",
            description="A delicious cheeseburger.",
            category_id=category.id,
            price=39.90,
            sla_product="Standard SLA"
        )

        with pytest.raises(IntegrityError):
            self.repository.create(product2)

    def test_get_product_by_name_success(self):
        category = CategoryFactory()
        product = ProductFactory(
            name="Cheeseburger",
            description="A delicious cheeseburger.",
            category=category,
            price=39.90,
            sla_product="Standard SLA"
        )
       
        product_response = self.repository.get_by_name(product.name)

        assert product_response.id is not None
        assert product_response.name == "Cheeseburger"
        assert product_response.description == "A delicious cheeseburger."
        assert product_response.category_id == category.id
        assert product_response.price == 39.90
        assert product_response.sla_product == "Standard SLA"

    def test_get_by_name_returns_none_for_unregistered_name(self):
        ProductFactory()
        category = self.repository.get_by_name("no name")
        assert category is None
    
    def test_get_product_by_id_success(self):
        category = CategoryFactory()
        product = ProductFactory(
            name="Cheeseburger",
            description="A delicious cheeseburger.",
            category=category,
            price=39.90,
            sla_product="Standard SLA"
        )
       
        product_response = self.repository.get_by_id(product_id=product.id)

        assert product_response.id is not None
        assert product_response.name == "Cheeseburger"
        assert product_response.description == "A delicious cheeseburger."
        assert product_response.category_id == category.id
        assert product_response.price == 39.90
        assert product_response.sla_product == "Standard SLA"

    
    def test_get_by_id_returns_none_for_unregistered_id(self):
        ProductFactory()
        category = self.repository.get_by_id(product_id=1)
        assert category is None

    def test_get_all_products_return_success(self):
        category1 = CategoryFactory(name="Drinks")
        category2 = CategoryFactory(name="Fast food")
        product1 = ProductFactory(
            name="Coca-Cola",
            description="Soft drink",
            price=6.99,
            category=category1
        )
        product2 = ProductFactory(
            name="Big Mac",
            description="Fast food burger",
            price=20.99,
            category=category2
        )
        
        products = self.repository.get_all()
       
        assert products == [
            product1,
            product2,
        ]

    def test_get_all_products_with_emtpy_db(self):
        products = self.repository.get_all()

        assert len(products) == 0
        assert products == []
    
    def test_update_product(self):
        category = CategoryFactory(name="Fast food")
        category2 = CategoryFactory(name="Burgers")
        
        product = ProductFactory(
            name="Big Mac",
            description="Fast food burger",
            price=20.99,
            category=category
        )

        product.name = "Big Mac - updated"
        product.description = "Fast food burger - updated"
        product.price = 28.99
        product.category_id = category2.id
        
        data = self.repository.update(product)

        assert data.id == product.id
        assert data.name == product.name
        assert data.description == product.description
        assert data.price == product.price
        assert data.category_id == product.category_id

    def test_delete_product(self):
        category1 = CategoryFactory(name="Drinks")
        category2 = CategoryFactory(name="Fast food")
        product1 = ProductFactory(name="Coca-Cola", category=category1)
        product2 = ProductFactory(name="Big Mac", category=category2)

        self.repository.delete(product1)
        data = self.repository.get_all()
        
        assert len(data) == 1
        assert data[0].id == product2.id
        assert data[0].name == product2.name
        assert data[0].description == product2.description
        assert data[0].price == product2.price
        assert data[0].category_id == product2.category_id
        

    def test_delete_product_with_inexistent_id(self):
        category = CategoryFactory(name="Soft Drinks")
        product = ProductFactory(name="Coca-Cola", category=category)

        product_not_registered = Product(
            id=999, name="Big Mac", description="Fast food burger", price=20.99, category=category
        )

        with pytest.raises(InvalidRequestError):
            self.repository.delete(product_not_registered)

        products = self.repository.get_all()
        assert len(products) == 1
        assert products[0] == product
