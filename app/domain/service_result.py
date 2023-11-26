# Standard library imports
from typing import Generic, Optional, TypeVar

# Local application/library specific imports
from app.domain.repository_action_status import RepositoryActionStatus
from app.domain.service_result_status import ServiceResultStatus

T = TypeVar("T")


class ServiceResult(Generic[T]):
    def __init__(
        self,
        data: Optional[T] = None,
        status: ServiceResultStatus = ServiceResultStatus.OK,
        exception: Optional[Exception] = None,
        error_message: Optional[str] = None,
    ):
        self.data = data
        self.status = status
        self.exception = exception
        self.error_message = (
            error_message or (str(exception) if exception else None)
        )

    @property
    def is_ok(self):
        return self.status == ServiceResultStatus.OK

    @property
    def is_not_found(self):
        return self.status == ServiceResultStatus.NOT_FOUND

    @property
    def is_error(self):
        return self.status == ServiceResultStatus.ERROR

    @property
    def is_unprocessable(self):
        return self.status == ServiceResultStatus.UNPROCESSABLE

    @property
    def is_bad_request(self):
        return self.status == ServiceResultStatus.BAD_REQUEST

    @property
    def is_unauthorized(self):
        return self.status == ServiceResultStatus.UNAUTHORIZED

    @property
    def is_conflict(self):
        return self.status == ServiceResultStatus.CONFLICT

    @classmethod
    def ok(cls, data: T):
        return cls(data=data, status=ServiceResultStatus.OK)

    @classmethod
    def not_found(cls, error_message: Optional[str] = None):
        return cls(
            status=ServiceResultStatus.NOT_FOUND,
            error_message=error_message
        )

    @classmethod
    def error(
        cls,
        exception: Optional[Exception] = None,
        error_message: Optional[str] = None
    ):
        return cls(
            status=ServiceResultStatus.ERROR,
            exception=exception,
            error_message=error_message,
        )

    @classmethod
    def unprocessable(cls, error_message: Optional[str] = None):
        return cls(
            status=ServiceResultStatus.UNPROCESSABLE,
            error_message=error_message
        )

    @classmethod
    def bad_request(cls, error_message: Optional[str] = None):
        return cls(
            status=ServiceResultStatus.BAD_REQUEST,
            error_message=error_message
        )

    @classmethod
    def unauthorized(cls, error_message: Optional[str] = None):
        return cls(
            status=ServiceResultStatus.UNAUTHORIZED,
            error_message=error_message
        )

    @classmethod
    def conflict(
        cls,
        data: Optional[T] = None,
        error_message: Optional[str] = None
    ):
        return cls(
            data=data,
            status=ServiceResultStatus.CONFLICT,
            error_message=error_message
        )

    @classmethod
    def from_repository_action_result(
        cls,
        repository_action_result,
        conversion_function,
        message=None
    ):
        if repository_action_result.status == RepositoryActionStatus.OK:
            # Convert the database entity to DTO if necessary
            if repository_action_result.entity is not None:
                if isinstance(repository_action_result.entity, list):
                    data_dto = [
                        conversion_function(e) for e
                        in repository_action_result.entity
                    ]
                else:
                    data_dto = conversion_function(
                        repository_action_result.entity
                    )
                return cls.ok(data=data_dto)
            else:
                return cls.ok(data=None)
        elif (repository_action_result.status
                == RepositoryActionStatus.NOT_FOUND):
            return cls.not_found(
                error_message=message or repository_action_result.error_message
            )
        elif repository_action_result.status == RepositoryActionStatus.ERROR:
            error_message = (
                message
                or str(repository_action_result.exception)
                or repository_action_result.error_message
            )
            return cls.error(error_message=error_message)
        else:
            raise ValueError("Invalid RepositoryActionStatus")
