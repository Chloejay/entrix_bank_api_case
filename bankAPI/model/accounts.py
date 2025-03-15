############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

import random
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Self
from uuid import UUID

from mimesis import Finance
from pydantic import BaseModel, Field

from bankAPI.model.utility import IBAN, Currency


class AccountStatus(str, Enum):
    """Basic lifecycle of the bank account creation to closure, and middle stage of suspense."""

    ACTIVE = 'active'
    CLOSED = 'closed'
    SUSPEND = 'suspend'

    @classmethod
    def random(cls) -> Self:
        return random.choice(list(cls))


class Account(BaseModel):
    """Contains basic information for the bank account.
    Default properites of a bank account: iban, deposit/balnce, currency, expiration date.
    """

    id: UUID = Field(title='Bank ID', description='Account unique id')
    iban: str = Field(default=IBAN.random().iban, title='Europe Bank ID', description='Bank card number.')
    balance: Decimal = Field(default=Decimal(Finance().price()), title='Account Balance')
    currency: Currency = Field(default=Currency.random(), title='Currency', description='transaction currency')
    status: AccountStatus = Field(default=AccountStatus.ACTIVE, title='Account Status')
    expiration_date: datetime = Field(
        ..., example='2025-03-10T18:25:37.227'
    )  # assume the bank account will expire in 6 years.
    created_date: datetime = Field(default=datetime.now())

    class Config:
        """Pydantic config to ensure datetime is parsed correctly."""

        json_encoders = {datetime: lambda v: v.isoformat()}


class AccountHistory(BaseModel):
    """The bank account transaction history."""

    pass


class AccountBalance(BaseModel):
    """The bank account balance."""

    pass
