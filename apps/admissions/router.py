"""Admissions API router."""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database.engine import get_db
from backend.middleware.security import require_admin, require_all
from backend.models.all_models import HSO_XetTuyen, PT_XetTuyen, TK_XetTuyen
from apps.admissions.schemas import (
    HSO_XetTuyenCreate,
    HSO_XetTuyenResponse,
    HSO_XetTuyenUpdate,
    PT_XetTuyenCreate,
    PT_XetTuyenResponse,
    PT_XetTuyenUpdate,
    TK_XetTuyenCreate,
    TK_XetTuyenResponse,
)
from backend.utils.hash import hash_password

router = APIRouter(prefix="/admissions", tags=["Admissions"])


# ---- TK_XetTuyen ----
@router.post("/accounts", response_model=TK_XetTuyenResponse, dependencies=[Depends(require_admin)])
async def create_account(
    data: TK_XetTuyenCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TK_XetTuyenResponse:
    """Create a new admission account."""
    tk = TK_XetTuyen(Email=data.Email, MatKhau=hash_password(data.MatKhau))
    db.add(tk)
    await db.flush()
    await db.refresh(tk)
    return TK_XetTuyenResponse.model_validate(tk)


# ---- HSO_XetTuyen ----
@router.post("/profiles", response_model=HSO_XetTuyenResponse, dependencies=[Depends(require_admin)])
async def create_profile(
    data: HSO_XetTuyenCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HSO_XetTuyenResponse:
    """Create a new admission profile."""
    hso = HSO_XetTuyen(**data.model_dump())
    db.add(hso)
    await db.flush()
    await db.refresh(hso)
    return HSO_XetTuyenResponse.model_validate(hso)


@router.get("/profiles", response_model=list[HSO_XetTuyenResponse], dependencies=[Depends(require_admin)])
async def list_profiles(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[HSO_XetTuyenResponse]:
    """List all admission profiles."""
    result = await db.execute(
        select(HSO_XetTuyen)
        .where(HSO_XetTuyen.is_active == True)  # noqa: E712
        .offset(skip).limit(limit)
    )
    profiles = result.scalars().all()
    return [HSO_XetTuyenResponse.model_validate(p) for p in profiles]


@router.get("/profiles/{ma_hso}", response_model=HSO_XetTuyenResponse, dependencies=[Depends(require_admin)])
async def get_profile(
    ma_hso: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HSO_XetTuyenResponse:
    """Get admission profile by MaHSO."""
    result = await db.execute(
        select(HSO_XetTuyen).where(HSO_XetTuyen.MaHSO == ma_hso)
    )
    hso = result.scalar_one_or_none()
    if not hso:
        raise HTTPException(status_code=404, detail="Profile not found")
    return HSO_XetTuyenResponse.model_validate(hso)


@router.put("/profiles/{ma_hso}", response_model=HSO_XetTuyenResponse, dependencies=[Depends(require_admin)])
async def update_profile(
    ma_hso: str,
    data: HSO_XetTuyenUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HSO_XetTuyenResponse:
    """Update admission profile."""
    result = await db.execute(
        select(HSO_XetTuyen).where(HSO_XetTuyen.MaHSO == ma_hso)
    )
    hso = result.scalar_one_or_none()
    if not hso:
        raise HTTPException(status_code=404, detail="Profile not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(hso, key):
            setattr(hso, key, value)
    await db.flush()
    await db.refresh(hso)
    return HSO_XetTuyenResponse.model_validate(hso)


# ---- PT_XetTuyen ----
@router.post("/applications", response_model=PT_XetTuyenResponse, dependencies=[Depends(require_admin)])
async def create_application(
    data: PT_XetTuyenCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PT_XetTuyenResponse:
    """Create a new admission application."""
    pt = PT_XetTuyen(**data.model_dump())
    db.add(pt)
    await db.flush()
    await db.refresh(pt)
    return PT_XetTuyenResponse.model_validate(pt)


@router.get("/applications", response_model=list[PT_XetTuyenResponse], dependencies=[Depends(require_admin)])
async def list_applications(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[PT_XetTuyenResponse]:
    """List all admission applications."""
    result = await db.execute(
        select(PT_XetTuyen)
        .where(PT_XetTuyen.is_active == True)  # noqa: E712
        .offset(skip).limit(limit)
    )
    apps = result.scalars().all()
    return [PT_XetTuyenResponse.model_validate(a) for a in apps]


@router.put("/applications/{ma_ptxt}", response_model=PT_XetTuyenResponse, dependencies=[Depends(require_admin)])
async def update_application(
    ma_ptxt: int,
    data: PT_XetTuyenUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PT_XetTuyenResponse:
    """Update admission application (approve/reject)."""
    result = await db.execute(
        select(PT_XetTuyen).where(PT_XetTuyen.MaPTXT == ma_ptxt)
    )
    pt = result.scalar_one_or_none()
    if not pt:
        raise HTTPException(status_code=404, detail="Application not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(pt, key):
            setattr(pt, key, value)
    await db.flush()
    await db.refresh(pt)
    return PT_XetTuyenResponse.model_validate(pt)
