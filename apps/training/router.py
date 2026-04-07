"""Training API router."""
from datetime import datetime, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database.engine import get_db
from backend.middleware.security import CurrentUser, require_all, require_gv
from backend.models.all_models import (
    DangKyHocPhan,
    GiangVien,
    KQ_HocTap,
    LichHoc,
    LopHocPhan,
    PhanCongGiangDay,
    SinhVien,
)
from apps.training.schemas import (
    DangKyHocPhanCreate,
    DangKyHocPhanResponse,
    DangKyHocPhanUpdate,
    KQ_HocTapCreate,
    KQ_HocTapResponse,
    KQ_HocTapUpdate,
    LichHocCreate,
    LichHocResponse,
    LichHocUpdate,
    LopHocPhanCreate,
    LopHocPhanResponse,
    LopHocPhanUpdate,
    PhanCongGiangDayCreate,
    PhanCongGiangDayResponse,
    PhanCongGiangDayUpdate,
)
from backend.utils.grade import diem_10_to_chu, diem_10_to_he4

router = APIRouter(prefix="/training", tags=["Training"])


# ---- LopHocPhan ----
@router.post("/class-sections", response_model=LopHocPhanResponse, dependencies=[Depends(require_all)])
async def create_class_section(
    data: LopHocPhanCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LopHocPhanResponse:
    """Create a new class section (admin/khoa)."""
    lhp = LopHocPhan(**data.model_dump())
    db.add(lhp)
    await db.flush()
    await db.refresh(lhp)
    return LopHocPhanResponse.model_validate(lhp)


@router.get("/class-sections", response_model=list[LopHocPhanResponse], dependencies=[Depends(require_all)])
async def list_class_sections(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_hk: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[LopHocPhanResponse]:
    """List class sections."""
    stmt = select(LopHocPhan).where(LopHocPhan.is_active == True)  # noqa: E712
    if ma_hk:
        stmt = stmt.where(LopHocPhan.MaHK == ma_hk)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [LopHocPhanResponse.model_validate(l) for l in result.scalars().all()]


@router.put("/class-sections/{ma_lophp}", response_model=LopHocPhanResponse, dependencies=[Depends(require_all)])
async def update_class_section(
    ma_lophp: int,
    data: LopHocPhanUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LopHocPhanResponse:
    """Update class section."""
    result = await db.execute(select(LopHocPhan).where(LopHocPhan.MaLopHP == ma_lophp))
    lhp = result.scalar_one_or_none()
    if not lhp:
        raise HTTPException(status_code=404, detail="Class section not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(lhp, key):
            setattr(lhp, key, value)
    await db.flush()
    await db.refresh(lhp)
    return LopHocPhanResponse.model_validate(lhp)


# ---- DangKyHocPhan ----
@router.post("/enrollments", response_model=DangKyHocPhanResponse, dependencies=[Depends(require_all)])
async def create_enrollment(
    data: DangKyHocPhanCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DangKyHocPhanResponse:
    """Student enrolls in a class section. BR-01 (tiên quyết) & BR-02 (sĩ số) enforced by DB."""
    dk = DangKyHocPhan(**data.model_dump())
    db.add(dk)
    await db.flush()
    await db.refresh(dk)
    return DangKyHocPhanResponse.model_validate(dk)


@router.get("/enrollments", response_model=list[DangKyHocPhanResponse], dependencies=[Depends(require_all)])
async def list_enrollments(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_sv: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[DangKyHocPhanResponse]:
    """List enrollments."""
    stmt = select(DangKyHocPhan).where(DangKyHocPhan.is_active == True)  # noqa: E712
    if ma_sv:
        stmt = stmt.where(DangKyHocPhan.MaSV == ma_sv)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [DangKyHocPhanResponse.model_validate(e) for e in result.scalars().all()]


@router.put("/enrollments/{ma_dk}", response_model=DangKyHocPhanResponse, dependencies=[Depends(require_all)])
async def update_enrollment(
    ma_dk: int,
    data: DangKyHocPhanUpdate,
    current_user: CurrentUser,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> DangKyHocPhanResponse:
    """Approve/reject enrollment. Updates SiSoHienTai on LopHocPhan via BR-02."""
    result = await db.execute(select(DangKyHocPhan).where(DangKyHocPhan.MaDK == ma_dk))
    dk = result.scalar_one_or_none()
    if not dk:
        raise HTTPException(status_code=404, detail="Enrollment not found")

    old_trang_thai = dk.TrangThai
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(dk, key):
            setattr(dk, key, value)

    # Auto-set NgayDuyet when approved
    if data.TrangThai == "DaDuyet" and old_trang_thai != "DaDuyet":
        dk.NgayDuyet = datetime.now(timezone.utc)
        # Check seat limit (BR-02)
        lhp_result = await db.execute(select(LopHocPhan).where(LopHocPhan.MaLopHP == dk.MaLopHP))
        lhp = lhp_result.scalar_one()
        if lhp.SiSoHienTai >= lhp.SiSoToiDa:
            raise HTTPException(status_code=400, detail="Class section is full")
        lhp.SiSoHienTai += 1
    elif old_trang_thai == "DaDuyet" and data.TrangThai and data.TrangThai != "DaDuyet":
        # Un-approve: decrement seat count
        lhp_result = await db.execute(select(LopHocPhan).where(LopHocPhan.MaLopHP == dk.MaLopHP))
        lhp = lhp_result.scalar_one()
        if lhp.SiSoHienTai > 0:
            lhp.SiSoHienTai -= 1

    await db.flush()
    await db.refresh(dk)
    return DangKyHocPhanResponse.model_validate(dk)


# ---- PhanCongGiangDay ----
@router.post("/assignments", response_model=PhanCongGiangDayResponse, dependencies=[Depends(require_all)])
async def create_assignment(
    data: PhanCongGiangDayCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PhanCongGiangDayResponse:
    """Assign lecturer to class section. BR-06 (vai trò)."""
    pc = PhanCongGiangDay(**data.model_dump())
    db.add(pc)
    await db.flush()
    await db.refresh(pc)
    return PhanCongGiangDayResponse.model_validate(pc)


@router.get("/assignments", response_model=list[PhanCongGiangDayResponse], dependencies=[Depends(require_all)])
async def list_assignments(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_lophp: int | None = None,
    ma_gv: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[PhanCongGiangDayResponse]:
    """List teaching assignments."""
    stmt = select(PhanCongGiangDay).where(PhanCongGiangDay.is_active == True)  # noqa: E712
    if ma_lophp:
        stmt = stmt.where(PhanCongGiangDay.MaLopHP == ma_lophp)
    if ma_gv:
        stmt = stmt.where(PhanCongGiangDay.MaGV == ma_gv)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [PhanCongGiangDayResponse.model_validate(a) for a in result.scalars().all()]


@router.put("/assignments/{ma_pc}", response_model=PhanCongGiangDayResponse, dependencies=[Depends(require_all)])
async def update_assignment(
    ma_pc: int,
    data: PhanCongGiangDayUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> PhanCongGiangDayResponse:
    """Update teaching assignment."""
    result = await db.execute(select(PhanCongGiangDay).where(PhanCongGiangDay.MaPC == ma_pc))
    pc = result.scalar_one_or_none()
    if not pc:
        raise HTTPException(status_code=404, detail="Assignment not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(pc, key):
            setattr(pc, key, value)
    await db.flush()
    await db.refresh(pc)
    return PhanCongGiangDayResponse.model_validate(pc)


# ---- LichHoc ----
@router.post("/schedules", response_model=LichHocResponse, dependencies=[Depends(require_all)])
async def create_schedule(
    data: LichHocCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LichHocResponse:
    """Create class schedule. BR-03 (xung đột lịch) enforced by DB trigger."""
    lh = LichHoc(**data.model_dump())
    db.add(lh)
    await db.flush()
    await db.refresh(lh)
    return LichHocResponse.model_validate(lh)


@router.get("/schedules", response_model=list[LichHocResponse], dependencies=[Depends(require_all)])
async def list_schedules(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_pc: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[LichHocResponse]:
    """List schedules."""
    stmt = select(LichHoc).where(LichHoc.is_active == True)  # noqa: E712
    if ma_pc:
        stmt = stmt.where(LichHoc.MaPC == ma_pc)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [LichHocResponse.model_validate(s) for s in result.scalars().all()]


# ---- KQ_HocTap ----
@router.post("/grades", response_model=KQ_HocTapResponse, dependencies=[Depends(require_gv)])
async def create_grade(
    data: KQ_HocTapCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> KQ_HocTapResponse:
    """Enter grade. BR-04 (quy đổi điểm) applied automatically."""
    kq = KQ_HocTap(**data.model_dump())
    # Auto-calculate DiemHe4 and DiemChu (BR-04)
    kq.DiemHe4 = diem_10_to_he4(data.Diem)
    kq.DiemChu = diem_10_to_chu(data.Diem)
    db.add(kq)
    await db.flush()
    await db.refresh(kq)
    return KQ_HocTapResponse.model_validate(kq)


@router.get("/grades", response_model=list[KQ_HocTapResponse], dependencies=[Depends(require_all)])
async def list_grades(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_sv: str | None = None,
    ma_hk: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[KQ_HocTapResponse]:
    """List grades."""
    stmt = select(KQ_HocTap).where(KQ_HocTap.is_active == True)  # noqa: E712
    if ma_sv:
        stmt = stmt.where(KQ_HocTap.MaSV == ma_sv)
    if ma_hk:
        stmt = stmt.where(KQ_HocTap.MaHK == ma_hk)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [KQ_HocTapResponse.model_validate(g) for g in result.scalars().all()]


@router.put("/grades/{ma_sv}/{ma_mh}/{ma_hk}", response_model=KQ_HocTapResponse, dependencies=[Depends(require_gv)])
async def update_grade(
    ma_sv: str,
    ma_mh: str,
    ma_hk: str,
    data: KQ_HocTapUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> KQ_HocTapResponse:
    """Update grade."""
    result = await db.execute(
        select(KQ_HocTap).where(
            KQ_HocTap.MaSV == ma_sv,
            KQ_HocTap.MaMH == ma_mh,
            KQ_HocTap.MaHK == ma_hk,
        )
    )
    kq = result.scalar_one_or_none()
    if not kq:
        raise HTTPException(status_code=404, detail="Grade not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(kq, key):
            setattr(kq, key, value)
    # Re-calculate grade conversion if Diem changed
    if data.Diem is not None:
        kq.DiemHe4 = diem_10_to_he4(data.Diem)
        kq.DiemChu = diem_10_to_chu(data.Diem)
    await db.flush()
    await db.refresh(kq)
    return KQ_HocTapResponse.model_validate(kq)
