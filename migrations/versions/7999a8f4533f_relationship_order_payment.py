"""relationship order payment

Revision ID: 7999a8f4533f
Revises: 3ea8f2d1c9b7
Create Date: 2025-01-20 20:38:18.869731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7999a8f4533f'
down_revision: Union[str, None] = '3ea8f2d1c9b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payments', sa.Column('amount', sa.Float(), nullable=False))
    op.add_column('payments', sa.Column('external_reference', sa.String(length=500), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payments', 'external_reference')
    op.drop_column('payments', 'amount')
    # ### end Alembic commands ###
