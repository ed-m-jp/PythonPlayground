# Standard library imports
from typing import Generic, Type, TypeVar

# Related third-party imports
from sqlalchemy.orm import Session

# Local application/library specific imports
from app.domain.repository_action_result import RepositoryActionResult

T = TypeVar('T')


class RepositoryBase(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def create(self, entity: T) -> RepositoryActionResult[T]:
        try:
            self.db.add(entity)
            self.db.commit()
            self.db.refresh(entity)
            return RepositoryActionResult.ok(entity)
        except Exception as e:
            self.db.rollback()
            # TODO - Log exception
            return (
                RepositoryActionResult
                .error(exception=e, error_message=str(e))
            )

    def get_by_id(self, id: int) -> RepositoryActionResult[T]:
        try:
            entity = (
                self.db.query(self.model)
                .filter(self.model.id == id)
                .first()
            )
            if entity:
                return RepositoryActionResult.ok(entity)
            else:
                return (
                    RepositoryActionResult
                    .not_found(f"Entity with id {id} not found")
                )
        except Exception as e:
            # TODO - Log exception
            return (
                RepositoryActionResult
                .error(exception=e, error_message=str(e))
            )

    def delete(self, id: int) -> RepositoryActionResult[None]:
        try:
            entity = (
                self.db.query(self.model)
                .filter(self.model.id == id)
                .first()
            )
            if entity:
                self.db.delete(entity)
                self.db.commit()
                return RepositoryActionResult.ok(None)
            else:
                return (
                    RepositoryActionResult
                    .not_found(f"Entity with id {id} not found")
                )
        except Exception as e:
            self.db.rollback()
            # TODO - Log exception
            return (
                RepositoryActionResult
                .error(exception=e, error_message=str(e))
            )

    def update(self, id: int, updated_data: dict) -> RepositoryActionResult[T]:
        try:
            entity = (
                self.db.query(self.model)
                .filter(self.model.id == id)
                .first()
            )
            if entity:
                for key, value in updated_data.items():
                    setattr(entity, key, value)
                self.db.commit()
                self.db.refresh(entity)
                return RepositoryActionResult.ok(entity)
            else:
                return (
                    RepositoryActionResult
                    .not_found(f"Entity with id {id} not found")
                )
        except Exception as e:
            self.db.rollback()
            # TODO - Log exception
            return (
                RepositoryActionResult
                .error(exception=e, error_message=str(e))
            )
