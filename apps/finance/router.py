"""Finance API router."""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database.engine import get_db
from backend.middleware.security import require_admin, require_all
from backend.models.all_models import DonGiaTinChi, HocPhi
from apps.finance.schemas import (
    DonGiaTinChiCreate,
    DonGiaTinChiResponse,
    DonGiaTinChiUpdate,
    HocPhiCreate,
    HocPhiResponse,
    HocPhiUpdate,
)

router = APIRouter(prefix="/finance", tags=["Finance"])


# ---- DonGiaTinChi ----
@router.post("/tuition-rates", response_model=DonGiaTinChiResponse, dependencies=[Depends(require_admin)])
async def create_tuition_rate(
    data: DonGiaTinChiCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DonGiaTinChiResponse:
    """Create tuition rate per credit."""
    dg = DonGiaTinChi(**data.model_dump())
    db.add(dg)
    await db.flush()
    await db.refresh(dg)
    return DonGiaTinChiResponse.model_validate(dg)


@router.get("/tuition-rates", response_model=list[DonGiaTinChiResponse], dependencies=[Depends(require_all)])
async def list_tuition_rates(
    db: Annotated[AsyncSession, Depends(get_db)],
    nam_hoc: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[DonGiaTinChiResponse]:
    """List tuition rates."""
    stmt = select(DonGiaTinChi).where(DonGiaTinChi.is_active == True)  # noqa: E712
    if nam_hoc:
        stmt = stmt.where(DonGiaTinChi.NamHoc == nam_hoc)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [DonGiaTinChiResponse.model_validate(r) for r in result.scalars().all()]


@router.put("/tuition-rates/{ma_dg}", response_model=DonGiaTinChiResponse, dependencies=[Depends(require_admin)])
async def update_tuition_rate(
    ma_dg: int,
    data: DonGiaTinChiUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DonGiaTinChiResponse:
    """Update tuition rate."""
    result = await db.execute(select(DonGiaTinChi).where(DonGiaTinChi.MaDonGia == ma_dg))
    dg = result.scalar_one_or_none()
    if not dg:
        raise HTTPException(status_code=404, detail="Tuition rate not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(dg, key):
            setattr(dg, key, value)
    await db.flush()
    await db.refresh(dg)
    return DonGiaTinChiResponse.model_validate(dg)


# ---- HocPhi ----
@router.post("/tuitions", response_model=HocPhiResponse, dependencies=[Depends(require_admin)])
async def create_tuition(
    data: HocPhiCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HocPhiResponse:
    """Create tuition record. BR-05 (tính tự động theo số tín chỉ)."""
    hp = HocPhi(**data.model_dump())
    db.add(hp)
    await db.flush()
    await db.refresh(hp)
    return HocPhiResponse.model_validate(hp)


@router.get("/tuitions", response_model=list[HocPhiResponse], dependencies=[Depends(require_all)])
async def list_tuitions(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_sv: str | None = None,
    ma_hk: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[HocPhiResponse]:
    """List tuition records."""
    stmt = select(HocPhi).where(HocPhi.is_active == True)  # noqa: E712
    if ma_sv:
        stmt = stmt.where(HocPhi.MaSV == ma_sv)
    if ma_hk:
        stmt = stmt.where(HocPhi.MaHK == ma_hk)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [HocPhiResponse.model_validate(t) for t in result.scalars().all()]


@router.put("/tuitions/{ma_hp}", response_model=HocPhiResponse, dependencies=[Depends(require_admin)])
async def update_tuition(
    ma_hp: int,
    data: HocPhiUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HocPhiResponse:
    """Update tuition (mark as paid, etc.)."""
    result = await db.execute(select(HocPhi).where(HocPhi.MaHP == ma_hp))
    hp = result.scalar_one_or_none()
    if not hp:
        raise HTTPException(status_code=404, detail="Tuition not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(hp, key):
            setattr(hp, key, value)
    await db.flush()
    await db.refresh(hp)
    return HocPhiResponse.model_validate(hp)
