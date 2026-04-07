"""Pydantic schemas cho Admissions module."""
from datetime import date, datetime
from pydantic import BaseModel, EmailStr, Field
from backend.schemas.base import AuditSchema


# ---- TK_XetTuyen ----
class TK_XetTuyenBase(BaseModel):
    Email: EmailStr


class TK_XetTuyenCreate(TK_XetTuyenBase):
    MatKhau: str = Field(..., min_length=6)


class TK_XetTuyenResponse(AuditSchema):
    MaTK: str
    Email: str


# ---- HSO_XetTuyen ----
class HSO_XetTuyenBase(BaseModel):
    MaTK: str | None = None
    HoTen: str
    GioiTinh: str | None = None
    NgaySinh: date | None = None
    CCCD: str | None = None
    SDT: str = Field(..., min_length=10, max_length=11)
    Email: EmailStr | None = None
    DiaChi: str | None = None
    QueQuan: str | None = None
    NoiSinh: str | None = None
    DanToc: str | None = None
    TrinhDoNgoaiNgu: str | None = None
    BangTotNghiep: str | None = None
    FileCCCD: str | None = None
    FileBangDiem: str | None = None


class HSO_XetTuyenCreate(HSO_XetTuyenBase):
    pass


class HSO_XetTuyenUpdate(BaseModel):
    HoTen: str | None = None
    GioiTinh: str | None = None
    NgaySinh: date | None = None
    CCCD: str | None = None
    SDT: str | None = None
    Email: EmailStr | None = None
    DiaChi: str | None = None
    QueQuan: str | None = None
    NoiSinh: str | None = None
    DanToc: str | None = None
    TrinhDoNgoaiNgu: str | None = None
    BangTotNghiep: str | None = None
    FileCCCD: str | None = None
    FileBangDiem: str | None = None


class HSO_XetTuyenResponse(AuditSchema):
    MaHSO: str
    MaTK: str | None = None
    HoTen: str
    GioiTinh: str | None = None
    NgaySinh: date | None = None
    CCCD: str | None = None
    SDT: str
    Email: str | None = None
    DiaChi: str | None = None
    QueQuan: str | None = None
    NoiSinh: str | None = None
    DanToc: str | None = None
    TrinhDoNgoaiNgu: str | None = None
    BangTotNghiep: str | None = None
    FileCCCD: str | None = None
    FileBangDiem: str | None = None


# ---- PT_XetTuyen ----
class PT_XetTuyenBase(BaseModel):
    MaNganh: str | None = None
    PhuongThuc: str
    Diem: float = Field(..., ge=0, le=10)
    TrangThai: str = "ChoDuyet"
    MaHSO: str | None = None
    GhiChu: str | None = None


class PT_XetTuyenCreate(PT_XetTuyenBase):
    pass


class PT_XetTuyenUpdate(BaseModel):
    PhuongThuc: str | None = None
    Diem: float | None = Field(default=None, ge=0, le=10)
    TrangThai: str | None = None
    GhiChu: str | None = None


class PT_XetTuyenResponse(AuditSchema):
    MaPTXT: int
    MaNganh: str | None = None
    PhuongThuc: str
    Diem: float
    TrangThai: str
    MaHSO: str | None = None
    MaAdmin: str | None = None
    NgayNop: datetime | None = None
    NgayDuyet: datetime | None = None
    GhiChu: str | None = None
