"""Thesis API router."""
from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database.engine import get_db
from backend.middleware.security import require_all
from backend.models.all_models import (
    DeCuongLuanAn,
    HoiDongBaoVe,
    LuanVan,
    ThuLaoHoiDong,
    ThanhVienHoiDong,
)
from apps.thesis.schemas import (
    DeCuongLuanAnCreate,
    DeCuongLuanAnResponse,
    DeCuongLuanAnUpdate,
    HoiDongBaoVeCreate,
    HoiDongBaoVeResponse,
    HoiDongBaoVeUpdate,
    LuanVanCreate,
    LuanVanResponse,
    LuanVanUpdate,
    ThuLaoHoiDongCreate,
    ThuLaoHoiDongResponse,
    ThuLaoHoiDongUpdate,
    ThanhVienHoiDongCreate,
    ThanhVienHoiDongResponse,
    ThanhVienHoiDongUpdate,
)
from backend.utils.grade import diem_10_to_chu, diem_10_to_he4

router = APIRouter(prefix="/thesis", tags=["Thesis"])


# ---- LuanVan ----
@router.post("/theses", response_model=LuanVanResponse, dependencies=[Depends(require_all)])
async def create_thesis(
    data: LuanVanCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LuanVanResponse:
    """Create thesis record."""
    lv = LuanVan(**data.model_dump())
    db.add(lv)
    await db.flush()
    await db.refresh(lv)
    return LuanVanResponse.model_validate(lv)


@router.get("/theses", response_model=list[LuanVanResponse], dependencies=[Depends(require_all)])
async def list_theses(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_sv: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[LuanVanResponse]:
    """List theses."""
    stmt = select(LuanVan).where(LuanVan.is_active == True)  # noqa: E712
    if ma_sv:
        stmt = stmt.where(LuanVan.MaSV == ma_sv)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [LuanVanResponse.model_validate(t) for t in result.scalars().all()]


@router.get("/theses/{ma_lv}", response_model=LuanVanResponse, dependencies=[Depends(require_all)])
async def get_thesis(
    ma_lv: str,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LuanVanResponse:
    """Get thesis by MaLV."""
    result = await db.execute(select(LuanVan).where(LuanVan.MaLV == ma_lv))
    lv = result.scalar_one_or_none()
    if not lv:
        raise HTTPException(status_code=404, detail="Thesis not found")
    return LuanVanResponse.model_validate(lv)


@router.put("/theses/{ma_lv}", response_model=LuanVanResponse, dependencies=[Depends(require_all)])
async def update_thesis(
    ma_lv: str,
    data: LuanVanUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LuanVanResponse:
    """Update thesis (including final grade). BR-04, BR-09 enforced."""
    result = await db.execute(select(LuanVan).where(LuanVan.MaLV == ma_lv))
    lv = result.scalar_one_or_none()
    if not lv:
        raise HTTPException(status_code=404, detail="Thesis not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(lv, key):
            setattr(lv, key, value)
    # Auto-calculate grade conversion on DiemBaoVe change
    if data.DiemBaoVe is not None:
        lv.DiemHe4 = diem_10_to_he4(data.DiemBaoVe)
        lv.DiemChu = diem_10_to_chu(data.DiemBaoVe)
        lv.TrangThai = "DaBaoVe"
    await db.flush()
    await db.refresh(lv)
    return LuanVanResponse.model_validate(lv)


# ---- DeCuongLuanAn ----
@router.post("/outlines", response_model=DeCuongLuanAnResponse, dependencies=[Depends(require_all)])
async def create_outline(
    data: DeCuongLuanAnCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeCuongLuanAnResponse:
    """Submit thesis outline."""
    dc = DeCuongLuanAn(**data.model_dump())
    db.add(dc)
    await db.flush()
    await db.refresh(dc)
    return DeCuongLuanAnResponse.model_validate(dc)


@router.get("/outlines", response_model=list[DeCuongLuanAnResponse], dependencies=[Depends(require_all)])
async def list_outlines(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_lv: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[DeCuongLuanAnResponse]:
    """List thesis outlines."""
    stmt = select(DeCuongLuanAn).where(DeCuongLuanAn.is_active == True)  # noqa: E712
    if ma_lv:
        stmt = stmt.where(DeCuongLuanAn.MaLV == ma_lv)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [DeCuongLuanAnResponse.model_validate(o) for o in result.scalars().all()]


@router.put("/outlines/{ma_dc}", response_model=DeCuongLuanAnResponse, dependencies=[Depends(require_all)])
async def update_outline(
    ma_dc: int,
    data: DeCuongLuanAnUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DeCuongLuanAnResponse:
    """Update/approve thesis outline."""
    result = await db.execute(select(DeCuongLuanAn).where(DeCuongLuanAn.MaDC == ma_dc))
    dc = result.scalar_one_or_none()
    if not dc:
        raise HTTPException(status_code=404, detail="Outline not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(dc, key):
            setattr(dc, key, value)
    if data.TrangThai == "DaDuyet":
        dc.NgayDuyet = datetime.now(timezone.utc)
    await db.flush()
    await db.refresh(dc)
    return DeCuongLuanAnResponse.model_validate(dc)


# ---- HoiDongBaoVe ----
@router.post("/committees", response_model=HoiDongBaoVeResponse, dependencies=[Depends(require_all)])
async def create_committee(
    data: HoiDongBaoVeCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HoiDongBaoVeResponse:
    """Create thesis defense committee. BR-07 (required roles)."""
    hd = HoiDongBaoVe(**data.model_dump())
    db.add(hd)
    await db.flush()
    await db.refresh(hd)
    return HoiDongBaoVeResponse.model_validate(hd)


@router.get("/committees", response_model=list[HoiDongBaoVeResponse], dependencies=[Depends(require_all)])
async def list_committees(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[HoiDongBaoVeResponse]:
    """List committees."""
    result = await db.execute(
        select(HoiDongBaoVe).where(HoiDongBaoVe.is_active == True)  # noqa: E712
        .offset(skip).limit(limit)
    )
    return [HoiDongBaoVeResponse.model_validate(c) for c in result.scalars().all()]


@router.put("/committees/{ma_hd}", response_model=HoiDongBaoVeResponse, dependencies=[Depends(require_all)])
async def update_committee(
    ma_hd: int,
    data: HoiDongBaoVeUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> HoiDongBaoVeResponse:
    """Update committee."""
    result = await db.execute(select(HoiDongBaoVe).where(HoiDongBaoVe.MaHD == ma_hd))
    hd = result.scalar_one_or_none()
    if not hd:
        raise HTTPException(status_code=404, detail="Committee not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(hd, key):
            setattr(hd, key, value)
    await db.flush()
    await db.refresh(hd)
    return HoiDongBaoVeResponse.model_validate(hd)


# ---- ThanhVienHoiDong ----
@router.post("/committee-members", response_model=ThanhVienHoiDongResponse, dependencies=[Depends(require_all)])
async def create_committee_member(
    data: ThanhVienHoiDongCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ThanhVienHoiDongResponse:
    """Add member to committee. BR-07: ChuTich, PhoChuTich, ThuKy, PhanBien1, PhanBien2."""
    tv = ThanhVienHoiDong(**data.model_dump())
    db.add(tv)
    await db.flush()
    await db.refresh(tv)
    return ThanhVienHoiDongResponse.model_validate(tv)


@router.get("/committee-members", response_model=list[ThanhVienHoiDongResponse], dependencies=[Depends(require_all)])
async def list_committee_members(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_hd: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[ThanhVienHoiDongResponse]:
    """List committee members."""
    stmt = select(ThanhVienHoiDong).where(ThanhVienHoiDong.is_active == True)  # noqa: E712
    if ma_hd:
        stmt = stmt.where(ThanhVienHoiDong.MaHD == ma_hd)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [ThanhVienHoiDongResponse.model_validate(m) for m in result.scalars().all()]


@router.put("/committee-members/{ma_tvhd}", response_model=ThanhVienHoiDongResponse, dependencies=[Depends(require_all)])
async def update_committee_member(
    ma_tvhd: int,
    data: ThanhVienHoiDongUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ThanhVienHoiDongResponse:
    """Update committee member."""
    result = await db.execute(select(ThanhVienHoiDong).where(ThanhVienHoiDong.MaTVHD == ma_tvhd))
    tv = result.scalar_one_or_none()
    if not tv:
        raise HTTPException(status_code=404, detail="Member not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(tv, key):
            setattr(tv, key, value)
    await db.flush()
    await db.refresh(tv)
    return ThanhVienHoiDongResponse.model_validate(tv)


# ---- ThuLaoHoiDong ----
@router.post("/stipends", response_model=ThuLaoHoiDongResponse, dependencies=[Depends(require_all)])
async def create_stipend(
    data: ThuLaoHoiDongCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ThuLaoHoiDongResponse:
    """Create stipend record."""
    tl = ThuLaoHoiDong(**data.model_dump())
    db.add(tl)
    await db.flush()
    await db.refresh(tl)
    return ThuLaoHoiDongResponse.model_validate(tl)


@router.get("/stipends", response_model=list[ThuLaoHoiDongResponse], dependencies=[Depends(require_all)])
async def list_stipends(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_hd: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[ThuLaoHoiDongResponse]:
    """List stipends."""
    stmt = select(ThuLaoHoiDong).where(ThuLaoHoiDong.is_active == True)  # noqa: E712
    if ma_hd:
        stmt = stmt.where(ThuLaoHoiDong.MaHD == ma_hd)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [ThuLaoHoiDongResponse.model_validate(s) for s in result.scalars().all()]


@router.put("/stipends/{ma_tl}", response_model=ThuLaoHoiDongResponse, dependencies=[Depends(require_all)])
async def update_stipend(
    ma_tl: int,
    data: ThuLaoHoiDongUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ThuLaoHoiDongResponse:
    """Update stipend."""
    result = await db.execute(select(ThuLaoHoiDong).where(ThuLaoHoiDong.MaTL == ma_tl))
    tl = result.scalar_one_or_none()
    if not tl:
        raise HTTPException(status_code=404, detail="Stipend not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(tl, key):
            setattr(tl, key, value)
    await db.flush()
    await db.refresh(tl)
    return ThuLaoHoiDongResponse.model_validate(tl)
