import uuid
import os
import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect, text
from alembic.config import Config
from alembic import command
from src.app import app
from config import settings
from config.database import get_db
from tests.factories.category_factory import CategoryFactory
from tests.factories.order_item_factory import OrderItemFactory
from tests.factories.payment_method_factory import PaymentMethodFactory
from tests.factories.payment_status_factory import PaymentStatusFactory
from tests.factories.product_factory import ProductFactory
from tests.factories.permission_factory import PermissionFactory
from tests.factories.profile_factory import ProfileFactory
from tests.factories.profile_permission_factory import ProfilePermissionFactory
from tests.factories.role_factory import RoleFactory
from tests.factories.user_factory import UserFactory
from tests.factories.user_profile_factory import UserProfileFactory


def create_database_url(user: str, password: str, host: str, port: str, database_name: str = ""):
    return f"mysql+pymysql://{user}:{password}@{host}:{port}/{database_name}"

@pytest.fixture(scope="function")
def setup_test_database():
    random_id = uuid.uuid4().hex[:8]
    test_user = f"temp_user_{random_id}"
    test_password = f"temp_pass_{random_id}"
    test_database = f"{os.getenv('MYSQL_DATABASE', 'test_db')}_test_{random_id}"

    # URL BD root user
    root_database_url = create_database_url(
        os.getenv("MYSQL_ROOT_USER", "root"),
        os.getenv("MYSQL_ROOT_PASSWORD", "root_password"),
        os.getenv("MYSQL_HOST", "localhost"),
        os.getenv("MYSQL_PORT", "3306")
    )

    # Conexão com o banco como root para criação de banco e usuário
    root_engine = create_engine(root_database_url, echo=True)

    try:
        with root_engine.connect() as connection:
            # Criando o banco de teste
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS `{test_database}`;"))

            # Criando o usuário com permissões
            connection.execute(
                text(
                    f"CREATE USER IF NOT EXISTS '{test_user}'@'%' IDENTIFIED BY '{test_password}';"
                )
            )
            connection.execute(
                text(
                    f"GRANT ALL PRIVILEGES ON `{test_database}`.* TO '{test_user}'@'%';"
                )
            )
            connection.execute(text("FLUSH PRIVILEGES;"))

        # URL do banco de teste com usuário de teste
        test_database_url = create_database_url(
            test_user, test_password, os.getenv("MYSQL_HOST", "localhost"),
            os.getenv("MYSQL_PORT", "3306"), test_database
        )

        # Redefinindo a constante DATABASE que será executada no env.py 
        settings.DATABASE.update({
            "drivername": "mysql+pymysql",
            "host": os.getenv("MYSQL_HOST", "localhost"),
            "port": os.getenv("MYSQL_PORT", "3306"),
            "user": test_user,
            "password": test_password,
            "name": test_database,
        })

        print(f"Usando configuração DATABASE={settings.DATABASE}")

        # Executando as migrações no banco de teste
        alembic_config = Config("alembic.ini")
        try:
            command.upgrade(alembic_config, "head")
            print("Migrações executadas com sucesso.")
        except Exception as e:
            pytest.fail(f"Erro ao aplicar migrações: {e}")

        test_engine = create_engine(test_database_url, echo=True)
        inspector = inspect(test_engine)
        created_tables = inspector.get_table_names()
        print(f"Tabelas criadas: {created_tables}")

        # expected_tables = ["categories"]
        # if not all(table in created_tables for table in expected_tables):
        #     pytest.fail(
        #         f"As seguintes tabelas não foram criadas: "
        #         f"{[table for table in expected_tables if table not in created_tables]}"
        #     )

        yield test_database_url
    finally:
        # Limpando o banco após cada teste, independentemente de falhas
        try:
            with root_engine.connect() as connection:
                connection.execute(text(f"DROP DATABASE IF EXISTS `{test_database}`;"))
                connection.execute(text(f"DROP USER IF EXISTS '{test_user}'@'%';"))
                connection.execute(text("FLUSH PRIVILEGES;"))
            print(f"Banco e usuário removidos: {test_database}, {test_user}")
        except Exception as e:
            print(f"Erro ao limpar banco ou usuário de teste: {e}")

    root_engine.dispose()


@pytest.fixture(scope="function")
def db_session(setup_test_database):
    """
    Cria uma sessão de banco de dados para cada teste.
    """
    test_engine = create_engine(setup_test_database, echo=False)
    SessionLocal = sessionmaker(bind=test_engine)

    session = SessionLocal()
    def override_get_db():
        try:
            yield session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    try:
        yield session
    finally:
        session.close()
        test_engine.dispose()
        app.dependency_overrides.pop(get_db, None)


@pytest.fixture(scope="function")
def client() -> Generator[TestClient, None, None]:
    """
    Cria um cliente de teste para a aplicação.
    """
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function", autouse=True)
def setup_factories(db_session):
    """
    Configura as factories para usar a sessão do banco de dados de teste.
    """
    factories = [
        CategoryFactory,
        ProductFactory,
        OrderItemFactory,
        PermissionFactory,
        ProfileFactory,
        ProfilePermissionFactory,
        PaymentMethodFactory,
        RoleFactory,
        PaymentStatusFactory,
        UserFactory,
        UserProfileFactory,
    ]

    for factory in factories:
        factory._meta.sqlalchemy_session = db_session
        factory.reset_sequence()
