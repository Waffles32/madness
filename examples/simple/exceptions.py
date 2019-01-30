
from dataclasses import dataclass

@dataclass
class APIException(Exception):
    message: str = ''
    status: int = 500

@dataclass
class PaymentRequired(APIException):
    message: str = 'default message'
    status: int = 402

@dataclass
class Forbidden(APIException):
    message: str = 'you must be logged in'
    status: int = 403
