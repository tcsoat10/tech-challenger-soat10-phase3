"""empty message

Revision ID: a342a6a8131d
Revises: 97f5618569bf, a8f3e2d1c9b7
Create Date: 2025-01-18 21:34:39.859907

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a342a6a8131d'
down_revision: Union[str, None] = ('97f5618569bf', 'a8f3e2d1c9b7')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
