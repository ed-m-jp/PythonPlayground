# Standard library imports
from typing import Generic, List, TypeVar

T = TypeVar("T")


class PaginationResult(Generic[T]):
    def __init__(
        self,
        items: List[T],
        total_items: int
    ):
        self.items = items
        self.total_items = total_items
