# validators.py

from custom_exceptions import InvalidAmountError


def validate_amount(amount):

    if amount <= 0:

        raise InvalidAmountError(
            "Amount must be greater than zero"
        )
