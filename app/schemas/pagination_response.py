# Standard library imports
from typing import Generic, List, TypeVar

# Related third-party imports
from pydantic import BaseModel

T = TypeVar("T")


class Pagination(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    page_size: int


class PaginationResponse(Generic[T], BaseModel):
    items: List[T]
    pagination: Pagination
