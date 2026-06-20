# banking logic

from validators import validate_amount
from custom_exceptions import (

    InsufficientFundsError
)


# deposit


def deposit(balance, amount):

    validate_amount(amount)

    return balance + amount


# withdraw

def withdraw(balance, amount):
    validate_amount(amount)

    if amount > balance:

        raise InsufficientFundsError(
            " Not enough money "
        )

    return balance - amount
