###########################################################
# This is for Entrix backend API service: banking-api-obpmev#
############################################################

from datetime import datetime, timedelta
from decimal import Decimal

from bankAPI.alembic.db.models import BankAccounts as AccountsDB
from bankAPI.alembic.db.models import Customers as CustomersDB
from bankAPI.model.accounts import Account
from bankAPI.model.customers import CustomerIn


def get_expiration_date() -> datetime:
    """Helper func to get expiration date, the default is six years from the bank card created."""
    expiration_date = datetime.now().replace(microsecond=0) + timedelta(days=6 * 365)
    return expiration_date


def toCustomersDB(
    customer: CustomerIn, iban: str, default_deposit: Decimal, _expiration_date: str = get_expiration_date()
) -> CustomersDB:
    """Map fields in CustomerIn pydantic model to ORM model"""
    return CustomersDB(
        first_name=customer.first_name,
        middle_name=customer.middle_name,
        last_name=customer.last_name,
        nationality=customer.biography.nationality,
        gender=customer.gender.value,
        birth_country=customer.biography.birth_country,
        birth_date=str(customer.biography.birth_date),
        city=customer.address.city,
        full_address=customer.address.street_name + customer.address.street_number,
        postal_code=customer.address.postal_code,
        phone=customer.contact.phone_number,
        email=customer.contact.email,
        identification_card_number=customer.biography.identification_card_number,
        iban=iban,
        default_deposit=default_deposit,
        expiration_date=_expiration_date,
        created_date=customer.created_date,
        updated_date=customer.updated_date,
    )


def toAccountDB(account: Account, customer_id):
    """Map openning account pydantic model to ORM model."""
    return AccountsDB(
        customer_id=customer_id,
        iban=str(account.iban),
        balance=account.balance,
        currency=account.currency,
        status=account.status,
        created_date=account.created_date,
        expiration_date=account.expiration_date,
    )
