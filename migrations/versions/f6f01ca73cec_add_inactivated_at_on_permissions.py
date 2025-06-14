"""Add inactivated_at on permissions

Revision ID: f6f01ca73cec
Revises: 134c95b25c36
Create Date: 2024-12-31 01:38:06.915583

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f6f01ca73cec'
down_revision: Union[str, None] = '134c95b25c36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('permissions', sa.Column('inactivated_at', sa.DateTime(timezone=True), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('permissions', 'inactivated_at')
    # ### end Alembic commands ###
