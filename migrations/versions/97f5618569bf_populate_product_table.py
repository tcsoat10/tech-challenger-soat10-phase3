"""populate product table

Revision ID: 97f5618569bf
Revises: 97e5618569bf
Create Date: 2025-01-18 18:32:12.951580

"""

import os
from typing import Sequence, Union
from alembic import op
from sqlalchemy.sql import table, column, select
from sqlalchemy import String, Integer, Float, MetaData

from src.constants.product_category import ProductCategoryEnum

# Revisão e informações básicas da migração
revision = '97f5618569bf'
down_revision: Union[str, None] = '97e5618569bf'
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
        'category': ProductCategoryEnum.BURGERS.name,
        'price': '25.00',
        'sla_product': '8 min'
    },
    {
        'name': 'Double Cheeseburger',
        'description': 'double patty, cheese',
        'category': ProductCategoryEnum.BURGERS.name,
        'price': '30.00',
        'sla_product': '10 min'
    },
    {
        'name': 'Chicken Burger',
        'description': 'single patty, cheese, bacon',
        'category': ProductCategoryEnum.BURGERS.name,
        'price': '20.00',
        'sla_product': '6 min'
    },
    {
        'name': 'Fish Burger',
        'description': 'single patty, cheese, bacon',
        'category': ProductCategoryEnum.BURGERS.name,
        'price': '22.00',
        'sla_product': '7 min'
    },
    {
        'name': 'Chicken Nuggets',
        'description': '10 chicken nuggets',
        'category': ProductCategoryEnum.SIDES.name,
        'price': '15.00',
        'sla_product': '4 min'
    },
    {
        'name': 'Cheese Balls',
        'description': '10 cheese balls',
        'category': ProductCategoryEnum.SIDES.name,
        'price': '18.00',
        'sla_product': '5 min',
    },
    {
        'name': 'Chicken Wings',
        'description': '6 chicken wings',
        'category': ProductCategoryEnum.SIDES.name,
        'price': '20.00',
        'sla_product': '6 min'
    },
    {
        'name': 'French Fries',
        'description': 'medium sized french fries',
        'category': ProductCategoryEnum.SIDES.name,
        'price': '8.00',
        'sla_product': '2 min'
    },
    {
        'name': 'Onion Rings',
        'description': '12 onion rings',
        'category': ProductCategoryEnum.SIDES.name,
        'price': '12.00',
        'sla_product': '3 min'
    },
    {
        'name': 'Vanilla Milkshake',
        'description': '500 ml milkshake',
        'category': ProductCategoryEnum.DESSERTS.name,
        'price': '15.00',
        'sla_product': '5 min'
    },
    {
        'name': 'Apple Juice',
        'description': '500 ml apple juice',
        'category': ProductCategoryEnum.DRINKS.name,
        'price': '5.00',
        'sla_product': '1 min'
    },
    {
        'name': 'Water',
        'description': '500 ml water bottle',
        'category': ProductCategoryEnum.DRINKS.name,
        'price': '2.00',
        'sla_product': '1 min'
    },
    {
        'name': 'Coca-Cola',
        'description': '500 ml Coca-Cola cup',
        'category': ProductCategoryEnum.DRINKS.name,
        'price': '3.00',
        'sla_product': '1 min'
    },
    {
        'name': 'Chocolate smoothie',
        'description': '400 ml smoothie',
        'category': ProductCategoryEnum.DESSERTS.name,
        'price': '10.00',
        'sla_product': '4 min'
    },
    {
        'name': 'Strawberry smoothie',
        'description': '400 ml smoothie',
        'category': ProductCategoryEnum.DESSERTS.name,
        'price': '10.00',
        'sla_product': '4 min'
    },
    {
        'name': 'Pineapple smoothie',
        'description': '400 ml smoothie',
        'category': ProductCategoryEnum.DESSERTS.name,
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
    product_names = [product['name'] for product in products]
    formatted_names = ', '.join(f"'{name}'" for name in product_names)
    op.execute(f"DELETE FROM products WHERE name IN ({formatted_names})")
