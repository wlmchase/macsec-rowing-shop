"""add shipping info zipcode column

Revision ID: add_shipping_info_zipcode
Revises: add_shipping_info_unit
Create Date: 2024-03-22 12:25:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_shipping_info_zipcode'
down_revision = 'add_shipping_info_unit'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add zipcode column to shipping_info table
    op.add_column('shipping_info', sa.Column('zipcode', sa.String(), nullable=False))


def downgrade() -> None:
    # Remove the zipcode column
    op.drop_column('shipping_info', 'zipcode') 