from src.core.ports.auth.i_auth_provider_gateway import IAuthProviderGateway
import os
import requests


class AWSCognitoGateway(IAuthProviderGateway):
    """
    Implementação do gateway de autenticação usando o AWS Cognito.
    """

    def __init__(self):
        self.base_url = os.getenv('API_GATEWAY_URL')
        self.headers = {
            "Content-Type": "application/json"
        }
    
    def authenticate(self, user_data: dict) -> bool:
        """
        Autentica um usuário com o AWS Cognito.
        Retorna True se a autenticação for bem-sucedida, False caso contrário.
        """
        if 'cpf' in user_data:
            cpf = user_data.get('cpf')

            try:
                response = requests.post(
                    f"{self.base_url}/login",
                    json={"cpf": cpf},
                    headers=self.headers
                )
                
                if response.status_code == 200:
                    return True
                return False
            except Exception as e:
                print(f"Erro ao autenticar usuário: {str(e)}")
                return False
        