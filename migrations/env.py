from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from config.database import DATABASE
from src.core.domain.entities import BaseEntity 


# Carrega a configuração do Alembic
config = context.config
fileConfig(config.config_file_name)

# Geração da URL do banco de dados
database_url = (
    f"{DATABASE['drivername']}://{DATABASE['user']}:{DATABASE['password']}@"
    f"{DATABASE['host']}:{DATABASE['port']}/{DATABASE['name']}"
)
config.set_main_option("sqlalchemy.url", database_url)

# Metadados das tabelas (BaseEntity como base para todas as entidades)
target_metadata = BaseEntity.metadata

# Modo offline: Gera SQL sem conexão ao banco
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()

# Modo online: Executa as migrações com conexão ativa ao banco
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
