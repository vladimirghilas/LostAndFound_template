"""merge category heads

Revision ID: 3b73cf827432
Revises: 6842545efdd5, 997f18b6be3d
Create Date: 2025-09-23 11:37:58.039872

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b73cf827432'
down_revision: Union[str, None] = ('6842545efdd5', '997f18b6be3d')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
