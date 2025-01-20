import uuid
from src.core.domain.entities.person import Person
from src.core.domain.entities.employee import Employee
from src.core.ports.employee.i_employee_repository import IEmployeeRepository
from src.core.domain.entities.customer import Customer
from src.core.ports.profile.i_profile_repository import IProfileRepository
from src.core.ports.customer.i_customer_repository import ICustomerRepository
from src.core.ports.auth.i_auth_service import IAuthService
from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO, LoginDTO, TokenDTO
from src.core.exceptions.invalid_credeitals_exception import InvalidCredentialsException
from src.core.exceptions.entity_not_found_exception import EntityNotFoundException
from src.core.utils.jwt_util import JWTUtil

class AuthService(IAuthService):
    def __init__(self, customer_repository, profile_repository, employee_repository):
        self.profile_repository: IProfileRepository = profile_repository
        self.employee_repository: IEmployeeRepository = employee_repository
        self.customer_repository: ICustomerRepository = customer_repository

    def login_customer_by_cpf(self, dto: AuthByCpfDTO) -> TokenDTO:
        customer: Customer = self.customer_repository.get_by_cpf(dto.cpf)
        if not customer:
            raise EntityNotFoundException(entity_name="Customer")

        customer_profile = self.profile_repository.get_by_name("customer")
        if not customer_profile:
            raise EntityNotFoundException(entity_name="Customer profile")

        permissions = [permission.name for permission in customer_profile.permissions]
        if not permissions:
            raise EntityNotFoundException(entity_name="Customer permissions")

        token_payload = {
            "person": {
                "id": str(customer.id),
                "name": customer.person.name,
                "cpf": customer.person.cpf,
                "email": customer.person.email,
            },
            "profile": {
                "name": customer_profile.name,
                "permissions": permissions,
            },
        }

        token = JWTUtil.create_token(token_payload)
        return TokenDTO(access_token=token, token_type="bearer")
    
    def login_anonymous(self) -> TokenDTO:
        customer_profile = self.profile_repository.get_by_name("customer")
        if not customer_profile:
            raise EntityNotFoundException(entity_name="Customer profile")
        
        anonymous_person = Person(name=f"Anonymous User - {uuid.uuid4().hex}")
        customer = Customer(person=anonymous_person)
        self.customer_repository.create(customer)

        token_payload = {
            "person": {
                "id": customer.id,
                "name": customer.person.name,
            },
            "profile": {
                "name": customer_profile.name,
                "permissions": [permission.name for permission in customer_profile.permissions],
            },
        }

        token = JWTUtil.create_token(token_payload)
        return TokenDTO(access_token=token, token_type="bearer")

    def login_employee(self, login_dto: LoginDTO) -> TokenDTO:
        employee: Employee = self.employee_repository.get_by_username(login_dto.username)
        if not employee or not employee.user.verify_password(login_dto.password):
            raise InvalidCredentialsException()
        
        profile_name = 'employee'
        if employee.role.name == 'manager':
            profile_name = 'manager'

        employee_profile = self.profile_repository.get_by_name(profile_name)
        if not employee_profile:
            raise EntityNotFoundException(entity_name="Employee profile")
 
        permissions = [permission.name for permission in employee_profile.permissions]
        if not permissions:
            raise EntityNotFoundException(entity_name="Employee permissions")

        token_payload = {
            "person": {
                "id": str(employee.id),
                "name": employee.person.name,
                "cpf": employee.person.cpf,
                "email": employee.person.email,
            },
            "profile": {
                "name": employee_profile.name,
                "permissions": permissions,
            },
        }

        token = JWTUtil.create_token(token_payload)
        return TokenDTO(access_token=token, token_type="bearer")
