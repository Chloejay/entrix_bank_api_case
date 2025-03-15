############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################
from mimesis import Person
from pydantic import BaseModel, Field


class Contact(BaseModel):
    """Contact model contains customer phone and email information."""

    email: str = Field(default=Person().email(), title='Email Address', example=['test@gmail.com'])
    phone_number: str = Field(default=Person().phone_number(), title='Phone Number', example=['+49 16262099000'])

    @classmethod
    def random(cls):
        return Contact(
            email= Person().email(),
            phone_number= Person().phone_number()
        )
