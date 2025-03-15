############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from datetime import datetime
from decimal import Decimal
from typing import Annotated

from mimesis import Person
from pydantic import Field

from bankAPI.model.address import CustomerAddress
from bankAPI.model.biography import Biography
from bankAPI.model.contact import Contact
from bankAPI.model.gender import Gender
from bankAPI.model.utility import SharedAccountBase


class CustomerBase(SharedAccountBase):
    """Customer base model that both in & out of customer contains

    Args:
        SharedAccountBase: the basic information that required for both internal employer and external bank customer.
    """

    gender: Gender = Field(default=Gender.random(), title='Gender', example=[Gender.female.value])
    address: CustomerAddress = Field(default=CustomerAddress.empty(), title='address information')
    contact: Contact = Field(default=Contact.random(), title='Contact', description='Phone number and email contact')
    biography: Biography = Field(default=Biography.random(), title='Biography', description='customer biography data')

    created_date: datetime
    updated_date: datetime

    class Config:
        from_attributes = True


class CustomerIn(CustomerBase):
    """Customer input model, will add password."""

    password: str = Field(
        default=Person().password(), title='Password', min_length=8, max_length=20
    )  # user also created password when a new bank account created. (will hash the password for security purpose.)


# TODO: create a new table for customer bank password, this one should encrpted and better NOT store any where unsafe.
class CustomerOut(CustomerBase):
    """The customer output model, will exclude password but will add iiban and its expiration date."""

    iban: str = Field(title='IBAN', example='DE44500105175407324931')
    default_deposit: Decimal = Annotated[Decimal, Field(gt=0, title='Default Deposit')]
    expiration_date: datetime = Field(title='Expiration Date')

    class Config:
        orm_mode = True
