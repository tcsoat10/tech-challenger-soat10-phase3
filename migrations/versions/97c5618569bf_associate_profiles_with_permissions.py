"""associate profiles with permissions

Revision ID: 97c5618569bf
Revises: 97b5618569bf
Create Date: 2025-01-11 18:45:12.951580

"""

from alembic import op
from sqlalchemy.sql import table, column, select
from sqlalchemy import Integer, String, DateTime, MetaData
from datetime import datetime, timezone

# Revisão e informações básicas da migração
revision = '97c5618569bf'
down_revision = '97b5618569bf'
branch_labels = None
depends_on = None

# Tabela de referência
profile_permissions_table = table(
    'profile_permissions',
    column('profile_id', String),
    column('permission_id', String),
    column('created_at', DateTime)
)

permissions_table = table(
    'permissions',
    column('id', Integer),
    column('name', String)
)


# Perfis e permissões associadas
profile_permissions = {
    "1": [  # Administrator: todas as permissões
        "can_create_category", "can_view_categories", "can_update_category", "can_delete_category",
        "can_create_product", "can_view_products", "can_update_product", "can_delete_product",
        "can_create_order_item", "can_view_order_items", "can_update_order_item", "can_delete_order_item",
        "can_create_order", "can_view_order", "can_update_order", "can_delete_order",
        "can_create_order_status", "can_view_order_status", "can_update_order_status", "can_delete_order_status",
        "can_create_permission", "can_view_permissions", "can_update_permission", "can_delete_permission",
        "can_create_profile", "can_view_profiles", "can_update_profile", "can_delete_profile",
        "can_create_profile_permission", "can_view_profile_permissions", "can_update_profile_permission", "can_delete_profile_permission",
        "can_create_payment_method", "can_view_payment_methods", "can_update_payment_method", "can_delete_payment_method",
        "can_create_payment", "can_view_payments", "can_update_payment", "can_delete_payment",
        "can_create_payment_status", "can_view_payment_statuses", "can_update_payment_status", "can_delete_payment_status",
        "can_create_role", "can_view_roles", "can_update_role", "can_delete_role",
        "can_create_user", "can_view_users", "can_update_user", "can_delete_user",
        "can_create_user_profile", "can_view_user_profiles", "can_update_user_profile", "can_delete_user_profile"
    ],
    "2": [  # Employee: acesso limitado
        "can_view_categories", "can_update_category",  # Apenas visualiza e atualiza categorias
        "can_view_products", "can_update_product",  # Apenas visualiza e atualiza produtos
        "can_create_order_item", "can_view_order_items", "can_update_order_item", "can_delete_order_item",  # Gerencia itens de pedidos
        "can_view_order",  # Pode visualizar pedidos
        "can_view_order_status", "can_update_order_status",  # Pode visualizar e atualizar status de pedidos
        "can_view_permissions",  # Apenas visualização
        "can_view_profiles",  # Apenas visualização
        "can_view_profile_permissions",  # Apenas visualização de permissões de perfis
        "can_view_roles",  # Apenas visualização de roles
        "can_view_payment_methods",  # Apenas visualização de métodos de pagamento
        "can_view_payment_statuses", "can_update_payment_statuses",  # Pode visualizar e atualizar status de pagamentos
        "can_view_users",  # Apenas visualização de usuários
        "can_view_user_profiles"  # Apenas visualização de perfis de usuários
    ],
    "3": [  # Client: acesso mínimo
        "can_create_order", "can_view_order",  # Pode criar e visualizar pedidos
        "can_create_order_item", "can_view_order_items",  # Pode criar e visualizar itens de pedidos
        "can_view_categories",  # Apenas visualização de categorias
        "can_view_products",  # Apenas visualização de produtos
        "can_create_user_profile", "can_view_user_profiles"  # Pode criar e visualizar perfis relacionados ao cliente
        "can_create_payment", "can_view_payments"  # Pode criar e visualizar pagamentos
    ]
}

def upgrade():
    connection = op.get_bind()
    metadata = MetaData()
    metadata.reflect(bind=connection)

    permissions_mapping = {}
    result = connection.execute(select(permissions_table.c.id, permissions_table.c.name))
    for row in result:
        permissions_mapping[row[1]] = row[0]

    insert_data = []
    for profile_id, permissions in profile_permissions.items():
        for permission_name in permissions:
            permission_id = permissions_mapping.get(permission_name)
            if permission_id:
                insert_data.append({
                    "profile_id": int(profile_id),
                    "permission_id": permission_id,
                    "created_at": datetime.now(timezone.utc)
                })

    op.bulk_insert(profile_permissions_table, insert_data)


def downgrade():
    op.execute("DELETE FROM profile_permissions WHERE profile_id IN ('1', '2', '3')")