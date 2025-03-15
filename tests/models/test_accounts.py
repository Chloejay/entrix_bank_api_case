############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from datetime import datetime
from decimal import Decimal
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from bankAPI.model.accounts import Account, AccountStatus
from bankAPI.model.utility import Currency


def test_random_valid_status():
    """Ensure in allowed AccountStatus enum values."""
    status = AccountStatus.random()
    assert status in AccountStatus

def test_random_valid_currency():
    """Ensure in allowed Currency enum values."""
    currency= Currency.random()
    assert currency in Currency


def test_account_creation_defaults():
    """Test creating an Account instance with default values."""
    account = Account(id=uuid4(), expiration_date=datetime(2030, 3, 10, 18, 25, 37))

    assert isinstance(account.id, UUID)
    assert isinstance(account.iban, str)
    assert isinstance(Decimal(account.balance), Decimal)
    assert isinstance(account.currency, Currency)
    assert account.status == AccountStatus.ACTIVE
    assert isinstance(account.expiration_date, datetime)
    assert isinstance(account.created_date, datetime)


def test_account_creation_custom_values():
    """Test creating an Account with specific values."""
    custom_id = uuid4()
    custom_iban = 'DE44500105175407324931'
    custom_balance = Decimal('1000.50')
    custom_currency = Currency.EUR
    custom_status = AccountStatus.SUSPEND
    custom_expiration_date = datetime(2030, 5, 20, 12, 0, 0)
    custom_created_date = datetime(2024, 3, 10, 10, 0, 0)

    account = Account(
        id=custom_id,
        iban=custom_iban,
        balance=custom_balance,
        currency=custom_currency,
        status=custom_status,
        expiration_date=custom_expiration_date,
        created_date=custom_created_date,
    )

    assert account.id == custom_id
    assert account.iban == custom_iban
    assert account.balance == custom_balance
    assert account.currency == custom_currency
    assert account.status == custom_status
    assert account.expiration_date == custom_expiration_date
    assert account.created_date == custom_created_date


def test_invalid_account_creation():
    """Ensure an error is raised when invalid data is provided."""
    with pytest.raises(ValidationError):
        Account(
            id='invalid-uuid',
            expiration_date='not-a-datetime',
        )


def test_json_encoding():
    """Ensure datetime fields are correctly serialized in JSON."""
    account = Account(id=uuid4(), expiration_date=datetime(2030, 3, 10, 18, 25, 37))
    json_data = account.model_dump_json()

    assert 'expiration_date' in json_data
    assert 'created_date' in json_data
    assert account.expiration_date.isoformat() in json_data
    assert account.created_date.isoformat() in json_data
