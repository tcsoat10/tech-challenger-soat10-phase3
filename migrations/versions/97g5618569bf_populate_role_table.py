"""populate role table

Revision ID: 97g5618569bf
Revises: cd518b138060
Create Date: 2025-01-19 13:31:12.951580

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column, select
from sqlalchemy import String, Integer, Float, MetaData

# Revisão e informações básicas da migração
revision = '97g5618569bf'
down_revision: Union[str, None] = 'cd518b138060'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

roles_table = table(
    'roles',
    column('id', Integer),
    column('name', String),
    column('description', String)
)


roles = [
    {'name': 'manager', 'description': 'store manager with full access'},
    {'name': 'employee', 'description': 'store employee with restricted access'}
]


def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    op.bulk_insert(roles_table, roles)

def downgrade():
    op.execute(
        "DELETE FROM roles WHERE name IN ('manager', 'employee')"
    )
