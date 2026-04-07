"""Decorators cho toàn bộ ứng dụng."""
from functools import wraps
from typing import Any, Callable, TypeVar

from fastapi import HTTPException, status

F = TypeVar("F", bound=Callable[..., Any])


def handle_db_errors(func: F) -> F:
    """Decorator xử lý lỗi database chung."""

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            if isinstance(e, HTTPException):
                raise
            raise
    return wrapper  # type: ignore[return-value]


def require_role(*roles: str) -> Callable[[F], F]:
    """Decorator kiểm tra role (sử dụng với Depends)."""

    def decorator(func: F) -> F:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            return await func(*args, **kwargs)
        return wrapper  # type: ignore[return-value]
    return decorator
