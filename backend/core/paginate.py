"""Pagination utilities."""
from typing import Generic, TypeVar
from pydantic import BaseModel, Field


T = TypeVar("T")


class PaginationParams(BaseModel):
    """Standard pagination parameters."""

    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard paginated response."""

    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


def paginate(items: list[T], total: int, page: int, page_size: int) -> PaginatedResponse[T]:
    """Create paginated response."""
    total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
    return PaginatedResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages,
    )
