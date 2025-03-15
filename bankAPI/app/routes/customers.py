############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from decimal import Decimal
from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import Field
from sqlalchemy.exc import SQLAlchemyError

from bankAPI.alembic.db.db import DBAdapter
from bankAPI.alembic.db.exceptions import DuplicatedEntityException
from bankAPI.model.customers import CustomerIn, CustomerOut
from bankAPI.model.utility import Currency
from bankAPI.utility.logger import logger

router = APIRouter(
    prefix='/customers',
    tags=['bank_customers'],
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {'description': 'data model validation error'},
        status.HTTP_201_CREATED: {'model': CustomerOut, 'description': 'create a new customer'},
    },
)


# logic: checking if to be created customer's phone number of email alreay existed in customer database.then can't created this customer.
async def createAccount(
    *,
    customer: CustomerIn,
    iban: str,
    default_deposit: Decimal,
    currency: Currency,
) -> CustomerOut:
    """Create a new customer and store customer information in customer table in psql db.

    Args:
        customer (CustomerIn): Customer input data contains required peronsal information.
        iban: str: The European bank account that created for this customer once opening a new account.
        default_deposit: Decimal:The default balance in bank account when a new customer opens an account.
        currency: Currency:The currency of amount.

    Returns:
        CustomerOut: Customer personal data, exclused the password to print out for data security.
    """
    if default_deposit <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "default deposit must be positive.")
    customer: CustomerIn = await DBAdapter().create_customer(
        customer=customer, iban=iban, default_deposit=default_deposit, currency=currency
    )
    return customer


@router.post(
    '/add',
    status_code=status.HTTP_201_CREATED,
    summary='Create a new bank customer.',
    response_model_exclude_unset=True,
)
async def create_new_customer(
    *, customer: CustomerIn, iban: str, default_deposit: Decimal, currency: Currency
) -> JSONResponse:
    """Create a new Bank customer"""
    try:
        customer = await createAccount(customer=customer, iban=iban, default_deposit=default_deposit, currency=currency)
        customer = CustomerOut.from_orm(customer)
        logger.info(f'Succeed create a new customer, {customer}')
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(customer))

    except (Exception, SQLAlchemyError) as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except DuplicatedEntityException as e:
        logger.error(e)
        raise HTTPException(status_code=409, detail=str(e))


# @router.get('/all', summary='Get all customers by pagination.')
# async def get_customer():
#     """Retrieve all customers from database."""
#     return JSONResponse('get customer.')


# @router.delete('/{customer_id}', summary='Delete a customer by customer id.')
# async def delete_customer(customer_id: str | UUID):
#     pass


# @router.patch('/{customer_id}', summary='Update a customer personal information by customer id.')
# async def modify_customer(customer_id: str | UUID):
#     pass
