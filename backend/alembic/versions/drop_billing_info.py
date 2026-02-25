"""drop billing info table

Revision ID: drop_billing_info
Revises: add_shipping_info_columns
Create Date: 2024-03-22 12:15:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'drop_billing_info'
down_revision = '8416c2c7d0e3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Drop the billing_info table
    op.drop_table('billing_info')


def downgrade() -> None:
    # Recreate the billing_info table
    op.create_table('billing_info',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('order_id', sa.UUID(), nullable=False),
        sa.Column('address', sa.String(), nullable=False),
        sa.Column('unit', sa.String(), nullable=True),
        sa.Column('city', sa.String(), nullable=False),
        sa.Column('province', sa.String(), nullable=False),
        sa.Column('zipcode', sa.String(), nullable=False),
        sa.Column('country', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('order_id')
    )
    op.create_index(op.f('ix_billing_info_id'), 'billing_info', ['id'], unique=False) 