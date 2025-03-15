############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

import random
from datetime import datetime, timedelta
from enum import Enum
from typing import Self

from mimesis import Person
from pydantic import BaseModel, Field


def get_expiration_date() -> datetime:
    """Helper func to get expiration date, the default is six years from the bank card created."""
    expiration_date = datetime.now().replace(microsecond=0) + timedelta(days=6 * 365)
    return expiration_date


def mimic_id_number() -> str:
    """ID card number contains random 9 digits of numeric numbers."""
    return ''.join(str(random.randint(0, 9)) for _ in range(9))


def mimic_iban_number() -> str:
    """Helper func for generating random IBAN Germany number.
    IBAN in Germany consists of 22 characters: DE89370400440532013000.
    """
    random_digits = ''.join(random.choices('0123456789', k=20))
    return f'DE{random_digits}'


class IBAN(BaseModel):
    """Helper func for creating IBAN."""

    iban: str = Field(
        ..., pattern=r'^DE\d{20}$', description="German IBAN pattern: (22 characters, 'DE' followed by 20 digits)"
    )

    @classmethod
    def random(cls) -> Self:
        return IBAN(iban=mimic_iban_number())


class IdentificationCardNumber(BaseModel):
    """Helper func for creating ID card number"""

    identification_number: str = Field(
        ..., pettern=r'^DE\d{20}$', description='Identification ID card contains random 9 digits.'
    )

    @classmethod
    def random(cls) -> Self:
        return IdentificationCardNumber(identification_number=mimic_id_number())


class ExpirationDate(BaseModel):
    """Random generate expiration date as today till six years later."""

    expiration_date: datetime = Field(..., title='Expiration Date', description='Bank card expiration date.')

    @classmethod
    def random(cls) -> Self:
        return ExpirationDate(expiration_date=get_expiration_date())


class SharedAccountBase(BaseModel):
    """Both internal employers and external bank customers shared some similar attributes"""

    first_name: str = Field(default=Person().first_name(), title='First Name')
    middle_name: str | None = Field(default=None, title='Middle Name')
    last_name: str = Field(default=Person().last_name(), title='Last Name')
    # email_address: str


class Currency(str, Enum):
    """List the major currency that assume bank supports. But will use EUR for testing, else need add new feature that
    calculate the amount with interest rates.
    """

    EUR = 'EUR'
    USD = 'USD'
    CNY = 'CNY'
    JPY = 'JPY'
    SGD = 'SGD'

    @classmethod
    def random(cls) -> Self:
        return random.choice(list(cls))
