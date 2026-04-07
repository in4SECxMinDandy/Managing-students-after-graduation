"""Base model với common columns."""
from datetime import datetime, timezone
from typing import Any

from sqlalchemy import Boolean, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class TimestampMixin:
    """Mixin thêm created_at, updated_at, deleted_at."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=lambda: datetime.now(timezone.utc),
    )
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), default=None
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )


class BaseTable(Base, TimestampMixin):
    """Base table với tất cả common columns."""

    __abstract__ = True

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)


class StringTypeMixin:
    """Mixin cho kiểu dữ liệu string."""

    Ma: Mapped[str] = mapped_column(String, primary_key=True)
