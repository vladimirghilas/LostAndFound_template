"""add users

Revision ID: 5f06e47a78f8
Revises: 3c0bb7481907
Create Date: 2025-09-24 11:30:10.285452

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5f06e47a78f8'
down_revision: Union[str, None] = '3c0bb7481907'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("username", sa.String, nullable=False, unique=True, index=True),
        sa.Column("email", sa.String, unique=True, index=True),
        sa.Column("full_name", sa.String),
        sa.Column("hashed_password", sa.String, nullable=False),
        sa.Column("is_active", sa.Integer, server_default="1", nullable=False),
        sa.Column("created_at", sa.DateTime, server_default=sa.func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")