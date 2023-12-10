from enum import Enum

from django.core.exceptions import ValidationError
from phonenumber_field.phonenumber import to_python
from phonenumbers.phonenumberutil import is_possible_number

from .error_codes import PaymentErrorCode

def validate_possible_number(phone, country=None):
    """validator for phone numbers usinf ponenumber_field

    Args:
        phone (str): phone number
        country (code, optional): country code. Defaults to None.

    Raises:
        ValidationError: Invalid Phone Number

    Returns:
        str: phone Number
    """
    phone_number = to_python(phone, country)
    if (
        phone_number
        and not is_possible_number(phone_number)
        or not phone_number.is_valid()
    ):
        raise ValidationError(
            "The phone number entered is not valid.", code=PaymentErrorCode.INVALID
        )
    return phone_number
