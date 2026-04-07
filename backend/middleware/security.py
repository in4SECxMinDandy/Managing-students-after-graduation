"""Security dependencies and JWT handling."""
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database.engine import get_db
from backend.utils.hash import decode_token

security = HTTPBearer()


class TokenPayload(BaseModel):
    """JWT token payload."""

    sub: str | None = None
    user_id: str | None = None
    role: str | None = None
    type: str | None = None
    exp: int | None = None


class CurrentUser(BaseModel):
    """Current authenticated user."""

    user_id: str
    role: str
    user_type: str  # admin | giangvien | sinhvien


def get_token_payload(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> TokenPayload:
    """Extract and validate JWT token payload."""
    token = credentials.credentials
    payload = decode_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return TokenPayload(**payload)


async def get_current_user(
    payload: Annotated[TokenPayload, Depends(get_token_payload)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> CurrentUser:
    """Get current authenticated user from token."""
    if payload.type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )
    if not payload.user_id or not payload.role:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    return CurrentUser(
        user_id=payload.user_id,
        role=payload.role,
        user_type=payload.get("user_type", "admin"),
    )


def require_roles(*allowed_roles: str):
    """Dependency factory for role-based access control."""
    async def role_checker(
        current_user: Annotated[CurrentUser, Depends(get_current_user)],
    ) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You don't have permission to perform this action",
            )
        return current_user
    return role_checker


# Pre-defined role dependencies
require_admin = require_roles("admin", "super_admin")
require_khoa = require_roles("admin", "super_admin", "khoa")
require_gv = require_roles("admin", "super_admin", "khoa", "giangvien")
require_all = require_roles("admin", "super_admin", "khoa", "giangvien", "sinhvien")
