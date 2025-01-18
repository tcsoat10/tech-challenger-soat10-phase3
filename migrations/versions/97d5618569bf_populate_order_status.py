"""populate order status

Revision ID: 97d5618569bf
Revises: 1ec56060d33c
Create Date: 2025-01-18 17:37:12.951580

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

from src.constants.order_status import OrderStatusEnum


revision = '97d5618569bf'
down_revision: Union[str, None] = '1ec56060d33c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

order_status_table = table(
    'order_status',
    column('id', Integer),
    column('status', String),
    column('description', String)
)

order_statuses = [*OrderStatusEnum.values_and_descriptions()]

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    op.bulk_insert(order_status_table, order_statuses)


def downgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    op.execute(
        f"DELETE FROM order_status WHERE status IN ({', '.join([f'\'{order_status.status}\'' for order_status in OrderStatusEnum])})"
    )
