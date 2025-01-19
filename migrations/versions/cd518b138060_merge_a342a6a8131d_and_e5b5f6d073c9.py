"""empty message

Revision ID: cd518b138060
Revises: a342a6a8131d, e5b5f6d073c9
Create Date: 2025-01-19 12:18:14.496772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cd518b138060'
down_revision: Union[str, None] = ('a342a6a8131d', 'e5b5f6d073c9')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
