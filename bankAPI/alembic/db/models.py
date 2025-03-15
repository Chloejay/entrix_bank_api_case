############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from __future__ import annotations

import uuid
from datetime import datetime
from uuid import UUID

from sqlalchemy import DECIMAL, DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, registry, relationship

from bankAPI.model.accounts import AccountStatus
from bankAPI.model.transactions import TransactionStatus

SCHEMA = 'bank_api_orm'
mapper_registry = registry()


class Base(DeclarativeBase):
    __table_args__ = {'schema': SCHEMA}


class InternalEmployees(Base):
    """Bank internal employers table to store employer basic infos and login credentials."""

    __tablename__: str = 'internal_employees'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    first_name: Mapped[str] = mapped_column(String())
    middle_name: Mapped[str | None] = mapped_column(String())
    last_name: Mapped[str] = mapped_column(String())
    email: Mapped[str | None] = mapped_column(String())

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Customers(Base):
    """Customer sqlalchemy model."""

    __tablename__: str = 'customers'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    first_name: Mapped[str] = mapped_column(String(), nullable=False)
    middle_name: Mapped[str | None] = mapped_column(String())
    last_name: Mapped[str] = mapped_column(String(), nullable=False)
    nationality: Mapped[str] = mapped_column(String())
    gender: Mapped[str] = mapped_column(String())
    birth_country: Mapped[str] = mapped_column(String())
    birth_date: Mapped[str] = mapped_column(String())
    city: Mapped[str] = mapped_column(String())
    full_address: Mapped[str] = mapped_column(String())
    postal_code: Mapped[str | None] = mapped_column(String())
    phone: Mapped[str] = mapped_column(String(), nullable=False)
    email: Mapped[str] = mapped_column(String(), nullable=False)
    identification_card_number: Mapped[str] = mapped_column(String(), nullable=False)

    # opening account bank id, the default and unique one, also is the FK between customers and accounts table.
    iban: Mapped[str] = mapped_column(String(), unique=True, nullable=False)
    default_deposit: Mapped[DECIMAL] = mapped_column(DECIMAL(15, 2))
    expiration_date: Mapped[datetime]

    # one to many relationship to accounts(A customer has one primary bank account)
    bank_accounts = relationship('BankAccounts', back_populates='customers', cascade='all, delete')

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class BankAccounts(Base):
    """Customer bank account model."""

    __tablename__: str = 'bank_accounts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey(f'{SCHEMA}.customers.id', ondelete='CASCADE'), nullable=False)

    iban: Mapped[str] = mapped_column(unique=True, nullable=False)
    balance: Mapped[DECIMAL] = mapped_column(DECIMAL(15, 2))  # store default deposit
    currency: Mapped[str] = mapped_column(String(3), default='EUR')
    status: Mapped[AccountStatus] = mapped_column(Enum(AccountStatus, name='account_status'))
    expiration_date: Mapped[datetime]

    # many to one
    customers = relationship('Customers', back_populates='bank_accounts')
    # one to many
    outgoing_transactions = relationship(
        'Transactions', foreign_keys='[Transactions.from_account_id]', back_populates='from_account'
    )
    incoming_transactions = relationship(
        'Transactions', foreign_keys='[Transactions.to_account_id]', back_populates='to_account'
    )

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Transactions(Base):
    """Transaction table for each transaction unit."""

    __tablename__: str = 'transactions'

    transaction_id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    from_account_id: Mapped[str] = mapped_column(
        String(), ForeignKey(f'{SCHEMA}.bank_accounts.iban', ondelete='CASCADE'), nullable=False
    )
    to_account_id: Mapped[str] = mapped_column(
        String(), ForeignKey(f'{SCHEMA}.bank_accounts.iban', ondelete='CASCADE'), nullable=False
    )

    amount: Mapped[DECIMAL] = mapped_column(DECIMAL(15, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default='EUR')

    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus, name='transaction_status'))

    # relationships
    from_account = relationship('BankAccounts', foreign_keys=[from_account_id], back_populates='outgoing_transactions')
    to_account = relationship('BankAccounts', foreign_keys=[to_account_id], back_populates='incoming_transactions')

    created_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class TransactionHistory(Base):
    """Customer transaction model."""

    __tablename__: str = 'transaction_history'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    transaction_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey(f'{SCHEMA}.transactions.transaction_id', ondelete='CASCADE'), nullable=False
    )
