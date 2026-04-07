"""Pydantic schemas cho Support module."""
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field
from backend.schemas.base import AuditSchema


# ---- ThongBao ----
class ThongBaoBase(BaseModel):
    TieuDe: str
    NoiDung: str
    LoaiTB: str = "Chung"
    MucDo: str = "BinhThuong"


class ThongBaoCreate(ThongBaoBase):
    pass


class ThongBaoUpdate(BaseModel):
    TieuDe: str | None = None
    NoiDung: str | None = None
    LoaiTB: str | None = None
    MucDo: str | None = None


class ThongBaoResponse(AuditSchema):
    MaTB: int
    TieuDe: str
    NoiDung: str
    LoaiTB: str | None = None
    MucDo: str | None = None
    MaAdmin: str | None = None


# ---- TB_NguoiNhan ----
class TB_NguoiNhanBase(BaseModel):
    MaTB: int
    MaSV: str | None = None
    MaGV: str | None = None


class TB_NguoiNhanCreate(TB_NguoiNhanBase):
    pass


class TB_NguoiNhanResponse(AuditSchema):
    MaTBNN: int
    MaTB: int
    MaSV: str | None = None
    MaGV: str | None = None
    TrangThaiDoc: bool
    ThoiGianDoc: datetime | None = None


# ---- NghienCuuKhoaHoc ----
class NghienCuuKhoaHocBase(BaseModel):
    TenCongTrinh: str
    LoaiCongTrinh: str
    MoTa: str | None = None
    Cap: str = "Truong"
    Nam: int = Field(..., ge=2000, le=2100)
    Link: str | None = None
    FileMinhChung: str | None = None


class NghienCuuKhoaHocCreate(NghienCuuKhoaHocBase):
    pass


class NghienCuuKhoaHocUpdate(BaseModel):
    TenCongTrinh: str | None = None
    LoaiCongTrinh: str | None = None
    MoTa: str | None = None
    Cap: str | None = None
    Nam: int | None = Field(default=None, ge=2000, le=2100)
    Link: str | None = None
    FileMinhChung: str | None = None


class NghienCuuKhoaHocResponse(AuditSchema):
    MaNCKH: int
    TenCongTrinh: str
    LoaiCongTrinh: str
    MoTa: str | None = None
    Cap: str | None = None
    Nam: int
    Link: str | None = None
    FileMinhChung: str | None = None


# ---- TacGiaCongTrinh ----
class TacGiaCongTrinhBase(BaseModel):
    MaNCKH: int
    MaGV: str | None = None
    MaSV: str | None = None
    VaiTro: str = "DongTacGia"
    ThuTu: int = 1


class TacGiaCongTrinhCreate(TacGiaCongTrinhBase):
    pass


class TacGiaCongTrinhResponse(AuditSchema):
    MaTacGia: int
    MaNCKH: int
    MaGV: str | None = None
    MaSV: str | None = None
    VaiTro: str
    ThuTu: int | None = None


# ---- QuyDinhDacThu ----
class QuyDinhDacThuBase(BaseModel):
    TenQD: str
    MoTa: str | None = None
    MaNganh: str | None = None
    KhoaTuyen: str | None = None
    LoaiQuyDinh: str
    GiaTri: float
    DonVi: str | None = None
    BatBuoc: bool = False


class QuyDinhDacThuCreate(QuyDinhDacThuBase):
    pass


class QuyDinhDacThuUpdate(BaseModel):
    TenQD: str | None = None
    MoTa: str | None = None
    MaNganh: str | None = None
    KhoaTuyen: str | None = None
    LoaiQuyDinh: str | None = None
    GiaTri: float | None = None
    DonVi: str | None = None
    BatBuoc: bool | None = None


class QuyDinhDacThuResponse(AuditSchema):
    MaQD: int
    TenQD: str
    MoTa: str | None = None
    MaNganh: str | None = None
    KhoaTuyen: str | None = None
    LoaiQuyDinh: str
    GiaTri: float
    DonVi: str | None = None
    BatBuoc: bool


# ---- TotNghiep ----
class TotNghiepBase(BaseModel):
    GPA: float = Field(..., ge=0, le=4.0)
    TongTinChi: int = Field(default=0, ge=0)
    XepLoai: str
    NgayTotNghiep: date | None = None
    SoHieuBang: str | None = None


class TotNghiepCreate(TotNghiepBase):
    pass


class TotNghiepResponse(AuditSchema):
    MaSV: str
    GPA: float
    TongTinChi: int
    XepLoai: str
    NgayTotNghiep: date | None = None
    SoHieuBang: str | None = None


# ---- LichThi ----
class LichThiBase(BaseModel):
    MaMH: str
    MaHK: str
    LoaiThi: str = "CuoiKy"
    NgayThi: date
    GioThi: str
    ThoiLuong: int | None = Field(default=None, ge=1, le=300)
    DiaDiem: str | None = None
    HinhThuc: str = "Viet"
    GhiChu: str | None = None


class LichThiCreate(LichThiBase):
    pass


class LichThiUpdate(BaseModel):
    LoaiThi: str | None = None
    NgayThi: date | None = None
    GioThi: str | None = None
    ThoiLuong: int | None = Field(default=None, ge=1, le=300)
    DiaDiem: str | None = None
    HinhThuc: str | None = None
    GhiChu: str | None = None


class LichThiResponse(AuditSchema):
    MaLT: int
    MaMH: str
    MaHK: str
    LoaiThi: str | None = None
    NgayThi: date
    GioThi: datetime | None = None
    ThoiLuong: int | None = None
    DiaDiem: str | None = None
    HinhThuc: str | None = None
    GhiChu: str | None = None
