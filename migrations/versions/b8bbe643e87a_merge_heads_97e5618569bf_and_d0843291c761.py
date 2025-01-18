"""empty message

Revision ID: b8bbe643e87a
Revises: 97e5618569bf, d0843291c761
Create Date: 2025-01-12 12:14:44.706667

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b8bbe643e87a'
down_revision: Union[str, None] = ('97e5618569bf', 'd0843291c761')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
