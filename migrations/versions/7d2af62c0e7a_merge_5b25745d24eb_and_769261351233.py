"""Merge branch 'heads/5b25745d24eb' and 'heads/769261351233'

Revision ID: 7d2af62c0e7a
Revises: 5b25745d24eb, 769261351233
Create Date: 2024-12-31 17:51:41.259774

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d2af62c0e7a'
down_revision: Union[str, None] = ('5b25745d24eb', '769261351233')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
