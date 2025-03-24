############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from datetime import datetime
from decimal import Decimal

import pytest

from bankAPI.model.address import CustomerAddress
from bankAPI.model.biography import Biography
from bankAPI.model.contact import Contact
from bankAPI.model.customers import CustomerBase
from bankAPI.model.gender import Gender

# how to write the test case that can have meaning and catch edge case? 
def test_CustomerBase():  # noqa D103;
    customer = CustomerBase(
        gender=Gender.random(),
        address=CustomerAddress.empty(),
        contact=Contact.random(),
        biography=Biography.random(),
        created_date=datetime.now(),
        updated_date=datetime.now(),
    )
    assert customer.gender in [Gender.male, Gender.female, Gender.not_given, Gender.other]
    assert isinstance(customer.default_deposit, Decimal)


def test_default_values():
    """Test if default values are correctly assigned."""
    customer = CustomerBase(default_deposit=Decimal('10.00'), created_date=datetime.now(), updated_date=datetime.now())

    assert customer.gender in [Gender.male, Gender.female, Gender.not_given, Gender.other]
    assert isinstance(customer.address, CustomerAddress)
    assert isinstance(customer.contact, Contact)
    assert isinstance(customer.biography, Biography)


def test_missing_fields():
    """Test that missing required fields raise validation errors."""
    with pytest.raises(ValueError):
        CustomerBase()