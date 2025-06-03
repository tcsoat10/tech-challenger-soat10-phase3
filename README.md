# Tech Challenge - Grupo 30 SOAT10 - Pós Tech Arquitetura de Software - FIAP


# Descrição do Projeto

O projeto visa atender à demanda de uma lanchonete de bairro, que, devido ao seu sucesso, necessita implementar um sistema de autoatendimento. 

Esta aplicação é parte de um ecossistema distribuído em quatro repositórios, executando inteiramente na AWS, com deploy via Terraform.

# Conteúdo

- [Tech Challenge - Grupo 30 SOAT10 - Pós Tech Arquitetura de Software - FIAP](#tech-challenge---grupo-30-soat10---pós-tech-arquitetura-de-software---fiap)
- [Descrição do Projeto](#descrição-do-projeto)
- [Conteúdo](#conteúdo)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Executando o Projeto](#executando-o-projeto)
- [Comunicação com os demais serviços](#comunicação-com-os-demais-serviços)
- [Secrets Necessários](#secrets-necessários)

# Tecnologias Utilizadas
- [Python 3.12](https://www.python.org/downloads/)
- [FastAPI](https://fastapi.tiangolo.com/)- 
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Alembic](https://alembic.sqlalchemy.org/)
- [MySQL](https://www.mysql.com/)
- [Kubernetes](https://kubernetes.io/)
- [Terraform](https://developer.hashicorp.com/terraform)
- [AWS RDS](https://aws.amazon.com/pt/rds/)
- [AWS EKS](https://aws.amazon.com/pt/eks/)
- [AWS Lambda](https://aws.amazon.com/pt/lambda/)
- [AWS Api Gateway](https://aws.amazon.com/pt/api-gateway/)
- [Github Actions](https://github.com/features/actions)

# Executando o Projeto
Este projeto não é executado localmente. O deploy ocorre automaticamente na AWS via GitHub Actions, fazendo uso do Terraform.

Este repositório contém apenas o código fonte da aplicação. Os demais repositórios contém a infraestrutura [Kubernetes](https://github.com/tcsoat10/tech-challenger-soat10-phase3-k8s), a infraestrutura de [banco de dados](https://github.com/tcsoat10/tech-challenger-soat10-phase3-db) e a [função Lambda](https://github.com/tcsoat10/tech-challenger-soat10-phase3-lambda) utilizada para autenticação de usuários.

# Comunicação com os demais serviços

- A função AWS Lambda é acessível por meio de um AWS API Gateway integrado a ela, o endpoint da API é configurado como um secret no repositório da aplicação.
- O deploy da infra Kubernetes é feito em um cluster EKS. Dentro deste cluster, o deploy da aplicação é feito em um pod, e tem seu acesso gerenciado por um Load Balancer.
- O deploy do banco de dados libera o acesso do grupo de segurança do pod com a aplicação durante sua execução.
- A aplicação enxerga o banco de dados disponível e realiza as migrações necessárias.

# Secrets Necessários
- AWS_SESSION_TOKEN
- XXXXX

