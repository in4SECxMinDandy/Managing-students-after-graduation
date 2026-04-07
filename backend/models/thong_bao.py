"""ThongBao models."""
from datetime import datetime, timezone
from sqlalchemy import BigInteger, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class ThongBao(BaseTable):
    """Bảng Thông báo."""

    __tablename__ = "ThongBao"

    MaTB: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    TieuDe: Mapped[str] = mapped_column(String(255), nullable=False)
    NoiDung: Mapped[str] = mapped_column(String, nullable=False)
    LoaiTB: Mapped[str] = mapped_column(String(30), default="Chung")
    MucDo: Mapped[str] = mapped_column(String(10), default="BinhThuong")
    MaAdmin: Mapped[str | None] = mapped_column(String(10), ForeignKey("QuanTri.MaAdmin", ondelete="SET NULL"), default=None)

    # Relationships
    nguoi_tao: Mapped[QuanTri | None] = relationship("QuanTri", back_populates="thong_bao")
    nguoi_nhan: Mapped[list["TB_NguoiNhan"]] = relationship("TB_NguoiNhan", back_populates="thong_bao")

    def __repr__(self) -> str:
        return f"<ThongBao(MaTB={self.MaTB}, TieuDe={self.TieuDe})>"


class TB_NguoiNhan(BaseTable):
    """Bảng Thông báo - Người nhận."""

    __tablename__ = "TB_NguoiNhan"

    MaTBNN: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaTB: Mapped[int] = mapped_column(BigInteger, ForeignKey("ThongBao.MaTB", ondelete="CASCADE"), nullable=False)
    MaSV: Mapped[str | None] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE"), default=None)
    MaGV: Mapped[str | None] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="CASCADE"), default=None)
    TrangThaiDoc: Mapped[bool] = mapped_column(Boolean, default=False)
    ThoiGianDoc: Mapped[datetime | None] = mapped_column(String, default=None)

    # Relationships
    thong_bao: Mapped["ThongBao"] = relationship("ThongBao", back_populates="nguoi_nhan")
    sinh_vien: Mapped[SinhVien | None] = relationship("SinhVien", back_populates="tb_nguoi_nhan")
    giang_vien: Mapped[GiangVien | None] = relationship("GiangVien", back_populates="tb_nguoi_nhan")

    def __repr__(self) -> str:
        return f"<TB_NguoiNhan(MaTBNN={self.MaTBNN}, MaTB={self.MaTB})>"


from backend.models.quan_tri import QuanTri
from backend.models.sinh_vien import SinhVien
from backend.models.giang_vien import GiangVien
