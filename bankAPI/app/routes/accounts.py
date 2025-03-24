############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from bankAPI.alembic.db.db import DBAdapter
from bankAPI.model.accounts import Account
from bankAPI.utility.logger import logger

router = APIRouter(
    prefix='/accounts',
    tags=['bank_accounts'],
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {'model': '', 'description': 'data model validation error.'},
        status.HTTP_200_OK: {'model': '', 'description': 'retrieve transaction information.'},
    },
)


@router.post('/add', summary='Create a new bank account for existed customer.', status_code=status.HTTP_201_CREATED)
async def create_new_bank_account(*, account: Account, email: str) -> JSONResponse:
    """Once a customer existed, at least one bank accounts will be lives on this customer account.

    **Args:**
    - account(Account): account pydantic model.
    - email(str): customer email account.

    **Returns:**

    **Raises:**
    """
    # current choose to use email (phone number) as the unique identification, because in the backned either email or phone number
    # can trace to customer id

    # check if customer if exists, if true, can create a new account,
    # if false, then return error message and sugegst customer to create account first.
    customer = await DBAdapter().get_customer_by_email(email)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail='Customer not found. Please create an account first.'
        )

    try:
        new_account = await DBAdapter().create_account(account, customer.id)
        if new_account:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED, content=f'Create a new account: {new_account.customer_id}'
            )
    except Exception:
        logger.error('Failed to create a new account.', exc_info=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Internal Server Error')


@router.get('/balance', summary='Retrieve account balance by bank account.')
async def get_account_balance(*, bank_id: str):
    """Reteieve the balance based on bank account provided.

    **Args:**
    - bank_id (str): customer bank IBAN.

    """
    try:
        balance = await DBAdapter().get_balance_by_bankID(bank_id)
        if balance:
            return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(balance))

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get('/transaction_history', summary='Retrieve customer transaction history by bank account.')
async def get_account_transaction_history(*, bank_id: str):
    """Retrieve transactions history based on bank account provided, then retrieve from transactions table.

    **Args:**
    - bank_id: either sender bank IBAN or receiver bank IBAN.

    **Returns:**

    **Raises:**
    """
    try:
        transaction_history = await DBAdapter().get_transaction_history_by_bankID(bank_id)
        return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(transaction_history))
    except Exception as e:
        logger.error(e)
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
