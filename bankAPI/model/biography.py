############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from typing import Self

from mimesis import Address, Person
from pydantic import BaseModel, Field

from bankAPI.model.utility import IdentificationCardNumber


class Biography(BaseModel):
    """A perosn's personal biography data."""

    nationality: str = Field(default=Person().nationality(), title='Nationality', example=['Germany'])
    birth_country: str = Field(default=Address().country_code(), title='Birth Country', example=['DEU'])
    birth_date: str = Field(default=Person().birthdate(), title='Birth Date', example=['1992.10.01'])
    identification_card_number: str = Field(
        default=IdentificationCardNumber.random().identification_number, title='Personal ID'
    )

    @classmethod
    def random(cls) -> Self:
        return Biography(
            nationality=Address().country_code(),
            birth_date=str(Person().birthdate()),
            identification_card_number=str(IdentificationCardNumber.random().identification_number),
        )
