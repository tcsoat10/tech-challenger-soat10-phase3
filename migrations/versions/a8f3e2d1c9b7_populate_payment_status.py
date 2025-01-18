"""populate payment status

Revision ID: a8f3e2d1c9b7
Revises: 97d5618569bf
Create Date: 2025-01-18 17:50:12.951580

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

from src.constants.payment_status import PaymentStatusEnum


revision = 'a8f3e2d1c9b7'
down_revision: Union[str, None] = '97d5618569bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

payment_status_table = table(
    'payment_status',
    column('id', Integer),
    column('name', String),
    column('description', String)
)

payment_statuses = [*PaymentStatusEnum.values_and_descriptions()]

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    op.bulk_insert(payment_status_table, payment_statuses)


def downgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    delete_query = f"DELETE FROM payment_status WHERE name IN ({', '.join([f'\'{payment_status.status}\'' for payment_status in PaymentStatusEnum])})"
    op.execute(delete_query)
