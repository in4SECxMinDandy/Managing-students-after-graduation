"""DeCuongLuanAn model - Đề cương luận án."""
from datetime import datetime, timezone
from sqlalchemy import BigInteger, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class DeCuongLuanAn(BaseTable):
    """Bảng Đề cương Luận án."""

    __tablename__ = "DeCuongLuanAn"

    MaDC: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaLV: Mapped[str] = mapped_column(String(15), ForeignKey("LuanVan.MaLV", ondelete="CASCADE"), nullable=False)
    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE"), nullable=False)
    PhienBan: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    TieuDe: Mapped[str] = mapped_column(String(255), nullable=False)
    TomTat: Mapped[str | None] = mapped_column(String, default=None)
    NoiDung: Mapped[str | None] = mapped_column(String, default=None)
    FileDeCuong: Mapped[str | None] = mapped_column(String(500), default=None)
    TrangThai: Mapped[str] = mapped_column(String(20), default="Nhap")
    NgayNop: Mapped[datetime] = mapped_column(String, default=lambda: datetime.now(timezone.utc))
    NgayDuyet: Mapped[datetime | None] = mapped_column(String, default=None)
    NguoiDuyet: Mapped[str | None] = mapped_column(String(10), ForeignKey("QuanTri.MaAdmin", ondelete="SET NULL"), default=None)
    BinhLuan: Mapped[str | None] = mapped_column(String, default=None)

    # Relationships
    luan_van: Mapped["LuanVan"] = relationship("LuanVan", back_populates="de_cuong")
    sinh_vien: Mapped["SinhVien"] = relationship("SinhVien", back_populates="de_cuong")
    nguoi_duyet: Mapped[QuanTri | None] = relationship("QuanTri", back_populates="de_cuong")

    def __repr__(self) -> str:
        return f"<DeCuongLuanAn(MaDC={self.MaDC}, MaLV={self.MaLV}, TrangThai={self.TrangThai})>"


from backend.models.luan_van import LuanVan
from backend.models.sinh_vien import SinhVien
from backend.models.quan_tri import QuanTri
