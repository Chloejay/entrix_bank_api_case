############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from fastapi import FastAPI
from pydantic_settings import BaseSettings

from bankAPI.app.routes.accounts import router as accountRouter
from bankAPI.app.routes.customers import router as customerRouter
from bankAPI.app.routes.transactions import router as transactionRouter


class Settings(BaseSettings): #noqa
    title: str= "bank api"
    summary: str='Entrix bank API Backend Service.'
    
settings= Settings()

app = FastAPI(summary= settings.summary, title= settings.title)

app.include_router(customerRouter)
app.include_router(accountRouter)
app.include_router(transactionRouter)