############################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

import random
from enum import Enum
from typing import Self


class Gender(str, Enum):
    """Gender of customer, apply ISO5218 code for representing human sexes in an international standard."""

    male = 1
    female = 2
    other = 0
    not_given = 9

    @classmethod
    def random(cls) -> Self:
        return random.choice(list(cls))
