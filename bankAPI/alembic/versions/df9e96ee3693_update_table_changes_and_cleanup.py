"""update table changes and cleanup

Revision ID: df9e96ee3693
Revises: 3a185f0c7909
Create Date: 2025-03-11 20:49:21.651178

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'df9e96ee3693'
down_revision: Union[str, None] = '3a185f0c7909'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('customers',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('nationality', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('birth_country', sa.String(), nullable=False),
    sa.Column('birth_date', sa.String(), nullable=False),
    sa.Column('city', sa.String(), nullable=False),
    sa.Column('full_address', sa.String(), nullable=False),
    sa.Column('postal_code', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('identification_card_number', sa.String(), nullable=False),
    sa.Column('iban', sa.String(), nullable=False),
    sa.Column('default_deposit', sa.DECIMAL(precision=15, scale=2), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('iban'),
    schema='bank_api_orm'
    )
    op.create_table('internal_employees',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('middle_name', sa.String(), nullable=True),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    schema='bank_api_orm'
    )
    op.create_table('bank_accounts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('customer_id', sa.Uuid(), nullable=False),
    sa.Column('iban', sa.String(), nullable=False),
    sa.Column('balance', sa.DECIMAL(precision=15, scale=2), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('status', sa.Enum('ACTIVE', 'CLOSED', 'SUSPEND', name='account_status'), nullable=False),
    sa.Column('expiration_date', sa.DateTime(), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['bank_api_orm.customers.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('iban'),
    schema='bank_api_orm'
    )
    op.create_table('transactions',
    sa.Column('transaction_id', sa.Uuid(), nullable=False),
    sa.Column('from_account_id', sa.String(), nullable=False),
    sa.Column('to_account_id', sa.String(), nullable=False),
    sa.Column('amount', sa.DECIMAL(precision=15, scale=2), nullable=False),
    sa.Column('currency', sa.String(length=3), nullable=False),
    sa.Column('status', sa.Enum('PENDING', 'COMPLETED', 'FAILED', name='transaction_status'), nullable=False),
    sa.Column('created_date', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['from_account_id'], ['bank_api_orm.bank_accounts.iban'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_account_id'], ['bank_api_orm.bank_accounts.iban'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('transaction_id'),
    schema='bank_api_orm'
    )
    op.create_table('transaction_history',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('transaction_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['transaction_id'], ['bank_api_orm.transactions.transaction_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    schema='bank_api_orm'
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction_history', schema='bank_api_orm')
    op.drop_table('transactions', schema='bank_api_orm')
    op.drop_table('bank_accounts', schema='bank_api_orm')
    op.drop_table('internal_employees', schema='bank_api_orm')
    op.drop_table('customers', schema='bank_api_orm')
    # ### end Alembic commands ###
