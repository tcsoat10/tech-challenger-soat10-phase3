"""Merge branch 'heads/6787f5df0f04' and 'heads/d930883ec3eb'

Revision ID: 134c95b25c36
Revises: 6787f5df0f04, d930883ec3eb
Create Date: 2024-12-31 01:31:06.431149

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '134c95b25c36'
down_revision: Union[str, None] = ('6787f5df0f04', 'd930883ec3eb')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
