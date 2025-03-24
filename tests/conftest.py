############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from bankAPI.main import app
from bankAPI.model.address import CustomerAddress
from bankAPI.model.biography import Biography
from bankAPI.model.contact import Contact
from bankAPI.model.customers import CustomerIn
from bankAPI.model.gender import Gender
from bankAPI.model.utility import IBAN


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def mock_header():  # noqa
    headers = {'Content-Type': 'application/json'}
    return headers


@pytest.fixture
def mock_customer():  # noqa
    return CustomerIn(
        first_name='emma',
        middle_name='',
        last_name='oliver',
        gender=Gender.female,
        address=CustomerAddress.empty(),
        contact=Contact.random(),
        biography=Biography.random(),
        created_date=datetime.now(),
        updated_date=datetime.now(),
        password='abcdefgh',
    )


@pytest.fixture
def existed_iban():  # noqa
    return 'DE86997513256182021252'

@pytest.fixture 
def random_iban(): #noqa
    return IBAN.random().iban