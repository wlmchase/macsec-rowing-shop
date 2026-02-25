"""orders_payment_information

Revision ID: 159c8a58a353
Revises: e2a5a6a54791
Create Date: 2025-03-22 09:03:22.869530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '159c8a58a353'
down_revision: Union[str, None] = 'e2a5a6a54791'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Drop existing columns in payment_info
    op.drop_column('payment_info', 'payment_method')
    op.drop_column('payment_info', 'transaction_id')
    op.drop_column('payment_info', 'amount')
    op.drop_column('payment_info', 'status')
    
    # Add new columns to payment_info
    op.add_column('payment_info', sa.Column('card_number', sa.String(), nullable=False))
    op.add_column('payment_info', sa.Column('card_holder', sa.String(), nullable=False))
    op.add_column('payment_info', sa.Column('expiration_date', sa.String(), nullable=False))
    op.add_column('payment_info', sa.Column('cvv', sa.String(), nullable=False))


def downgrade() -> None:
    """Downgrade schema."""
    # Drop new columns from payment_info
    op.drop_column('payment_info', 'card_number')
    op.drop_column('payment_info', 'card_holder')
    op.drop_column('payment_info', 'expiration_date')
    op.drop_column('payment_info', 'cvv')
    
    # Add back original columns to payment_info
    op.add_column('payment_info', sa.Column('payment_method', sa.String(), nullable=False))
    op.add_column('payment_info', sa.Column('transaction_id', sa.String(), nullable=True))
    op.add_column('payment_info', sa.Column('amount', sa.Float(), nullable=False))
    op.add_column('payment_info', sa.Column('status', sa.String(), nullable=True))
