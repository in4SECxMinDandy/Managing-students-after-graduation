"""Support API router."""
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.database.engine import get_db
from backend.middleware.security import require_all, require_admin
from backend.models.all_models import (
    LichThi,
    NghienCuuKhoaHoc,
    QuyDinhDacThu,
    TacGiaCongTrinh,
    TB_NguoiNhan,
    ThongBao,
    TotNghiep,
)
from apps.support.schemas import (
    LichThiCreate,
    LichThiResponse,
    LichThiUpdate,
    NghienCuuKhoaHocCreate,
    NghienCuuKhoaHocResponse,
    NghienCuuKhoaHocUpdate,
    QuyDinhDacThuCreate,
    QuyDinhDacThuResponse,
    QuyDinhDacThuUpdate,
    TacGiaCongTrinhCreate,
    TacGiaCongTrinhResponse,
    TB_NguoiNhanCreate,
    TB_NguoiNhanResponse,
    ThongBaoCreate,
    ThongBaoResponse,
    ThongBaoUpdate,
    TotNghiepCreate,
    TotNghiepResponse,
)
from backend.utils.grade import gpa_to_xep_loai, tinh_tong_tin_chi

router = APIRouter(prefix="/support", tags=["Support"])


# ---- ThongBao ----
@router.post("/announcements", response_model=ThongBaoResponse, dependencies=[Depends(require_admin)])
async def create_announcement(
    data: ThongBaoCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> ThongBaoResponse:
    """Create announcement."""
    tb = ThongBao(**data.model_dump())
    db.add(tb)
    await db.flush()
    await db.refresh(tb)
    return ThongBaoResponse.model_validate(tb)


@router.get("/announcements", response_model=list[ThongBaoResponse], dependencies=[Depends(require_all)])
async def list_announcements(
    db: Annotated[AsyncSession, Depends(get_db)],
    loai_tb: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[ThongBaoResponse]:
    """List announcements."""
    stmt = select(ThongBao).where(ThongBao.is_active == True)  # noqa: E712
    if loai_tb:
        stmt = stmt.where(ThongBao.LoaiTB == loai_tb)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [ThongBaoResponse.model_validate(a) for a in result.scalars().all()]


# ---- TB_NguoiNhan ----
@router.post("/recipients", response_model=TB_NguoiNhanResponse, dependencies=[Depends(require_admin)])
async def create_recipient(
    data: TB_NguoiNhanCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TB_NguoiNhanResponse:
    """Add recipient to announcement."""
    tbnn = TB_NguoiNhan(**data.model_dump())
    db.add(tbnn)
    await db.flush()
    await db.refresh(tbnn)
    return TB_NguoiNhanResponse.model_validate(tbnn)


# ---- NghienCuuKhoaHoc ----
@router.post("/research", response_model=NghienCuuKhoaHocResponse, dependencies=[Depends(require_all)])
async def create_research(
    data: NghienCuuKhoaHocCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> NghienCuuKhoaHocResponse:
    """Create research publication."""
    nckh = NghienCuuKhoaHoc(**data.model_dump())
    db.add(nckh)
    await db.flush()
    await db.refresh(nckh)
    return NghienCuuKhoaHocResponse.model_validate(nckh)


@router.get("/research", response_model=list[NghienCuuKhoaHocResponse], dependencies=[Depends(require_all)])
async def list_research(
    db: Annotated[AsyncSession, Depends(get_db)],
    loai: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[NghienCuuKhoaHocResponse]:
    """List research publications."""
    stmt = select(NghienCuuKhoaHoc).where(NghienCuuKhoaHoc.is_active == True)  # noqa: E712
    if loai:
        stmt = stmt.where(NghienCuuKhoaHoc.LoaiCongTrinh == loai)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [NghienCuuKhoaHocResponse.model_validate(r) for r in result.scalars().all()]


@router.put("/research/{ma_nckh}", response_model=NghienCuuKhoaHocResponse, dependencies=[Depends(require_all)])
async def update_research(
    ma_nckh: int,
    data: NghienCuuKhoaHocUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> NghienCuuKhoaHocResponse:
    """Update research publication."""
    result = await db.execute(select(NghienCuuKhoaHoc).where(NghienCuuKhoaHoc.MaNCKH == ma_nckh))
    nckh = result.scalar_one_or_none()
    if not nckh:
        raise HTTPException(status_code=404, detail="Research not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(nckh, key):
            setattr(nckh, key, value)
    await db.flush()
    await db.refresh(nckh)
    return NghienCuuKhoaHocResponse.model_validate(nckh)


# ---- TacGiaCongTrinh ----
@router.post("/research-authors", response_model=TacGiaCongTrinhResponse, dependencies=[Depends(require_all)])
async def create_author(
    data: TacGiaCongTrinhCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TacGiaCongTrinhResponse:
    """Add author to research."""
    tg = TacGiaCongTrinh(**data.model_dump())
    db.add(tg)
    await db.flush()
    await db.refresh(tg)
    return TacGiaCongTrinhResponse.model_validate(tg)


@router.get("/research-authors", response_model=list[TacGiaCongTrinhResponse], dependencies=[Depends(require_all)])
async def list_authors(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_nckh: int | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[TacGiaCongTrinhResponse]:
    """List authors."""
    stmt = select(TacGiaCongTrinh).where(TacGiaCongTrinh.is_active == True)  # noqa: E712
    if ma_nckh:
        stmt = stmt.where(TacGiaCongTrinh.MaNCKH == ma_nckh)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [TacGiaCongTrinhResponse.model_validate(a) for a in result.scalars().all()]


# ---- QuyDinhDacThu ----
@router.post("/regulations", response_model=QuyDinhDacThuResponse, dependencies=[Depends(require_admin)])
async def create_regulation(
    data: QuyDinhDacThuCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> QuyDinhDacThuResponse:
    """Create specific regulation."""
    qd = QuyDinhDacThu(**data.model_dump())
    db.add(qd)
    await db.flush()
    await db.refresh(qd)
    return QuyDinhDacThuResponse.model_validate(qd)


@router.get("/regulations", response_model=list[QuyDinhDacThuResponse], dependencies=[Depends(require_all)])
async def list_regulations(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_nganh: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[QuyDinhDacThuResponse]:
    """List specific regulations."""
    stmt = select(QuyDinhDacThu).where(QuyDinhDacThu.is_active == True)  # noqa: E712
    if ma_nganh:
        stmt = stmt.where(QuyDinhDacThu.MaNganh == ma_nganh)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [QuyDinhDacThuResponse.model_validate(r) for r in result.scalars().all()]


@router.put("/regulations/{ma_qd}", response_model=QuyDinhDacThuResponse, dependencies=[Depends(require_admin)])
async def update_regulation(
    ma_qd: int,
    data: QuyDinhDacThuUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> QuyDinhDacThuResponse:
    """Update regulation."""
    result = await db.execute(select(QuyDinhDacThu).where(QuyDinhDacThu.MaQD == ma_qd))
    qd = result.scalar_one_or_none()
    if not qd:
        raise HTTPException(status_code=404, detail="Regulation not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(qd, key):
            setattr(qd, key, value)
    await db.flush()
    await db.refresh(qd)
    return QuyDinhDacThuResponse.model_validate(qd)


# ---- TotNghiep ----
@router.post("/graduations", response_model=TotNghiepResponse, dependencies=[Depends(require_admin)])
async def create_graduation(
    data: TotNghiepCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> TotNghiepResponse:
    """Record graduation. BR-08: GPA classification applied."""
    tg = TotNghiep(**data.model_dump())
    tg.XepLoai = gpa_to_xep_loai(float(data.GPA))
    db.add(tg)
    await db.flush()
    await db.refresh(tg)
    return TotNghiepResponse.model_validate(tg)


@router.get("/graduations", response_model=list[TotNghiepResponse], dependencies=[Depends(require_all)])
async def list_graduations(
    db: Annotated[AsyncSession, Depends(get_db)],
    skip: int = 0,
    limit: int = 100,
) -> list[TotNghiepResponse]:
    """List graduation records."""
    result = await db.execute(
        select(TotNghiep).where(TotNghiep.is_active == True)  # noqa: E712
        .offset(skip).limit(limit)
    )
    return [TotNghiepResponse.model_validate(g) for g in result.scalars().all()]


# ---- LichThi ----
@router.post("/exam-schedules", response_model=LichThiResponse, dependencies=[Depends(require_admin)])
async def create_exam_schedule(
    data: LichThiCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LichThiResponse:
    """Create exam schedule."""
    lt = LichThi(**data.model_dump())
    db.add(lt)
    await db.flush()
    await db.refresh(lt)
    return LichThiResponse.model_validate(lt)


@router.get("/exam-schedules", response_model=list[LichThiResponse], dependencies=[Depends(require_all)])
async def list_exam_schedules(
    db: Annotated[AsyncSession, Depends(get_db)],
    ma_hk: str | None = None,
    skip: int = 0,
    limit: int = 100,
) -> list[LichThiResponse]:
    """List exam schedules."""
    stmt = select(LichThi).where(LichThi.is_active == True)  # noqa: E712
    if ma_hk:
        stmt = stmt.where(LichThi.MaHK == ma_hk)
    result = await db.execute(stmt.offset(skip).limit(limit))
    return [LichThiResponse.model_validate(e) for e in result.scalars().all()]


@router.put("/exam-schedules/{ma_lt}", response_model=LichThiResponse, dependencies=[Depends(require_admin)])
async def update_exam_schedule(
    ma_lt: int,
    data: LichThiUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
) -> LichThiResponse:
    """Update exam schedule."""
    result = await db.execute(select(LichThi).where(LichThi.MaLT == ma_lt))
    lt = result.scalar_one_or_none()
    if not lt:
        raise HTTPException(status_code=404, detail="Exam schedule not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        if hasattr(lt, key):
            setattr(lt, key, value)
    await db.flush()
    await db.refresh(lt)
    return LichThiResponse.model_validate(lt)
