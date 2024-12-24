import pytest
from src.adapters.driven.repositories.category_repository import CategoryRepository
from src.core.domain.entities.category import Category


class TestCategoryRepository:
    """
    Testes para o repositório de Category.
    """
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = CategoryRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(Category).delete()
        self.db_session.commit()

    def test_create_category_success(self):
        # Criando a categoria "Drinks"
        drinks_category = Category(name="Drinks", description="Beverages category")
        created_drinks_category = self.repository.create(drinks_category)

        assert created_drinks_category.id is not None
        assert created_drinks_category.name == "Drinks"
        assert created_drinks_category.description == "Beverages category"

        # Criando a categoria "Burgers"
        burgers_category = Category(name="Burgers", description="Fast food category")
        created_burgers_category = self.repository.create(burgers_category)

        assert created_burgers_category.id is not None
        assert created_burgers_category.name == "Burgers"
        assert created_burgers_category.description == "Fast food category"

        # Verifica se a categoria Drinks foi persistida no banco
        db_category = self.db_session.query(Category).filter_by(name="Drinks").first()
        assert db_category is not None
        assert db_category.name == "Drinks"

        # Verifica se a categoria Burgers foi persistida no banco
        db_category = self.db_session.query(Category).filter_by(name="Burgers").first()
        assert db_category is not None
        assert db_category.name == "Burgers"
