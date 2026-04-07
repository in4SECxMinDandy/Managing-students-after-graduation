"""Pydantic base schemas."""
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class BaseSchema(BaseModel):
    """Base Pydantic schema."""

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
    )


class TimestampSchema(BaseSchema):
    """Schema with timestamp fields."""

    created_at: datetime | None = None
    updated_at: datetime | None = None
    deleted_at: datetime | None = None


class SoftDeleteSchema(BaseSchema):
    """Schema with soft delete fields."""

    is_active: bool = True


class AuditSchema(TimestampSchema, SoftDeleteSchema):
    """Schema with audit fields."""

    pass


class ErrorResponse(BaseSchema):
    """Standard error response."""

    detail: str
    code: str | None = None
