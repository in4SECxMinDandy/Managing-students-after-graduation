"""Generic repository for CRUD operations."""
from typing import Any, TypeVar
from uuid import uuid4

from sqlalchemy import Select, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.base_model import TimestampSoftDeleteMixin

ModelT = TypeVar("ModelT", bound=TimestampSoftDeleteMixin)


class BaseRepository:
    """Generic repository for CRUD operations."""

    model: type[ModelT]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, id: int | str) -> ModelT | None:
        """Get entity by primary key."""
        result = await self.session.get(self.model, id)
        return result if result and result.is_active else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelT]:
        """Get all active entities with pagination."""
        stmt = (
            select(self.model)
            .where(self.model.is_active == True)  # noqa: E712
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count(self) -> int:
        """Count active entities."""
        stmt = select(func.count()).select_from(self.model).where(self.model.is_active == True)  # noqa: E712
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def create(self, data: dict[str, Any]) -> ModelT:
        """Create a new entity."""
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(self, id: int | str, data: dict[str, Any]) -> ModelT | None:
        """Update an entity by ID."""
        instance = await self.get_by_id(id)
        if not instance:
            return None
        for key, value in data.items():
            if hasattr(instance, key):
                setattr(instance, key, value)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, id: int | str) -> bool:
        """Soft delete an entity."""
        instance = await self.get_by_id(id)
        if not instance:
            return False
        instance.is_active = False
        await self.session.flush()
        return True

    async def exists(self, id: int | str) -> bool:
        """Check if entity exists."""
        instance = await self.get_by_id(id)
        return instance is not None
