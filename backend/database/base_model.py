"""Base model with common fields."""
from datetime import datetime
from typing import Any

from sqlalchemy import Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.database.engine import Base


class TimestampMixin:
    """Mixin for created_at/updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )


class SoftDeleteMixin:
    """Mixin for soft delete support."""

    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class TimestampSoftDeleteMixin(Base, TimestampMixin, SoftDeleteMixin):
    """Base model with timestamps and soft delete."""

    __abstract__ = True

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary."""
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }
