############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

import datetime
import os
from decimal import Decimal

from dotenv import load_dotenv
from fastapi import HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from bankAPI.alembic.db.exceptions import DuplicatedEntityException
from bankAPI.alembic.db.models import BankAccounts as AccountsDB
from bankAPI.alembic.db.models import Customers as CustomersDB
from bankAPI.alembic.db.models import Transactions as TransactionsDB
from bankAPI.alembic.db.utility import toAccountDB, toCustomersDB
from bankAPI.model.accounts import AccountStatus, Currency
from bankAPI.model.customers import CustomerIn
from bankAPI.model.transactions import Transactions, TransactionStatus
from bankAPI.model.utility import ExpirationDate
from bankAPI.utility.logger import logger

load_dotenv()


def check_customer_existed_stmt(CustomersDB, customer):
    """Check if this customer existed by its email or phone number in customer table."""
    try:
        stmt = select(CustomersDB).where(
            (CustomersDB.email == customer.contact.email) | (CustomersDB.phone == customer.contact.phone_number)
        )
        return stmt
    except Exception:
        logger.error('Failed to filter if customer is existed.', exc_info=True)


class DBSingleton(type):
    """Ensures only one instance of DBAdapter exists."""

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class DBAdapter:#noqa
    def __init__(self):
        self._initialize_engine()

    def _initialize_engine(self):
        """Initialize the database engine and session factory."""
        psql_url = os.getenv('sqlalchemy_url')
        if not psql_url:
            logger.error('Database URL is not set in .env file.')
            raise ValueError('Missing postgresql url environment variable.')

        try:
            self.engine = create_async_engine(psql_url, pool_size=50, max_overflow=20, echo=False, future=True)
            self.session_factory = async_sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
            logger.info('Successfully connected to DB.')

        except Exception as e:
            logger.exception(f'Failed to initialize database connection: {e}')
            raise

    async def session(self):
        """Provide an async session as a context manager."""
        async with self.session_factory() as session:
            yield session

    async def create_customer(self, customer: CustomerIn, iban: str, default_deposit: Decimal, currency: Currency):
        """Create a new customer and store in customers table."""
        async for session in self.session():
            try:
                customer_db = toCustomersDB(customer, iban, default_deposit)
                stmt = check_customer_existed_stmt(CustomersDB, customer)
                result = await session.execute(stmt)
                existing_customer = result.scalars().first()

                if existing_customer:
                    logger.error('This customer is already esisted created.')
                    raise DuplicatedEntityException('This customer is created before.')
                else:
                    session.add(customer_db)
                    await session.commit()
                    await session.refresh(customer_db)
                    account_db = AccountsDB(
                        customer_id=customer_db.id,
                        iban=iban,
                        balance=default_deposit,
                        currency=currency,
                        status=AccountStatus.ACTIVE,
                        created_date=datetime.datetime.now(),
                        expiration_date=ExpirationDate.random().expiration_date,
                    )
                    session.add(account_db)
                    await session.commit()
                    session.refresh(account_db)
                    return customer_db
            except IntegrityError:
                await session.rollback()
                raise HTTPException(status_code= status.HTTP_409_CONFLICT, detail= "Duplicated customer.")
            except Exception:
                await session.rollback()
                logger.error('Failed to store a new customer.', exc_info=True)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal server error.')

    async def get_customer_by_email(self, email: str):
        """Retrieve customer by its email."""
        async for session in self.session():
            try:
                result = await session.execute(select(CustomersDB).where(CustomersDB.email == email))
                customer = result.scalars().first()
                logger.info('Succeed retrive customer by account email.')
                return customer
            except Exception as e:
                logger.error(e)

    async def create_account(self, account, account_id):
        """Create a new account under the customer, so first check if customer exists, else create a customer then create an account"""
        # one thought should be account under the customer, or decouple?
        async for session in self.session():
            try:
                account_db = toAccountDB(account, account_id)
                session.add(account_db)
                await session.commit()
                await session.refresh(account_db)

                return account_db
            except IntegrityError as e:
                logger.error('Duplicated value found in column required unique value', exc_info=True)
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Duplicated value error.') from e
            except Exception:
                logger.error('Failed to store new account', exc_info=True)

    async def get_account_by_bank_id(self, account_id: str):
        """Get bank account by the bank id provided for retrieve both sender and receiver bank account."""
        async for session in self.session():
            try:
                account = await session.execute(select(AccountsDB).where(AccountsDB.iban == account_id))
                logger.info(f'Succeed retrieve account, {account}.')
                return account.scalar_one_or_none()
            except Exception:
                logger.error('Failed to retrieve aoount by provided account id.', exc_info=True)

    async def make_transaction(self, from_account_id: str, to_account_id: str, amount: Decimal, currency: Currency):
        """Conduct a transaction, which transfer within two bank accounts."""
        async for session in self.session():
            try:
                sender_account = await self.get_account_by_bank_id(from_account_id)
                receiver_account = await self.get_account_by_bank_id(to_account_id)

                if not sender_account:
                    return None, 'Invalid sender account'

                if not receiver_account:
                    return None, 'Invalid receiver account'

                if sender_account.balance < amount:
                    return None, 'Insufficent funds.'

                sender_account.balance -= int(amount)
                receiver_account.balance += int(amount)

                transaction_db = TransactionsDB(
                    from_account_id=from_account_id,
                    to_account_id=to_account_id,
                    amount=amount,
                    currency=currency,
                    status=TransactionStatus.COMPLETED,
                    created_date=datetime.datetime.now(),
                )

                session.add(transaction_db)
                await session.commit()  # commit() for each changes to avoid InvalidRequestError.
                await session.refresh(transaction_db)
                session.add(sender_account)
                await session.commit()
                session.add(receiver_account)
                await session.commit()

                logger.info(f'Succeed complete a transaction for account: {from_account_id}.')

                return transaction_db, None
            except Exception:
                logger.error('Failed to complete a transaction.', exc_info=True)

    async def get_balance_by_bankID(self, bank_id: str):
        """Retrieve the customer bank account balance default by bank id."""
        async for session in self.session():
            try:
                result = await session.execute(select(AccountsDB).where(AccountsDB.iban == bank_id))
                balance = result.scalar_one_or_none()

                logger.info(f'Succeed retrieve balance from account bank id:{bank_id}.')
                return balance
            except Exception:
                logger.error('Failed to retrieve balance.', exc_info=True)

    async def get_transaction_history_by_bankID(self, bank_id: str) -> list:
        """Retrieve the selected the bank account transaction history, default by bank id."""
        async for session in self.session():
            try:
                result = await session.execute(
                    select(TransactionsDB).where(
                        or_(
                            TransactionsDB.from_account_id == bank_id,
                            TransactionsDB.to_account_id == bank_id,
                        )
                    )
                )
                transactions = result.scalars()
                logger.info(f'Retrieved transactions: {transactions}')

                transaction_list = []
                for transaction in transactions:
                    logger.info(f'Transaction: {transaction}')
                    transaction = Transactions(
                        from_account_id=transaction.from_account_id,
                        to_account_id=transaction.to_account_id,
                        amount=transaction.amount,
                        currency=transaction.currency,
                        status=transaction.status,
                        transaction_date=transaction.created_date,
                    )
                    transaction_list.append(transaction)

                return transaction_list

            except Exception:
                logger.error(f'Failed to retrieve the transaction data for bank id : {bank_id}', exc_info=True)
                return []
