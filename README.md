# Tech Challenge - Grupo 24 SOAT10 - Pós Tech Arquitetura de Software - FIAP


# Descrição do Projeto

O projeto visa atender à demanda de uma lanchonete de bairro, que, devido ao seu sucesso, necessita implementar um sistema de autoatendimento.

# Requisitos

## **Docker**

O projeto utiliza o [Docker](https://www.docker.com/) para gerenciamento de containers e volumes. É necessário garantir que o Docker Compose esteja instalado.

## **Python**

A versão utilizada do Python foi a 3.12, disponível para [download](https://www.python.org/downloads/).

## **Dependências / Bibliotecas**

As dependências do projeto foram gerenciadas com o [Poetry](https://python-poetry.org/docs/#installation). 

Após instalado, o comando **`poetry init`** cria um ambiente virtual a partir do arquivo **`pyproject.toml`**. Com o ambiente virtual criado, o comando **`poetry shell`** ativa o ambiente, e o comando **`poetry install`** instala as dependências do projeto no ambiente virtual.

## **Banco de Dados**

O banco de dados utilizado foi o MySQL versão 8, executado dentro de um container.

## Demais tecnologias
- SQLAlchemy
- Make
- FastAPI
- Pytest
- Alembic
- bcrypt
- faker

# Executando o projeto
## 1. Clonar o repositório
    
No diretório definido para armazenar os arquivos do projeto, executar o comando `git clone https://github.com/carlosrjr/tech-challenger-soat10-phase1.git` caso deseje clonar o repositório usando HTTPS. Se for utilizado SSH, o comando deve ser `git clone git@github.com:carlosrjr/tech-challenger-soat10-phase1.git`.

## 2. Arquivo .env

O arquivo .env contém valores necessários para a execução do projeto, como senhas e variáveis de ambiente. Ele não deve ser salvo no repositório remoto, e é necessário que seja alocado no diretório raiz do projeto.

### Envs necessárias
```

# Configuração do Banco de Dados
MYSQL_VERSION=""
MYSQL_CONTAINER_NAME=""
MYSQL_ROOT_PASSWORD=""
MYSQL_DATABASE=""
MYSQL_USER=""
MYSQL_PASSWORD=""
MYSQL_HOST=""
MYSQL_PORT=""

# Configurações de ambiente
DEBUG=true
ENVIRONMENT=development

# Configurações de servidor
APP_NAME=soat10
APP_PORT=8000

# Configuração de logs
LOG_LEVEL=INFO

# JWT
SECRET_KEY=

# Mercado Pago
MERCADO_PAGO_ACCESS_TOKEN=
MERCADO_PAGO_USER_ID=
MERCADO_PAGO_POS_ID=

# Webhook
WEBHOOK_URL="http://localhost:8000"
```

## 3.1. Docker Compose (produção)

Após verificar que a Docker Engine está ativa, executar o comando **`docker compose up -d --build`** no diretório raiz do projeto. Este comando sobe a aplicação e o banco de dados seguindo as instruções definidas no arquivo **`docker-compose.yml`**.

Dois containers serão executados dentro de uma única rede, um para o banco de dados MySQL e um para a aplicação. O container da aplicação tem sua imagem construída a partir do **`Dockerfile`** presente no projeto.

Os dados da aplicação são persistidos em um volume, também criado a partir do **`docker compose`**. Caso este volume seja excluído, ele será recriado na próxima execução do docker compose e as migrações necessárias serão automaticamente executadas.

## 4. Testes

Alternativamente, o comando **`make dev`** cria uma versão de testes da aplicação.
Obs.: Se for a primeira execução, ainda será necessário executar **`docker compose up -d --build`**.

# Documentação

A API possui duas opções de documentação, Swagger UI, disponível em **http://127.0.0.1:8000/docs**, e Redoc, disponível em **http://127.0.0.1:8000/redoc**. O openapi.json está disponível em **http://127.0.0.1:8000/openapi.json** e pode ser importado no **`postman`**.


# Endpoints

## Clientes
### Cadastrar Cliente
```
POST localhost:8000/api/v1/customers

Request body:
    {
  "person": {
    "cpf": "77148752512",
    "name": "string",
    "email": "user@example.com",
    "birth_date": "2025-01-22"
  }
}
```


## Produtos

Endpoints restritos a perfis com permissão de administrador ou gerente.

### Cadastrar Produto

```
POST localhost:8000/api/v1/products

Request body:
{
  "name": "string",
  "description": "string",
  "price": 0,
  "category_id": 1
}
```

### Editar Produto

```
PUT localhost:8000/api/v1/products/{product_id}

Request body:
{
  "id": 0,
  "name": "string",
  "description": "string",
  "price": 0,
  "category_id": 1
}
```

### Remover Produto

```
DELETE localhost:8000/api/v1/products/{product_id}
```

## Pedidos

### Listar Pedidos

```
GET localhost:8000/api/v1/orders
```

# Pagamento

O projeto utiliza a solução de QR Code do Mercado Pago. Foi utilizado um webhook local, criado com a ferramenta [ngrok](https://ngrok.com/), a fim de capturar a resposta da API do Mercado Pago, podendo assim atualizar o status de um pedido quando seu QR Code for criado e quando este for pago.

A página de [documentação](https://dashboard.ngrok.com/get-started/setup/linux) do ngrok contém as instruções de instalação. Após a instalação e execução, a URL gerada deve ser inserida no arquivo `.env`, como valor da variável `WEBHOOK_URL`.

# Passo a Passo - Fluxo do Pedido

Esta seção visa detalhar as chamadas necessárias para executar o fluxo do pedido por completo, da sua criação à sua finalização

## 1. Criar OAuth Token

O primeiro passo necessário é criar um token de autenticação. Apenas clientes podem criar novos pedidos, portanto neste momento a autenticação deve ser feita como cliente.

```
POST localhost:8000/api/auth/token

Request body (form):
username: <CPF>
```

Caso seja necessário autenticar como funcionário, deve-se enviar o nome de usuário e a senha:

```
POST localhost:8000/api/auth/token

Request body (form):
username: <nome de usuário>
password: <senha do usuário>
```


Resposta esperada:

```
{
    "access_token": "<auth token>",
    "token_type": "bearer"
}
```

O token de acesso recebido deve ser usado como autenticação em todas as etapas. Até o pagamento, deve-se estar autenticado como cliente, e após o pagamento, como funcionário.

## 2. Criar novo Pedido

Com o token de acesso do cliente, é possível criar um novo pedido:

```
POST localhost:8000/api/orders
```

Resposta esperada:

```
{
    "id": <id do pedido>,
    "customer": {
        "id": <id do cliente>,
        "person": {
            "id": <id da pessoa relacionada ao cliente>,
            "cpf": "<cpf do cliente>",
            "name": "<nome do cliente>",
            "email": "<e-mail do cliente>",
            "birth_date": "<data de nascimento do cliente>"
        }
    },
    "order_status": {
        "id": 1,
        "status": "order_pending",
        "description": "The order is pending."
    },
    "employee": null,
    "order_items": []
}
```

O ID do pedido será utilizado nas etapas subsequentes.

## 3. Avançar Status do Pedido

Para que seja possível adicionar itens ao pedido, é necessário antes avançar seu status, com a seguinte chamada:

```
POST localhost:8000/api/orders/<id do pedido>/advance
```

Resposta esperada:
```
{
    "id": <id do pedido>,
    "customer": {
        "id": <id do cliente>,
        "person": {
            "id": <id da pessoa relacionada ao cliente>,
            "cpf": "<cpf do cliente>",
            "name": "<nome do cliente>",
            "email": "<e-mail do cliente>",
            "birth_date": "<data de nascimento do cliente>"
        }
    },
    "order_status": {
        "id": 2,
        "status": "order_waiting_burgers",
        "description": "Waiting for a burger."
    },
    "employee": null,
    "order_items": []
}
```

Nota-se que o status do pedido foi atualizado. Neste momento é possível adicionar produtos da categoria "burgers". Na próxima etapa será descrito como fazer isto, além dos produtos disponíveis em cada categoria.

Caso seja necessário retornar ao status anterior, deve ser feita a seguinte chamada:

```
POST localhost:8000/api/orders/<id do pedido>/go-back
```

Alguns dos status não permitem retornar ao status anterior.


## 4. Adicionar Itens ao Pedido

Há 4 status de pedido que permitem a adição de novos itens, um para cada uma das categorias existentes: "order_waiting_burgers", "order_waiting_sides", "order_waiting_drinks" e "order_waiting_desserts".

Para adicionar um item, deve-se primeiro [avançar ou retornar](#3-avançar-status-do-pedido) até o status relacionado à categoria do item e fazer a seguinte chamada:

```
POST localhost:8000/api/orders/<id do pedido>/items

Request body:
{
  "product_id": "<id do produto>",
  "quantity": "<quantidade do produto>",
  "observation": "<observações sobre o preparo>",
  "order_id": "<id do pedido>"
}
```

Produtos disponíveis (ID):
* Burgers: Bacon Cheeseburger (1), Double Cheeseburger (2), Chicken Burger (3), Fish Burger (4)
* Side dishes: Chicken Nuggets (5), Cheese Balls (6), Chicken Wings (7), French Fries (8), Onion Rings (9)
* Drinks: Apple Juice (11), Water (12), Coca-Cola (13)
* Desserts: Vanilla Milkshake (10), Chocolate Smoothie (14), Strawberry Smoothie (15), Pineapple Smoothie (16)

Resposta esperada:
```
{
    "detail": "Item adicionado com sucesso."
}
```

Após passar por todas as etapas de adição de item, o pedido chegará ao status "order_ready_to_place". Este é o último status do qual se pode retornar caso seja necessário atualizar os itens incluídos no pedido. Ao avançar para o próximo status, "order_placed", o pedido estará fechado e pronto para ser pago.

## 5. Pagar o Pedido

Para pagar o pedido, é necessário gerar o QR Code de pagamento, com a seguinte chamada:

```
POST localhost:8000/api/payments/<id do pedido>?payment_method=qr_code
```
Resposta esperada:
```
{
    "payment_id": <id do pagamento>,
    "transaction_id": "<id da transação>",
    "qr_code_link": "<QR code em texto>"
}
```

É necessário gerar a imagem do QR Code, utilizando qualquer ferramenta disponível para geração de QR Code a partir de texto. Após isso, deve-se efetuar o pagamento com uma conta de teste do Mercado Pago.

## 6. Iniciar o Preparo do Pedido

A partir desta etapa, é necessário estar [autenticado como funcionário](#1-criar-oauth-token).

Ao [avançar o status do pedido](#3-avançar-status-do-pedido), caso este já esteja pago e o usuário autenticado seja um funcionário, o id do funcionário sera atribuído ao pedido e seu status sera atualizado para "order_preparing".

Ao continuar avançando, o pedido receberá os status de "order_ready" e "order_completed", nesta ordem. Assim é finalizado o fluxo de criação, preparação e entrega de um pedido.


# Diagrama de Contexto do sistema

![image](https://github.com/user-attachments/assets/6d49ecc1-b854-4455-b442-b8b418b330c0)


# Diagrama de conteiner

![image](https://github.com/user-attachments/assets/ee16a5f5-9222-4daa-9db6-635e7652dd10)


# Diagrama de Componentes

![image](https://github.com/user-attachments/assets/da0d9d5b-0e51-4bcd-ab25-b9ddec3491e7)
