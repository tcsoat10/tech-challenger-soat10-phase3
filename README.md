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
    
No diretório definido para armazenar os arquivos do projeto, executar o comando `git clone XXXXXXXX`.

## 2. Arquivo .env

O arquivo .env contém valores necessários para a execução do projeto, como senhas e variáveis de ambiente. Ele não deve ser salvo no repositório remoto, e é necessário que seja alocado no diretório raiz do projeto.

## 3.1. Docker Compose (produção)

Após verificar que a Docker Engine está ativa, executar o comando **`docker compose up -d --build`** no diretório raiz do projeto. Este comando sobe a aplicação e o banco de dados seguindo as instruções definidas no arquivo **`docker-compose.yml`**.

Dois containers serão executados dentro de uma única rede, um para o banco de dados MySQL e um para a aplicação. O container da aplicação tem sua imagem construída a partir do **`Dockerfile`** presente no projeto.

Os dados da aplicação são persistidos em um volume, também criado a partir do **`docker compose`**. Caso este volume seja excluído, ele será recriado na próxima execução do docker compose e as migrações necessárias serão automaticamente executadas.

## 4. Testes

Alternativamente, o comando **`make dev`** cria uma versão de testes da aplicação.


# Documentação

A API possui duas opções de documentação, Swagger UI, disponível em **http://127.0.0.1:8000/docs**, e Redoc, disponível em **http://127.0.0.1:8000/redoc**


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