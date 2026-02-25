"""rename zipcode to zip_code

Revision ID: rename_zipcode_to_zip_code
Revises: add_shipping_info_zipcode
Create Date: 2024-03-22 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'rename_zipcode_to_zip_code'
down_revision = 'add_shipping_info_zipcode'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the zipcode column since zip_code already exists
    op.drop_column('shipping_info', 'zipcode')


def downgrade() -> None:
    # Add back the zipcode column
    op.add_column('shipping_info', sa.Column('zipcode', sa.String(), nullable=False)) 