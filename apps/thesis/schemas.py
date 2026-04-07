"""Pydantic schemas cho Thesis module."""
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from backend.schemas.base import AuditSchema


# ---- LuanVan ----
class LuanVanBase(BaseModel):
    MaSV: str
    MaGV: str | None = None
    TenDeTai: str
    NgayDangKy: date | None = None
    NgayBaoVe: date | None = None
    TrangThai: str = "ChuaBaoVe"
    GhiChu: str | None = None


class LuanVanCreate(LuanVanBase):
    pass


class LuanVanUpdate(BaseModel):
    MaGV: str | None = None
    TenDeTai: str | None = None
    NgayDangKy: date | None = None
    NgayBaoVe: date | None = None
    TrangThai: str | None = None
    DiemBaoVe: float | None = Field(default=None, ge=0, le=10)
    DiemHe4: float | None = Field(default=None, ge=0, le=4)
    DiemChu: str | None = None
    GhiChu: str | None = None


class LuanVanResponse(AuditSchema):
    MaLV: str
    MaSV: str
    MaGV: str | None = None
    TenDeTai: str
    NgayDangKy: date | None = None
    NgayBaoVe: date | None = None
    TrangThai: str
    DiemBaoVe: float | None = None
    DiemHe4: float | None = None
    DiemChu: str | None = None
    GhiChu: str | None = None


# ---- DeCuongLuanAn ----
class DeCuongLuanAnBase(BaseModel):
    MaLV: str
    MaSV: str
    PhienBan: int = 1
    TieuDe: str
    TomTat: str | None = None
    NoiDung: str | None = None
    FileDeCuong: str | None = None
    TrangThai: str = "Nhap"


class DeCuongLuanAnCreate(DeCuongLuanAnBase):
    pass


class DeCuongLuanAnUpdate(BaseModel):
    TieuDe: str | None = None
    TomTat: str | None = None
    NoiDung: str | None = None
    FileDeCuong: str | None = None
    TrangThai: str | None = None
    BinhLuan: str | None = None


class DeCuongLuanAnResponse(AuditSchema):
    MaDC: int
    MaLV: str
    MaSV: str
    PhienBan: int
    TieuDe: str
    TomTat: str | None = None
    NoiDung: str | None = None
    FileDeCuong: str | None = None
    TrangThai: str
    NgayNop: datetime | None = None
    NgayDuyet: datetime | None = None
    NguoiDuyet: str | None = None
    BinhLuan: str | None = None


# ---- HoiDongBaoVe ----
class HoiDongBaoVeBase(BaseModel):
    MaLV: str
    TenHD: str | None = None
    NgayThanhLap: date | None = None
    NgayBaoVe: date | None = None
    DiaDiem: str | None = None
    TrangThai: str = "ChuaThanhLap"
    GhiChu: str | None = None


class HoiDongBaoVeCreate(HoiDongBaoVeBase):
    pass


class HoiDongBaoVeUpdate(BaseModel):
    TenHD: str | None = None
    NgayThanhLap: date | None = None
    NgayBaoVe: date | None = None
    DiaDiem: str | None = None
    TrangThai: str | None = None
    GhiChu: str | None = None


class HoiDongBaoVeResponse(AuditSchema):
    MaHD: int
    MaLV: str
    TenHD: str | None = None
    NgayThanhLap: date | None = None
    NgayBaoVe: date | None = None
    DiaDiem: str | None = None
    TrangThai: str
    GhiChu: str | None = None


# ---- ThanhVienHoiDong ----
class ThanhVienHoiDongBase(BaseModel):
    MaHD: int
    MaGV: str
    VaiTro: str
    DiemDanhGia: float | None = Field(default=None, ge=0, le=10)
    NhanXet: str | None = None


class ThanhVienHoiDongCreate(ThanhVienHoiDongBase):
    pass


class ThanhVienHoiDongUpdate(BaseModel):
    VaiTro: str | None = None
    DiemDanhGia: float | None = Field(default=None, ge=0, le=10)
    NhanXet: str | None = None


class ThanhVienHoiDongResponse(AuditSchema):
    MaTVHD: int
    MaHD: int
    MaGV: str
    VaiTro: str
    DiemDanhGia: float | None = None
    NhanXet: str | None = None


# ---- ThuLaoHoiDong ----
class ThuLaoHoiDongBase(BaseModel):
    MaTVHD: int
    MaHD: int
    SoTien: float = Field(..., ge=0)
    TrangThai: str = "ChuaChiTra"
    MaGiaoDich: str | None = None
    GhiChu: str | None = None


class ThuLaoHoiDongCreate(ThuLaoHoiDongBase):
    pass


class ThuLaoHoiDongUpdate(BaseModel):
    TrangThai: str | None = None
    MaGiaoDich: str | None = None
    GhiChu: str | None = None


class ThuLaoHoiDongResponse(AuditSchema):
    MaTL: int
    MaTVHD: int
    MaHD: int
    SoTien: float
    TrangThai: str
    NgayChiTra: datetime | None = None
    MaGiaoDich: str | None = None
    GhiChu: str | None = None
