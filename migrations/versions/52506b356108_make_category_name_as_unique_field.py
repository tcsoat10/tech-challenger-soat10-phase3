"""Make category name as unique field

Revision ID: 52506b356108
Revises: d4cfda9a0fb4
Create Date: 2024-12-26 23:59:00.500194

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52506b356108'
down_revision: Union[str, None] = 'd4cfda9a0fb4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define um nome para a constraint
constraint_name = 'uq_categories_name'

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        # Usa o nome definido
        batch_op.create_unique_constraint(constraint_name, ['name'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('categories', schema=None) as batch_op:
        # Usa o mesmo nome para remover
        batch_op.drop_constraint(constraint_name, type_='unique')
    # ### end Alembic commands ###