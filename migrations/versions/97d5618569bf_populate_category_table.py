"""populate category table

Revision ID: 97d5618569bf
Revises: 97c5618569bf
Create Date: 2025-01-18 18:15:12.951580

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column
from sqlalchemy import String, Integer

# Revisão e informações básicas da migração
revision = '97d5618569bf'
down_revision: Union[str, None] = '97c5618569bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

categories_table = table(
    'categories',
    column('id', Integer),
    column('name', String),
    column('description', String)
)

categories = [
    {"name": "burgers", "description": "meat, chicken and fish burgers"},
    {"name": "drinks", "description": "soda, juice, water and beers"},
    {"name": "side dishes", "description": "fries, onions, chicken nuggets"},
    {"name": "desserts", "description": "ice cream and smoothies"},
]

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return
    
    op.bulk_insert(categories_table, categories)

def downgrade():
    op.execute(
        "DELETE FROM categories WHERE name IN ('burgers', 'drinks', 'side dishes', 'desserts')"
    )
