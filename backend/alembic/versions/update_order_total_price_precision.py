"""update order total price precision

Revision ID: update_price_precision
Revises: rename_zipcode_to_zip_code
Create Date: 2024-03-21 22:57:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'update_price_precision'
down_revision = 'rename_zipcode_to_zip_code'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # Update the total_price column to use decimal precision
    op.alter_column('orders', 'total_price',
        type_=sa.Numeric(precision=10, scale=2),
        existing_type=sa.Float(),
        postgresql_using='total_price::numeric(10,2)'
    )

def downgrade() -> None:
    # Revert back to float type
    op.alter_column('orders', 'total_price',
        type_=sa.Float(),
        existing_type=sa.Numeric(precision=10, scale=2),
        postgresql_using='total_price::float'
    ) 