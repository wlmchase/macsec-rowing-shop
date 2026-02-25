"""remove_order_status

Revision ID: e6e5275db81a
Revises: 047299503a2b
Create Date: 2025-03-22 08:50:01.240943

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6e5275db81a'
down_revision: Union[str, None] = '047299503a2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('order_items', 'price')


def downgrade() -> None:
    """Downgrade schema."""
    sa.Column('price', sa.Float(), nullable=False)

