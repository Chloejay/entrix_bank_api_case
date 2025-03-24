############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################


from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError

from bankAPI.alembic.db.db import DBAdapter
from bankAPI.model.customers import CustomerIn, CustomerOut
from bankAPI.model.utility import Currency
from bankAPI.utility.logger import logger

router = APIRouter(
    prefix='/customers',
    tags=['bank_customers'],
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {'description': 'Data model validation error'},
        status.HTTP_201_CREATED: {'model': CustomerOut, 'description': 'Succeed creating a new customer'},
    },
)


# logic: checking if to be created customer's phone number of email alreay existed in customer database, if so then this customer can't be created.
async def createAccount(
    *,
    customer: CustomerIn,
    iban: str,
    default_deposit: str,
    currency: Currency,
) -> CustomerOut:
    """Create a new customer and store customer information in customer table in psql db.

    **Args:**
        customer (CustomerIn): Customer input data contains required peronsal information.
        iban (IBAN): The European bank account that created for this customer once opening a new account.
        default_deposit(Decimal): The default balance in bank account when a new customer opens an account.
        currency(Currency): The currency of amount.

    **Returns:**
        CustomerOut: Customer personal data, exclused the password to print out for data security.

    **Raises:** Exceptions for server errors or duplicated entity errors.
    """
    if float(default_deposit) <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Default deposit must be positive.')
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
    *,
    customer: CustomerIn = Body(...),
    iban: str = Body(...),
    default_deposit: str = Body(...),
    currency: Currency = Body(...),
) -> JSONResponse:
    """Create a new Bank customer.

    **Args:**
    - customer (CustomerIn): Customer input data contains required peronsal information.
    - iban (str): The European bank account that created for this customer once opening a new account.
    - default_deposit(Decimal): The default balance in bank account when a new customer opens an account.
    - currency(Currency): The currency of amount.

    **Returns:** JSONResponse

    **Raises:** Exceptions server error or duplicated error.
    """
    try:
        customer = await createAccount(customer=customer, iban=iban, default_deposit=default_deposit, currency=currency)
        customer = CustomerOut.from_orm(customer)
        logger.info(f'Succeed create a new customer, {customer}')
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(customer))

    except RequestValidationError as e:
        error_details = [{'field': err['loc'], 'message': err['msg'], 'type': err['type']} for err in e.errors()]
        logger.error(f'Validation error: {error_details}')
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=error_details)

    except IntegrityError as e:
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    # except Exception as e:
    #     logger.error(e)
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/{email_id}', summary='Get customer by email id.')
async def get_customer(email: EmailStr):
    """Retrieve customer info by its email from customer table."""
    return JSONResponse('get customer.')


# @router.delete('/{customer_id}', summary='Delete a customer by customer id.')
# async def delete_customer(customer_id: str | UUID):
#     pass


# @router.patch('/{customer_id}', summary='Update a customer personal information by customer id.')
# async def modify_customer(customer_id: str | UUID):
#     pass
