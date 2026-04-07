"""QuanTri model - Admin/Quản trị viên."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class QuanTri(BaseTable):
    """Bảng Quản trị viên."""

    __tablename__ = "QuanTri"

    MaAdmin: Mapped[str] = mapped_column(String(10), primary_key=True)
    TenDN: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    MatKhau: Mapped[str] = mapped_column(String(255), nullable=False)
    HoTen: Mapped[str] = mapped_column(String(100), nullable=False)
    Email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    SDT: Mapped[str | None] = mapped_column(String(11), default=None)
    VaiTro: Mapped[str] = mapped_column(String(20), default="admin")

    # Relationships
    thong_bao: Mapped[list["ThongBao"]] = relationship("ThongBao", back_populates="nguoi_tao")
    de_cuong: Mapped[list["DeCuongLuanAn"]] = relationship("DeCuongLuanAn", back_populates="nguoi_duyet")

    def __repr__(self) -> str:
        return f"<QuanTri(MaAdmin={self.MaAdmin}, HoTen={self.HoTen}, VaiTro={self.VaiTro})>"


from backend.models.thong_bao import ThongBao
from backend.models.de_cuong import DeCuongLuanAn
