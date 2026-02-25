"""update_orders

Revision ID: 572f61ae43f3
Revises: initial_migration
Create Date: 2025-03-22 08:17:01.908472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '572f61ae43f3'
down_revision: Union[str, None] = 'initial_migration'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('orders', sa.Column('total_price', sa.Float(), nullable=False))
    op.alter_column('orders', 'created_at',
                    type_=sa.DateTime(timezone=True),
                    existing_type=sa.DateTime(),
                    existing_nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('orders', 'total_price')
    op.alter_column('orders', 'created_at',
                    type_=sa.DateTime(),
                    existing_type=sa.DateTime(timezone=True),
                    existing_nullable=False)
