# Standard library imports
from enum import Enum


class ServiceResultStatus(Enum):
    OK = 'Ok'
    NOT_FOUND = 'NotFound'
    ERROR = 'Error'
    UNPROCESSABLE = 'Unprocessable'
    BAD_REQUEST = 'BadRequest'
    UNAUTHORIZED = 'Unauthorized'
    CONFLICT = 'Conflict'
