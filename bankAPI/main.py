############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from fastapi import FastAPI

from bankAPI.app.routes.accounts import router as accountRouter
from bankAPI.app.routes.customers import router as customerRouter
from bankAPI.app.routes.transactions import router as transactionRouter

app = FastAPI(summary='Entrix bank API Backend Service.')

app.include_router(customerRouter)
app.include_router(accountRouter)
app.include_router(transactionRouter)