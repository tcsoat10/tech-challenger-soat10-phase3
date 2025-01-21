"""populate payment method table

Revision ID: 97l5618569bf
Revises: b6dfcf4e95ee
Create Date: 2025-01-19 13:31:12.951580

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column, select
from sqlalchemy import String, Integer, MetaData


# Revisão e informações básicas da migração
revision = '97l5618569bf'
down_revision: Union[str, None] = 'b6dfcf4e95ee'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

payment_methods_table = table(
    'payment_methods',
    column('name', String),
    column('description', String)
)


payment_methods = [
    {
        'name': 'QR Code',
        'description': 'Payment via Mercado Pago QR Code'
    }
]
    

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    op.bulk_insert(payment_methods_table, payment_methods)

def downgrade():
    op.execute(
        "DELETE FROM payment_methods WHERE name IN ('QR Code')"
    )
