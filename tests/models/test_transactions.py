############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from datetime import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from bankAPI.model.transactions import Transactions, TransactionStatus
from bankAPI.model.utility import Currency


def test_random_valid_transaction_status():
    """Ensure in allowed TransactionStatus enum values."""
    status = TransactionStatus.random()
    assert status in TransactionStatus


def test_transaction_creation_defaults():
    """Test creating a Transactions instance with default values."""
    transaction = Transactions()

    assert isinstance(transaction.from_account_id, str)
    assert isinstance(transaction.to_account_id, str)
    assert isinstance(Decimal(transaction.amount), Decimal)
    assert isinstance(transaction.currency, Currency)
    assert isinstance(transaction.status, TransactionStatus)
    assert isinstance(transaction.transaction_date, datetime)


def test_transaction_creation_custom_values():
    """Test creating a Transactions instance with specific values."""
    custom_from_id = 'DE44500105175407324931'
    custom_to_id = 'FR1420041010050500013M02606'
    custom_amount = Decimal('500.75')
    custom_currency = Currency.USD
    custom_status = TransactionStatus.COMPLETED
    custom_date = datetime(2024, 3, 10, 14, 30, 0)

    transaction = Transactions(
        from_account_id=custom_from_id,
        to_account_id=custom_to_id,
        amount=custom_amount,
        currency=custom_currency,
        status=custom_status,
        transaction_date=custom_date,
    )

    assert transaction.from_account_id == custom_from_id
    assert transaction.to_account_id == custom_to_id
    assert transaction.amount == custom_amount
    assert transaction.currency == custom_currency
    assert transaction.status == custom_status
    assert transaction.transaction_date == custom_date


def test_invalid_transaction_creation():
    """Ensure an error is raised for invalid data."""
    with pytest.raises(ValidationError):
        Transactions(
            from_account_id=12345,  
            amount='invalid-amount',
        )


def test_json_encoding():
    """Ensure datetime fields are correctly serialized in JSON."""
    transaction = Transactions()
    json_data = transaction.model_dump_json()

    assert 'transaction_date' in json_data
    assert transaction.transaction_date.isoformat() in json_data
