"""SinhVien model."""
from datetime import date
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class SinhVien(BaseTable):
    """Bảng Sinh viên."""

    __tablename__ = "SinhVien"

    MaSV: Mapped[str] = mapped_column(String(15), primary_key=True)
    HoTen: Mapped[str] = mapped_column(String(100), nullable=False)
    NgaySinh: Mapped[date] = mapped_column(Date, nullable=False)
    GioiTinh: Mapped[str | None] = mapped_column(String(10), default=None)
    Email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    MatKhau: Mapped[str] = mapped_column(String(255), nullable=False)
    MaLop: Mapped[str | None] = mapped_column(String(15), ForeignKey("Lop.MaLop", ondelete="SET NULL"), default=None)
    MaHSO: Mapped[str | None] = mapped_column(String(10), ForeignKey("HSO_XetTuyen.MaHSO", ondelete="SET NULL"), default=None)
    MaTK: Mapped[str | None] = mapped_column(String(10), ForeignKey("TK_XetTuyen.MaTK", ondelete="SET NULL"), default=None)
    HeDaoTao: Mapped[str] = mapped_column(String(20), default="ChinhQuy")
    QueQuan: Mapped[str | None] = mapped_column(String(100), default=None)
    NoiSinh: Mapped[str | None] = mapped_column(String(100), default=None)
    DanToc: Mapped[str | None] = mapped_column(String(50), default=None)
    DiaChi: Mapped[str | None] = mapped_column(String(255), default=None)
    SDT: Mapped[str | None] = mapped_column(String(11), default=None)
    CCCD: Mapped[str | None] = mapped_column(String(12), default=None, unique=True)
    BangTotNghiepURL: Mapped[str | None] = mapped_column(String(500), default=None)

    # Relationships
    lop: Mapped[Lop | None] = relationship("Lop", back_populates="sinh_vien")
    hso: Mapped[HSOXetTuyen | None] = relationship("HSOXetTuyen", back_populates="sinh_vien")
    dang_ky: Mapped[list["DangKyHocPhan"]] = relationship("DangKyHocPhan", back_populates="sinh_vien")
    kq_hoc_tap: Mapped[list["KQHocTap"]] = relationship("KQHocTap", back_populates="sinh_vien")
    luan_van: Mapped["LuanVan"] = relationship("LuanVan", back_populates="sinh_vien", uselist=False)
    de_cuong: Mapped[list["DeCuongLuanAn"]] = relationship("DeCuongLuanAn", back_populates="sinh_vien")
    hoc_phi: Mapped[list["HocPhi"]] = relationship("HocPhi", back_populates="sinh_vien")
    tot_nghiep: Mapped["TotNghiep"] = relationship("TotNghiep", back_populates="sinh_vien", uselist=False)
    tb_nguoi_nhan: Mapped[list["TB_NguoiNhan"]] = relationship("TB_NguoiNhan", back_populates="sinh_vien")
    tac_gia: Mapped[list["TacGiaCongTrinh"]] = relationship("TacGiaCongTrinh", back_populates="sinh_vien")

    def __repr__(self) -> str:
        return f"<SinhVien(MaSV={self.MaSV}, HoTen={self.HoTen})>"


from backend.models.lop import Lop
from backend.models.hso_xet_tuyen import HSOXetTuyen
from backend.models.dang_ky_hoc_phan import DangKyHocPhan
from backend.models.kq_hoc_tap import KQHocTap
from backend.models.luan_van import LuanVan
from backend.models.de_cuong import DeCuongLuanAn
from backend.models.hoc_phi import HocPhi
from backend.models.tot_nghiep import TotNghiep
from backend.models.thong_bao import TB_NguoiNhan
from backend.models.nckh import TacGiaCongTrinh
