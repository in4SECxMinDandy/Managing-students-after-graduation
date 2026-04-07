"""Pydantic schemas cho common/system entities (Khoa, Nganh, Lop, HocKy, MonHoc)."""
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field

from backend.schemas.base import AuditSchema


# ---- Khoa ----
class KhoaBase(BaseModel):
    TenKhoa: str = Field(..., min_length=1, max_length=100)
    DiaChi: str | None = None
    SDT: str | None = None
    Email: str | None = None


class KhoaCreate(KhoaBase):
    MaKhoa: str = Field(..., min_length=1, max_length=5)


class KhoaUpdate(BaseModel):
    TenKhoa: str | None = None
    DiaChi: str | None = None
    SDT: str | None = None
    Email: str | None = None


class KhoaResponse(AuditSchema):
    MaKhoa: str
    TenKhoa: str
    DiaChi: str | None = None
    SDT: str | None = None
    Email: str | None = None


# ---- Nganh ----
class NganhBase(BaseModel):
    TenNganh: str = Field(..., min_length=1, max_length=100)
    MaKhoa: str | None = None
    MoTa: str | None = None


class NganhCreate(NganhBase):
    MaNganh: str = Field(..., min_length=1, max_length=10)


class NganhUpdate(BaseModel):
    TenNganh: str | None = None
    MaKhoa: str | None = None
    MoTa: str | None = None


class NganhResponse(AuditSchema):
    MaNganh: str
    TenNganh: str
    MaKhoa: str | None = None
    MoTa: str | None = None


# ---- Lop ----
class LopBase(BaseModel):
    TenLop: str = Field(..., min_length=1, max_length=100)
    MaNganh: str | None = None
    SiSo: int | None = None


class LopCreate(LopBase):
    MaLop: str = Field(..., min_length=1, max_length=15)


class LopUpdate(BaseModel):
    TenLop: str | None = None
    MaNganh: str | None = None
    SiSo: int | None = None


class LopResponse(AuditSchema):
    MaLop: str
    TenLop: str
    MaNganh: str | None = None
    SiSo: int | None = None


# ---- HocKy ----
class HocKyBase(BaseModel):
    TenHK: str = Field(..., min_length=1, max_length=50)
    NamHoc: str = Field(..., pattern=r"^\d{4}-\d{4}$")
    ThoiGianBD: date
    ThoiGianKT: date


class HocKyCreate(HocKyBase):
    MaHK: str = Field(..., min_length=1, max_length=10)


class HocKyUpdate(BaseModel):
    TenHK: str | None = None
    NamHoc: str | None = None
    ThoiGianBD: date | None = None
    ThoiGianKT: date | None = None


class HocKyResponse(AuditSchema):
    MaHK: str
    TenHK: str
    NamHoc: str
    ThoiGianBD: date
    ThoiGianKT: date


# ---- MonHoc ----
class MonHocBase(BaseModel):
    TenMH: str = Field(..., min_length=1, max_length=100)
    SoTinChi: int = Field(..., ge=1, le=10)
    MoTa: str | None = None


class MonHocCreate(MonHocBase):
    MaMH: str = Field(..., min_length=1, max_length=10)


class MonHocUpdate(BaseModel):
    TenMH: str | None = None
    SoTinChi: int | None = Field(default=None, ge=1, le=10)
    MoTa: str | None = None


class MonHocResponse(AuditSchema):
    MaMH: str
    TenMH: str
    SoTinChi: int
    MoTa: str | None = None


# ---- ChuongTrinhDaoTao ----
class ChuongTrinhDaoTaoBase(BaseModel):
    MaNganh: str
    MaMH: str
    HocKy: int | None = Field(default=None, ge=1, le=20)
    LoaiMH: str = "BatBuoc"


class ChuongTrinhDaoTaoCreate(ChuongTrinhDaoTaoBase):
    pass


class ChuongTrinhDaoTaoUpdate(BaseModel):
    HocKy: int | None = Field(default=None, ge=1, le=20)
    LoaiMH: str | None = None


class ChuongTrinhDaoTaoResponse(AuditSchema):
    MaCTDT: int
    MaNganh: str
    MaMH: str
    HocKy: int | None = None
    LoaiMH: str | None = None


# ---- MonHocTienQuyet ----
class MonHocTienQuyetBase(BaseModel):
    MaMH: str
    MaMHTienQuyet: str
    MoTa: str | None = None


class MonHocTienQuyetCreate(MonHocTienQuyetBase):
    pass


class MonHocTienQuyetResponse(AuditSchema):
    MaMH: str
    MaMHTienQuyet: str
    MoTa: str | None = None
