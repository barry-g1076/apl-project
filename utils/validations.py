import re
from typing import Union, Optional, Pattern

class DataValidator:
    """Comprehensive data validator class."""

    DATE_PATTERN: Pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    BOOKING_PATTERN: Pattern = re.compile(r"^booking_[a-zA-Z0-9_]+$")
    EMAIL_PATTERN: Pattern = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$", re.IGNORECASE
    )
    PAYMENT_PATTERN: Pattern = re.compile(r"^(CreditCard|PayPal|Crypto)$")

    @classmethod
    def is_float(cls, value: Union[float, int, str]) -> bool:
        return isinstance(value, float) and not isinstance(value, bool)

    @classmethod
    def is_int(cls, value: Union[int, float, str]) -> bool:
        return isinstance(value, int) and not isinstance(value, bool)

    @classmethod
    def is_str(cls, value: object) -> bool:
        return isinstance(value, str)

    @classmethod
    def validate_date(cls, date_str: str) -> bool:
        return bool(cls.DATE_PATTERN.match(date_str))

    @classmethod
    def validate_booking_id(cls, booking_id: str) -> bool:
        return bool(cls.BOOKING_PATTERN.match(booking_id))

    @classmethod
    def validate_email(cls, email: str) -> bool:
        return bool(cls.EMAIL_PATTERN.match(email))

    @classmethod
    def validate_view_type(cls, view_type: str) -> bool:
        allowed_view_types = {"tickets", "confirmed", "paid", "canceled", "available"}
        return view_type in allowed_view_types

    @classmethod
    def validate_payment_method(cls, payment_method: str) -> bool:
        return bool(cls.PAYMENT_PATTERN.match(payment_method))
