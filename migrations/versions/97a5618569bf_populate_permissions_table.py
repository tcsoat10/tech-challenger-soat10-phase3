"""populate permissions table

Revision ID: 97a5618569bf
Revises: af6a351d5427
Create Date: 2025-01-11 18:21:12.951580

"""

from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String

# Revisão e informações básicas da migração
revision = '97a5618569bf'
down_revision: Union[str, None] = 'af6a351d5427'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

permissions_table = table(
    'permissions',
    column('id', String),
    column('name', String),
    column('description', String)
)

permissions = [
    # Categories
    {"name": "can_create_category", "description": "Permission to create a category"},
    {"name": "can_view_categories", "description": "Permission to view all categories"},
    {"name": "can_view_category_by_name", "description": "Permission to view category by name"},
    {"name": "can_view_category_by_id", "description": "Permission to view category by ID"},
    {"name": "can_update_category", "description": "Permission to update a category"},
    {"name": "can_delete_category", "description": "Permission to delete a category"},

    # Products
    {"name": "can_create_product", "description": "Permission to create a product"},
    {"name": "can_view_products", "description": "Permission to view all products"},
    {"name": "can_view_product_by_name", "description": "Permission to view product by name"},
    {"name": "can_view_product_by_id", "description": "Permission to view product by ID"},
    {"name": "can_update_product", "description": "Permission to update a product"},
    {"name": "can_delete_product", "description": "Permission to delete a product"},

    # Order Items
    {"name": "can_create_order_item", "description": "Permission to create an order item"},
    {"name": "can_view_order_items", "description": "Permission to view all order items"},
    {"name": "can_view_order_item_by_id", "description": "Permission to view order item by ID"},
    {"name": "can_update_order_item", "description": "Permission to update an order item"},
    {"name": "can_delete_order_item", "description": "Permission to delete an order item"},

    # Permissions
    {"name": "can_create_permission", "description": "Permission to create a permission"},
    {"name": "can_view_permissions", "description": "Permission to view all permissions"},
    {"name": "can_view_permission_by_name", "description": "Permission to view permission by name"},
    {"name": "can_view_permission_by_id", "description": "Permission to view permission by ID"},
    {"name": "can_update_permission", "description": "Permission to update a permission"},
    {"name": "can_delete_permission", "description": "Permission to delete a permission"},

    # Profiles
    {"name": "can_create_profile", "description": "Permission to create a profile"},
    {"name": "can_view_profiles", "description": "Permission to view all profiles"},
    {"name": "can_view_profile_by_name", "description": "Permission to view profile by name"},
    {"name": "can_view_profile_by_id", "description": "Permission to view profile by ID"},
    {"name": "can_update_profile", "description": "Permission to update a profile"},
    {"name": "can_delete_profile", "description": "Permission to delete a profile"},

    # Profile Permissions
    {"name": "can_create_profile_permission", "description": "Permission to create a profile permission"},
    {"name": "can_view_profile_permissions", "description": "Permission to view all profile permissions"},
    {"name": "can_view_profile_permission_by_id", "description": "Permission to view profile permission by ID"},
    {"name": "can_view_profile_permission_by_permission_id", "description": "Permission to view profile permission by permission ID"},
    {"name": "can_view_profile_permission_by_profile_id", "description": "Permission to view profile permission by profile ID"},
    {"name": "can_update_profile_permission", "description": "Permission to update a profile permission"},
    {"name": "can_delete_profile_permission", "description": "Permission to delete a profile permission"},

    # Payment Methods
    {"name": "can_create_payment_method", "description": "Permission to create a payment method"},
    {"name": "can_view_payment_methods", "description": "Permission to view all payment methods"},
    {"name": "can_view_payment_method_by_name", "description": "Permission to view payment method by name"},
    {"name": "can_view_payment_method_by_id", "description": "Permission to view payment method by ID"},
    {"name": "can_update_payment_method", "description": "Permission to update a payment method"},
    {"name": "can_delete_payment_method", "description": "Permission to delete a payment method"},

    # Roles
    {"name": "can_create_role", "description": "Permission to create a role"},
    {"name": "can_view_roles", "description": "Permission to view all roles"},
    {"name": "can_view_role_by_name", "description": "Permission to view role by name"},
    {"name": "can_view_role_by_id", "description": "Permission to view role by ID"},
    {"name": "can_update_role", "description": "Permission to update a role"},
    {"name": "can_delete_role", "description": "Permission to delete a role"},

    # Payment Status
    {"name": "can_create_payment_status", "description": "Permission to create a payment status"},
    {"name": "can_view_payment_statuses", "description": "Permission to view all payment statuses"},
    {"name": "can_view_payment_status_by_name", "description": "Permission to view payment status by name"},
    {"name": "can_view_payment_status_by_id", "description": "Permission to view payment status by ID"},
    {"name": "can_update_payment_status", "description": "Permission to update a payment status"},
    {"name": "can_delete_payment_status", "description": "Permission to delete a payment status"},

    # Users
    {"name": "can_create_user", "description": "Permission to create a user"},
    {"name": "can_view_users", "description": "Permission to view all users"},
    {"name": "can_view_user_by_name", "description": "Permission to view user by name"},
    {"name": "can_view_user_by_id", "description": "Permission to view user by ID"},
    {"name": "can_update_user", "description": "Permission to update a user"},
    {"name": "can_delete_user", "description": "Permission to delete a user"},

    # User Profiles
    {"name": "can_create_user_profile", "description": "Permission to create a user profile"},
    {"name": "can_view_user_profiles", "description": "Permission to view all user profiles"},
    {"name": "can_view_user_profile_by_id", "description": "Permission to view user profile by ID"},
    {"name": "can_view_user_profile_by_user_id_and_profile_id", "description": "Permission to view user profile by user and profile IDs"},
    {"name": "can_update_user_profile", "description": "Permission to update a user profile"},
    {"name": "can_delete_user_profile", "description": "Permission to delete a user profile"}
]


def upgrade():
    op.bulk_insert(permissions_table, permissions)


def downgrade():
    op.execute("DELETE FROM roles WHERE name LIKE 'can_%'")
