"""populate product table

Revision ID: 97e5618569bf
Revises: 97d5618569bf
Create Date: 2025-01-18 18:32:12.951580

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column, select
from sqlalchemy import String, Integer, Float, MetaData

# Revisão e informações básicas da migração
revision = '97e5618569bf'
down_revision: Union[str, None] = '97d5618569bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

products_table = table(
    'products',
    column('id', Integer),
    column('name', String),
    column('description', String),
    column('category_id', Integer),
    column('price', Float),
    column('sla_product', String)
)

categories_table = table(
    'categories',
    column('id', Integer),
    column('name', String),
)


products =[
    {
        'name': 'Bacon Cheeseburger',
        'description': 'single patty, cheese, bacon',
        'category': 'burgers',
        'price': '25.00',
        'sla_product': '8 min'
    },
    {
        'name': 'French Fries',
        'description': 'medium sized french fries',
        'category': 'side dishes',
        'price': '8.00',
        'sla_product': '2 min'
    },
    {
        'name': 'Coca-Cola',
        'description': '500 ml Coca-Cola cup',
        'category': 'drinks',
        'price': '3.00',
        'sla_product': '1 min'
    },
    {
        'name': 'Chocolate smoothie',
        'description': '400 ml smoothie',
        'category': 'desserts',
        'price': '10.00',
        'sla_product': '4 min'
    }
]

def upgrade():
    if os.getenv("ENVIRONMENT") == "testing":
        return

    connection = op.get_bind()
    metadata = MetaData()
    metadata.reflect(bind=connection)
    
    categories_mapping = {}
    result = connection.execute(select(categories_table.c.id, categories_table.c.name))
    for row in result:
        categories_mapping[row[1]] = row[0]

    insert_data = []
    for product in products:
        category_id = categories_mapping.get(product['category'])
        if category_id:
            insert_data.append({
                'name': product['name'],
                'description': product['description'],
                'category_id': category_id,
                'price': product['price'],
                'sla_product': product['sla_product']
            })

    
    op.bulk_insert(products_table, insert_data)

def downgrade():
    op.execute(
        "DELETE FROM products WHERE name IN ('Bacon Cheeseburger')"
    )
