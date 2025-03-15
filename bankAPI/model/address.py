############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from __future__ import annotations

from typing import Self

from mimesis import Address
from pydantic import BaseModel, Field


class CustomerAddress(BaseModel):
    """Constains the address information for the bank customer."""

    street_name: str = Field(default=Address().street_name(), title='Street Name', examples=['boyenstr'])
    street_number: str = Field(default=Address().street_number(), title='Street Number', examples=['123'])
    houseNumber: str = Field(default="1", title='House Number', examples=['1'])
    postal_code: str = Field(default=Address().postal_code(), title='Postal Code', examples=['10115'])
    country: str = Field(default=Address().country(), title='Country', examples=['Germany'])
    city: str = Field(default=Address().city(), title='City', examples=['Berlin'])

    @classmethod
    def empty(cls) -> Self:
        """Create an empty CustomerAddress model."""
        return CustomerAddress(street_name='', street_number='', houseNumber='', postal_code='', country='', city='')
