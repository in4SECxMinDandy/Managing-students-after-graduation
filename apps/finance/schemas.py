"""Pydantic schemas cho Finance module."""
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from backend.schemas.base import AuditSchema


# ---- DonGiaTinChi ----
class DonGiaTinChiBase(BaseModel):
    NamHoc: str = Field(..., pattern=r"^\d{4}-\d{4}$")
    HeDaoTao: str
    MaNganh: str | None = None
    DonGia: float = Field(..., gt=0)


class DonGiaTinChiCreate(DonGiaTinChiBase):
    pass


class DonGiaTinChiUpdate(BaseModel):
    DonGia: float | None = Field(default=None, gt=0)
    is_active: bool | None = None


class DonGiaTinChiResponse(AuditSchema):
    MaDonGia: int
    NamHoc: str
    HeDaoTao: str
    MaNganh: str | None = None
    DonGia: float


# ---- HocPhi ----
class HocPhiBase(BaseModel):
    MaSV: str
    MaHK: str
    SoTien: float = Field(..., gt=0)
    TrangThai: str = "ChuaDong"
    NgayHanNop: date | None = None
    MaGiaoDich: str | None = None
    GhiChu: str | None = None


class HocPhiCreate(HocPhiBase):
    pass


class HocPhiUpdate(BaseModel):
    TrangThai: str | None = None
    MaGiaoDich: str | None = None
    GhiChu: str | None = None


class HocPhiResponse(AuditSchema):
    MaHP: int
    MaSV: str
    MaHK: str
    SoTien: float
    TrangThai: str
    NgayHanNop: date | None = None
    NgayDong: datetime | None = None
    MaGiaoDich: str | None = None
    GhiChu: str | None = None
