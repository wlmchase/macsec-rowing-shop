"""make_order_items_price_nullable

Revision ID: e2a5a6a54791
Revises: e6e5275db81a
Create Date: 2025-03-22 08:55:02.199533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e2a5a6a54791'
down_revision: Union[str, None] = 'e6e5275db81a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
