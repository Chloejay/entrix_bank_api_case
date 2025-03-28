from decimal import Decimal

import pytest
from fastapi import status


@pytest.fixture
def mock_request_body(mock_customer, random_iban):  # noqa
    mock_customer_dict = mock_customer.model_dump()
    mock_customer_dict['created_date'] = mock_customer.created_date.isoformat()
    mock_customer_dict['updated_date'] = mock_customer.updated_date.isoformat()
    return {
        'customer': mock_customer_dict,
        'iban': random_iban,
        'default_deposit': str(Decimal('20.01')),
        'currency': 'EUR',
    }


@pytest.fixture
def mock_request_body_fail(mock_customer, existed_iban):  # noqa
    mock_customer_dict = mock_customer.model_dump()
    mock_customer_dict['created_date'] = mock_customer.created_date.isoformat()
    mock_customer_dict['updated_date'] = mock_customer.updated_date.isoformat()
    return {
        'customer': mock_customer_dict,
        'iban': existed_iban,
        'default_deposit': str(Decimal('20.01')),
        'currency': 'EUR',
    }


def test_create_customer_success(client, mock_request_body, mock_header):  # noqa
    response = client.post('/customers/add', json=mock_request_body, headers=mock_header)
    print(response.json())
    print(response.content)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.content is not None


def test_create_existed_customer_fail(client, mock_request_body_fail, mock_header):  # noqa
    response = client.post('/customers/add', json=mock_request_body_fail, headers=mock_header)
    assert response.status_code == status.HTTP_409_CONFLICT
