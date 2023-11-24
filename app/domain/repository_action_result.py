from typing import Generic, TypeVar, Optional
from app.domain.repository_action_status import RepositoryActionStatus

T = TypeVar("T")


class RepositoryActionResult(Generic[T]):
    def __init__(
        self,
        entity: Optional[T] = None,
        exception: Optional[Exception] = None,
        error_message: Optional[str] = None,
        status: RepositoryActionStatus = RepositoryActionStatus.OK,
    ):
        self.entity = entity
        self.exception = exception
        self.error_message = error_message
        self.status = status

    @property
    def is_ok(self):
        return self.status == RepositoryActionStatus.OK

    @property
    def is_not_found(self):
        return self.status == RepositoryActionStatus.NOT_FOUND

    @property
    def is_error(self):
        return self.status == RepositoryActionStatus.ERROR

    @classmethod
    def not_found(cls, message: str):
        return cls(
            error_message=message,
            status=RepositoryActionStatus.NOT_FOUND
        )

    @classmethod
    def ok(cls, entity: T):
        return cls(entity=entity, status=RepositoryActionStatus.OK)

    @classmethod
    def error(
        cls,
        exception: Optional[Exception] = None,
        error_message: Optional[str] = None
    ):
        return cls(
            exception=exception,
            error_message=error_message,
            status=RepositoryActionStatus.ERROR,
        )
