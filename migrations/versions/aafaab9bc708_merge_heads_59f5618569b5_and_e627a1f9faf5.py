"""empty message

Revision ID: aafaab9bc708
Revises: 59f5618569b5, e627a1f9faf5
Create Date: 2025-01-05 20:27:19.217061

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aafaab9bc708'
down_revision: Union[str, None] = ('59f5618569b5', 'e627a1f9faf5')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
