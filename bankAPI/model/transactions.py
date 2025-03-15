############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

import random
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Self

from mimesis import Finance
from pydantic import BaseModel, Field

from bankAPI.model.utility import IBAN, Currency


class TransactionStatus(str, Enum):
    """Status of transaction."""

    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

    @classmethod
    def random(cls) -> Self:
        return random.choice(list(cls))


class Transactions(BaseModel):
    """The bank accountn transactions"""

    from_account_id: str = Field(default=IBAN.random().iban, title='Transaction sender account')
    to_account_id: str = Field(default=IBAN.random().iban, title='Transaction receiver account')
    amount: Decimal = Field(default=Finance().price(), description='Transaction amount')
    currency: Currency = Field(default=Currency.random(), title='Currency', description='transaction currency')
    status: TransactionStatus = Field(default=TransactionStatus.random(), title='Transaction status')

    transaction_date: datetime = Field(
        default_factory=datetime.now
    )  # impl: should have sent&receive timestamp, or need have a callback or webhook to notify once send.


class TransactionHistory(BaseModel):
    """Transaction history"""

    transaction_id: str
    transactionHistory: list[Transactions] = Field(...)
