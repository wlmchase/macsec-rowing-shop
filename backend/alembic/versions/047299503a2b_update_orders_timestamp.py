"""update_orders_timestamp

Revision ID: 047299503a2b
Revises: 572f61ae43f3
Create Date: 2025-03-22 08:24:56.037262

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '047299503a2b'
down_revision: Union[str, None] = '572f61ae43f3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Remove the status column from orders table
    op.drop_column('orders', 'status')


def downgrade() -> None:
    """Downgrade schema."""
    # Add back the status column to orders table
    op.add_column('orders', sa.Column('status', sa.String(), nullable=True))
