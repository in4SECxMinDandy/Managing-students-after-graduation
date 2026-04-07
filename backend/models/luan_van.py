"""LuanVan model."""
from datetime import date
from sqlalchemy import DECIMAL, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class LuanVan(BaseTable):
    """Bảng Luận văn."""

    __tablename__ = "LuanVan"

    MaLV: Mapped[str] = mapped_column(String(15), primary_key=True)
    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE"), nullable=False, unique=True)
    MaGV: Mapped[str | None] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="SET NULL"), default=None)
    TenDeTai: Mapped[str] = mapped_column(String(255), nullable=False)
    NgayDangKy: Mapped[date | None] = mapped_column(Date, default=None)
    NgayBaoVe: Mapped[date | None] = mapped_column(Date, default=None)
    TrangThai: Mapped[str] = mapped_column(String(20), default="ChuaBaoVe")
    DiemBaoVe: Mapped[float | None] = mapped_column(DECIMAL(4, 2), default=None)
    DiemHe4: Mapped[float | None] = mapped_column(DECIMAL(3, 2), default=None)
    DiemChu: Mapped[str | None] = mapped_column(String(2), default=None)
    GhiChu: Mapped[str | None] = mapped_column(String, default=None)

    # Relationships
    sinh_vien: Mapped["SinhVien"] = relationship("SinhVien", back_populates="luan_van")
    giang_vien: Mapped[GiangVien | None] = relationship("GiangVien", back_populates="luan_van_huong_dan")
    de_cuong: Mapped[list["DeCuongLuanAn"]] = relationship("DeCuongLuanAn", back_populates="luan_van")
    hoi_dong: Mapped["HoiDongBaoVe"] = relationship("HoiDongBaoVe", back_populates="luan_van", uselist=False)

    def __repr__(self) -> str:
        return f"<LuanVan(MaLV={self.MaLV}, TenDeTai={self.TenDeTai})>"


from backend.models.sinh_vien import SinhVien
from backend.models.giang_vien import GiangVien
from backend.models.de_cuong import DeCuongLuanAn
from backend.models.hoi_dong import HoiDongBaoVe
