from abc import ABC, abstractmethod


class IAuthProviderGateway(ABC):
    """
    Interface for authentication provider gateways.
    This interface defines the methods that any authentication provider gateway must implement.
    """

    @abstractmethod
    def authenticate(self, cpf: str) -> bool:
        """
        Authenticates a customer with the given CPF.
        Returns True if authentication is successful, False otherwise.
        """
        pass

    @abstractmethod
    def sync_user(self, user_id: str) -> None:
        """
        Synchronizes the user data with the authentication provider.
        This method should be called when user data is updated in the system.
        """
        pass