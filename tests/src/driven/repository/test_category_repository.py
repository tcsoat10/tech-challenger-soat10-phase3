import pytest
from sqlalchemy.exc import IntegrityError
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

    def test_repository_create_category_duplicate_error(self, db_session):
        """
        Testa erro ao tentar criar uma categoria com nome duplicado.
        """
        # Dados da categoria
        new_category = Category(name="Drinks", description="Beverages category")

        # Cria a primeira categoria
        self.repository.create(new_category)

        # Tenta criar uma segunda categoria com o mesmo nome
        duplicate_category = Category(name="Drinks", description="Another description")

        with pytest.raises(IntegrityError):
            self.repository.create(duplicate_category)

    def test_get_category_by_name_success(self):
        """
        Testa a recuperação de uma categoria pelo Nome com sucesso.
        """
        new_category = Category(name="Drinks", description="Beverages category")
        created_category = self.repository.create(new_category)

        category = self.repository.get_by_name(created_category.name)

        assert category is not None
        assert category.id == created_category.id
        assert category.name == "Drinks"
        assert category.description == "Beverages category"

    def test_get_category_by_name_with_no_name_registered(self):
        """
        Testa a busca de uma categoria por nome que não está registrado.
        """
        new_category = Category(name="Drinks", description="Beverages category")
        self.repository.create(new_category)

        category = self.repository.get_by_name("no name")

        assert category is None
    
    def test_get_category_by_id_success(self):
        """
        Testa a recuperação de uma categoria pelo ID com sucesso.
        """
        new_category = Category(name="Drinks", description="Beverages category")
        created_category = self.repository.create(new_category)

        category = self.repository.get_by_id(created_category.id)

        assert category is not None
        assert category.id == created_category.id
        assert category.name == "Drinks"
        assert category.description == "Beverages category"

    
    def test_get_category_by_id_with_no_id_registered(self):
        """
        Testa a busca de uma categoria por id que não está registrado.
        """
        new_category = Category(name="Drinks", description="Beverages category")
        self.repository.create(new_category)

        category = self.repository.get_by_id(2)

        assert category is None

    def test_get_all_categories(self):
        """
        Testa a listagem de todas as categorias.
        """
        category1 = Category(name="Drinks", description="Beverages category")
        category2 = Category(name="Burgers", description="Fast food category")

        self.repository.create(category1)
        self.repository.create(category2)

        categories = self.repository.get_all()

        assert len(categories) == 2
        assert categories[0].name == "Drinks"
        assert categories[1].name == "Burgers"
    

    def test_get_all_categories_with_emtpy_db(self):
        """
        Testa a listagem de todas as categorias quando o banco de dados está vazio.
        """
        categories = self.repository.get_all()

        assert len(categories) == 0
        assert categories == []
    
