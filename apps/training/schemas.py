"""Pydantic schemas cho Training module."""
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from backend.schemas.base import AuditSchema


# ---- LopHocPhan ----
class LopHocPhanBase(BaseModel):
    MaMH: str
    MaHK: str
    MaGV: str
    TenNhom: str | None = None
    SiSoToiDa: int = Field(default=50, ge=1)
    MoTa: str | None = None


class LopHocPhanCreate(LopHocPhanBase):
    pass


class LopHocPhanUpdate(BaseModel):
    MaGV: str | None = None
    TenNhom: str | None = None
    SiSoToiDa: int | None = Field(default=None, ge=1)
    MoTa: str | None = None


class LopHocPhanResponse(AuditSchema):
    MaLopHP: int
    MaMH: str
    MaHK: str
    MaGV: str
    TenNhom: str | None = None
    SiSoToiDa: int
    SiSoHienTai: int
    MoTa: str | None = None


# ---- DangKyHocPhan ----
class DangKyHocPhanBase(BaseModel):
    MaSV: str
    MaLopHP: int
    TrangThai: str = "ChoDuyet"
    DuocMien: bool = False
    LyDoMien: str | None = None


class DangKyHocPhanCreate(DangKyHocPhanBase):
    pass


class DangKyHocPhanUpdate(BaseModel):
    TrangThai: str | None = None
    DuocMien: bool | None = None
    LyDoMien: str | None = None


class DangKyHocPhanResponse(AuditSchema):
    MaDK: int
    MaSV: str
    MaLopHP: int
    TrangThai: str
    DuocMien: bool
    LyDoMien: str | None = None
    NgayDK: datetime | None = None
    NgayDuyet: datetime | None = None
    NguoiDuyet: str | None = None


# ---- PhanCongGiangDay ----
class PhanCongGiangDayBase(BaseModel):
    MaLopHP: int
    MaGV: str
    VaiTro: str = "GiangVienChinh"
    SoTiet: int | None = Field(default=None, ge=1, le=200)


class PhanCongGiangDayCreate(PhanCongGiangDayBase):
    pass


class PhanCongGiangDayUpdate(BaseModel):
    VaiTro: str | None = None
    SoTiet: int | None = Field(default=None, ge=1, le=200)


class PhanCongGiangDayResponse(AuditSchema):
    MaPC: int
    MaLopHP: int
    MaGV: str
    VaiTro: str | None = None
    SoTiet: int | None = None


# ---- LichHoc ----
class LichHocBase(BaseModel):
    MaPC: int
    Thu: int = Field(..., ge=2, le=8)
    TietBatDau: int = Field(..., ge=1, le=15)
    SoTiet: int = Field(..., ge=1, le=6)
    Buoi: str | None = None
    PhongHoc: str | None = None


class LichHocCreate(LichHocBase):
    pass


class LichHocUpdate(BaseModel):
    Thu: int | None = Field(default=None, ge=2, le=8)
    TietBatDau: int | None = Field(default=None, ge=1, le=15)
    SoTiet: int | None = Field(default=None, ge=1, le=6)
    Buoi: str | None = None
    PhongHoc: str | None = None


class LichHocResponse(AuditSchema):
    MaLH: int
    MaPC: int
    Thu: int
    TietBatDau: int
    SoTiet: int
    Buoi: str | None = None
    PhongHoc: str | None = None


# ---- KQ_HocTap ----
class KQ_HocTapBase(BaseModel):
    MaSV: str
    MaMH: str
    MaHK: str
    Diem: float = Field(..., ge=0, le=10)
    LoaiDiem: str = "Thi"
    GhiChu: str | None = None


class KQ_HocTapCreate(KQ_HocTapBase):
    pass


class KQ_HocTapUpdate(BaseModel):
    Diem: float | None = Field(default=None, ge=0, le=10)
    LoaiDiem: str | None = None
    GhiChu: str | None = None


class KQ_HocTapResponse(AuditSchema):
    MaSV: str
    MaMH: str
    MaHK: str
    Diem: float
    LoaiDiem: str | None = None
    DiemHe4: float | None = None
    DiemChu: str | None = None
    GhiChu: str | None = None
