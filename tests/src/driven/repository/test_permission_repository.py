import pytest
from src.adapters.driven.repositories.permission_repository import PermissionRepository
from src.core.domain.entities.permission import Permission


class TestPermissionRepository:
    """
    Testes para o repositório de Permission.
    """
    @pytest.fixture(autouse=True)
    def setup(self, db_session):
        self.repository = PermissionRepository(db_session)
        self.db_session = db_session
        self.clean_database()

    def clean_database(self):
        self.db_session.query(Permission).delete()
        self.db_session.commit()

    def test_create_permission_success(self):
        # Criando a permissão "Admin"
        admin_permission = Permission(name="Admin", description="System admin permission")
        created_admin_permission = self.repository.create(admin_permission)

        assert created_admin_permission.id is not None
        assert created_admin_permission.name == "Admin"
        assert created_admin_permission.description == "System admin permission"

        # Criando a permissão "Employee"
        employee_permission = Permission(name="Employee", description="System user permission")
        created_employee_permission = self.repository.create(employee_permission)

        assert created_employee_permission.id is not None
        assert created_employee_permission.name == "Employee"
        assert created_employee_permission.description == "System user permission"

        # Verifica se a permissão Admin foi persistida no banco
        db_permission = self.db_session.query(Permission).filter_by(name="Admin").first()
        assert db_permission is not None
        assert db_permission.name == "Admin"

        # Verifica se a permissão Employee foi persistida no banco
        db_permission = self.db_session.query(Permission).filter_by(name="Employee").first()
        assert db_permission is not None
        assert db_permission.name == "Employee"
