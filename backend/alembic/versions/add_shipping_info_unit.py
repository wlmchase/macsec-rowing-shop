"""add shipping info unit column

Revision ID: add_shipping_info_unit
Revises: drop_billing_info
Create Date: 2024-03-22 12:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_shipping_info_unit'
down_revision = 'drop_billing_info'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add unit column to shipping_info table
    op.add_column('shipping_info', sa.Column('unit', sa.String(), nullable=True))


def downgrade() -> None:
    # Remove the unit column
    op.drop_column('shipping_info', 'unit') 