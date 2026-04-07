"""LichThi model."""
from datetime import time
from sqlalchemy import BigInteger, Date, ForeignKey, SmallInteger, String, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class LichThi(BaseTable):
    """Bảng Lịch thi."""

    __tablename__ = "LichThi"

    MaLT: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaMH: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE"), nullable=False)
    MaHK: Mapped[str] = mapped_column(String(10), ForeignKey("HocKy.MaHK", ondelete="CASCADE"), nullable=False)
    LoaiThi: Mapped[str] = mapped_column(String(20), default="CuoiKy")
    NgayThi: Mapped[date] = mapped_column(Date, nullable=False)
    GioThi: Mapped[time] = mapped_column(Time, nullable=False)
    ThoiLuong: Mapped[int | None] = mapped_column(SmallInteger, default=None)
    DiaDiem: Mapped[str | None] = mapped_column(String(200), default=None)
    HinhThuc: Mapped[str] = mapped_column(String(30), default="Viet")
    GhiChu: Mapped[str | None] = mapped_column(String, default=None)

    # Relationships
    mon_hoc: Mapped["MonHoc"] = relationship("MonHoc", back_populates="lich_thi")
    hoc_ky: Mapped["HocKy"] = relationship("HocKy", back_populates="lich_thi")

    def __repr__(self) -> str:
        return f"<LichThi(MaLT={self.MaLT}, MaMH={self.MaMH}, NgayThi={self.NgayThi})>"


from backend.models.mon_hoc import MonHoc
from backend.models.hoc_ky import HocKy
