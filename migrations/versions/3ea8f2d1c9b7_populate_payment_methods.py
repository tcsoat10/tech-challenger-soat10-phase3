"""populate payment methods

Revision ID: 3ea8f2d1c9b7
Revises: b6dfcf4e95ee
Create Date: 2025-01-18 17:50:12.951580

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

from src.constants.payment_method_enum import PaymentMethodEnum

revision = '3ea8f2d1c9b7'
down_revision: Union[str, None] = 'b6dfcf4e95ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

payment_methods_table = table(
    'payment_methods',
    column('id', Integer),
    column('name', String),
    column('description', String)
)

payment_methods = [*PaymentMethodEnum.values_and_descriptions()]

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    op.bulk_insert(payment_methods_table, payment_methods)


def downgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    delete_query = f"DELETE FROM payment_methods WHERE name IN ({', '.join([f'\'{payment_method.name}\'' for payment_method in PaymentMethodEnum])})"
    op.execute(delete_query)
