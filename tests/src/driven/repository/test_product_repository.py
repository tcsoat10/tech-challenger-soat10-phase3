import pytest
from sqlalchemy.exc import IntegrityError
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
    
