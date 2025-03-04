from abc import ABC, abstractmethod

from src.core.domain.dtos.auth.auth_dto import AuthByCpfDTO, LoginDTO, TokenDTO

class IAuthService(ABC):

    @abstractmethod
    async def login_employee(self, data: LoginDTO) -> TokenDTO:
        pass
