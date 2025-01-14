from abc import ABC, abstractmethod

from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO, LoginDTO, TokenDTO

class IAuthService(ABC):
    @abstractmethod
    async def login_customer_by_cpf(self, data: AuthByCpfDTO) -> TokenDTO:
        pass

    @abstractmethod
    async def login_anonymous(self) -> TokenDTO:
        pass

    @abstractmethod
    async def login_employee(self, data: LoginDTO) -> TokenDTO:
        pass
