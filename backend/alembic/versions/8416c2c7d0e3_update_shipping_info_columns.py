"""update_shipping_info_columns

Revision ID: 8416c2c7d0e3
Revises: drop_billing_info
Create Date: 2025-03-22 09:13:45.543222

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8416c2c7d0e3'
down_revision: Union[str, None] = '159c8a58a353'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add first_name and last_name columns to shipping_info table
    op.add_column('shipping_info', sa.Column('first_name', sa.String(), nullable=True))
    op.add_column('shipping_info', sa.Column('last_name', sa.String(), nullable=True))
    op.add_column('shipping_info', sa.Column('email', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove the columns in reverse order
    op.drop_column('shipping_info', 'email')
    op.drop_column('shipping_info', 'last_name')
    op.drop_column('shipping_info', 'first_name') 
