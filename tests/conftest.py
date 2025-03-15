############################################################
#This is for Entrix backend API service: banking-api-obpmev#
############################################################

import pytest
from fastapi.testclient import TestClient

from bankAPI.main import app


@pytest.fixture
def app_client():
    return TestClient(app)

@pytest.fixture
def test_customer():#TODO
    return 