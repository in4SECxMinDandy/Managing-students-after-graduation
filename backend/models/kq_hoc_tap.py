"""KQ_HocTap model - Kết quả học tập."""
from sqlalchemy import DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class KQHocTap(BaseTable):
    """Bảng Kết quả Học tập."""

    __tablename__ = "KQ_HocTap"

    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE"), primary_key=True)
    MaMH: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE"), primary_key=True)
    MaHK: Mapped[str] = mapped_column(String(10), ForeignKey("HocKy.MaHK", ondelete="RESTRICT"), primary_key=True)
    Diem: Mapped[float] = mapped_column(DECIMAL(4, 2), nullable=False)
    LoaiDiem: Mapped[str] = mapped_column(String(20), default="Thi")
    DiemHe4: Mapped[float | None] = mapped_column(DECIMAL(3, 2), default=None)
    DiemChu: Mapped[str | None] = mapped_column(String(2), default=None)
    GhiChu: Mapped[str | None] = mapped_column(String, default=None)

    # Relationships
    sinh_vien: Mapped["SinhVien"] = relationship("SinhVien", back_populates="kq_hoc_tap")
    mon_hoc: Mapped["MonHoc"] = relationship("MonHoc", back_populates="kq_hoc_tap")
    hoc_ky: Mapped["HocKy"] = relationship("HocKy", back_populates="kq_hoc_tap")

    def __repr__(self) -> str:
        return f"<KQHocTap(MaSV={self.MaSV}, MaMH={self.MaMH}, Diem={self.Diem})>"


from backend.models.sinh_vien import SinhVien
from backend.models.mon_hoc import MonHoc
from backend.models.hoc_ky import HocKy
