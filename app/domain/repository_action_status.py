# Standard library imports
from enum import Enum


class RepositoryActionStatus(Enum):
    OK = 'Ok'
    NOT_FOUND = 'NotFound'
    ERROR = 'Error'
