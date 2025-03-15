############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from bankAPI.alembic.db.db import DBAdapter
from bankAPI.model.transactions import Transactions

router = APIRouter(
    prefix='/transactions',
    tags=['bank_account_transactions'],
    responses={
        status.HTTP_422_UNPROCESSABLE_ENTITY: {'model': '', 'description': 'data model validation error.'},
        status.HTTP_200_OK: {'model': '', 'description': 'retrieve transaction information.'},
    },
)


# TODO:
# 1. currently check transaction amount and balance, previously didn't consider currency.
# for case study, will limit scope to EUR, in the future need have one standalone table to integrate with external API to fetach dynamic currency rates.
@router.post(
    '/transfer',
    status_code=status.HTTP_200_OK,
    summary='Submit a new transaction.',
    response_model_exclude_unset=True,
)
async def transfer_amount(*, transaction: Transactions):
    """Make a new transaction between two accounts."""
    new_transaction, error = await DBAdapter().make_transaction(
        transaction.from_account_id, transaction.to_account_id, transaction.amount, transaction.currency
    )
    if error:
        raise HTTPException(status_code=400, detail=error)
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(new_transaction))
