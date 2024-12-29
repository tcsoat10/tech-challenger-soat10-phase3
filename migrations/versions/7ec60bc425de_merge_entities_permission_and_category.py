"""Merge entities Permission and Category

Revision ID: 7ec60bc425de
Revises: 52506b356108, 960b06e32f16
Create Date: 2024-12-28 22:26:24.866834

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ec60bc425de'
down_revision: Union[str, None] = ('52506b356108', '960b06e32f16')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
