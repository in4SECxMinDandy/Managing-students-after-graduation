"""Pagination utilities."""
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


@dataclass
class PaginationParams:
    """Params cho pagination."""

    page: int = Field(default=1, ge=1, description="Trang hiện tại")
    page_size: int = Field(default=20, ge=1, le=100, description="Số items/trang")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response."""

    items: list[T] = Field(default_factory=list)
    total: int = Field(default=0, ge=0)
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1)
    total_pages: int = Field(default=0, ge=0)
    has_next: bool = False
    has_prev: bool = False

    @classmethod
    def create(
        cls,
        items: list[T],
        total: int,
        page: int,
        page_size: int,
    ) -> "PaginatedResponse[T]":
        total_pages = (total + page_size - 1) // page_size if page_size > 0 else 0
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_prev=page > 1,
        )
