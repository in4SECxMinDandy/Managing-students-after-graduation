"""Pydantic schemas cho Auth module."""
from datetime import date, datetime

from pydantic import BaseModel, EmailStr, Field

from backend.schemas.base import AuditSchema


# ---- Login / Token ----
class LoginRequest(BaseModel):
    """Request body for login."""

    username: str = Field(..., min_length=1, max_length=50)
    password: str = Field(..., min_length=1)


class TokenResponse(BaseModel):
    """JWT token response."""

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user_id: str | None = None
    ho_ten: str | None = None
    role: str | None = None


class RefreshRequest(BaseModel):
    """Request body for token refresh."""

    refresh_token: str


class RefreshResponse(BaseModel):
    """Refreshed token response."""

    access_token: str
    token_type: str = "bearer"


# ---- QuanTri ----
class QuanTriBase(BaseModel):
    """Base schema for QuanTri."""

    MaAdmin: str
    TenDN: str
    HoTen: str
    Email: EmailStr
    SDT: str | None = None
    VaiTro: str = "admin"


class QuanTriCreate(QuanTriBase):
    """Schema for creating QuanTri."""

    MatKhau: str = Field(..., min_length=6)


class QuanTriUpdate(BaseModel):
    """Schema for updating QuanTri."""

    TenDN: str | None = None
    HoTen: str | None = None
    Email: EmailStr | None = None
    SDT: str | None = None
    VaiTro: str | None = None
    MatKhau: str | None = Field(default=None, min_length=6)


class QuanTriResponse(AuditSchema):
    """Response schema for QuanTri."""

    MaAdmin: str
    TenDN: str
    HoTen: str
    Email: str
    SDT: str | None = None
    VaiTro: str


# ---- GiangVien ----
class GiangVienBase(BaseModel):
    """Base schema for GiangVien."""

    MaGV: str
    HoTen: str
    Email: EmailStr
    SDT: str | None = None
    HocVi: str | None = None
    HocHam: str | None = None
    ChuyenNganh: str | None = None
    DiaChi: str | None = None
    MaKhoa: str | None = None


class GiangVienCreate(GiangVienBase):
    """Schema for creating GiangVien."""

    MatKhau: str = Field(..., min_length=6)


class GiangVienUpdate(BaseModel):
    """Schema for updating GiangVien."""

    HoTen: str | None = None
    Email: EmailStr | None = None
    SDT: str | None = None
    HocVi: str | None = None
    HocHam: str | None = None
    ChuyenNganh: str | None = None
    DiaChi: str | None = None
    MaKhoa: str | None = None
    MatKhau: str | None = Field(default=None, min_length=6)


class GiangVienResponse(AuditSchema):
    """Response schema for GiangVien."""

    MaGV: str
    HoTen: str
    Email: str
    SDT: str | None = None
    HocVi: str | None = None
    HocHam: str | None = None
    ChuyenNganh: str | None = None
    DiaChi: str | None = None
    MaKhoa: str | None = None


# ---- SinhVien ----
class SinhVienBase(BaseModel):
    """Base schema for SinhVien."""

    MaSV: str
    HoTen: str
    NgaySinh: date
    GioiTinh: str | None = None
    Email: EmailStr
    MaLop: str | None = None
    HeDaoTao: str = "ChinhQuy"
    QueQuan: str | None = None
    NoiSinh: str | None = None
    DanToc: str | None = None
    DiaChi: str | None = None
    SDT: str | None = None
    CCCD: str | None = None


class SinhVienCreate(SinhVienBase):
    """Schema for creating SinhVien."""

    MatKhau: str = Field(..., min_length=6)


class SinhVienUpdate(BaseModel):
    """Schema for updating SinhVien."""

    HoTen: str | None = None
    NgaySinh: date | None = None
    GioiTinh: str | None = None
    Email: EmailStr | None = None
    MaLop: str | None = None
    HeDaoTao: str | None = None
    QueQuan: str | None = None
    NoiSinh: str | None = None
    DanToc: str | None = None
    DiaChi: str | None = None
    SDT: str | None = None
    CCCD: str | None = None
    MatKhau: str | None = Field(default=None, min_length=6)


class SinhVienResponse(AuditSchema):
    """Response schema for SinhVien."""

    MaSV: str
    HoTen: str
    NgaySinh: date
    GioiTinh: str | None = None
    Email: str
    MaLop: str | None = None
    MaHSO: str | None = None
    MaTK: str | None = None
    HeDaoTao: str
    QueQuan: str | None = None
    NoiSinh: str | None = None
    DanToc: str | None = None
    DiaChi: str | None = None
    SDT: str | None = None
    CCCD: str | None = None
    BangTotNghiepURL: str | None = None
