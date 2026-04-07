"""LichHoc model - Lịch học."""
from sqlalchemy import BigInteger, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class LichHoc(BaseTable):
    """Bảng Lịch học."""

    __tablename__ = "LichHoc"

    MaLH: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaPC: Mapped[int] = mapped_column(BigInteger, ForeignKey("PhanCongGiangDay.MaPC", ondelete="CASCADE"), nullable=False)
    Thu: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    TietBatDau: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    SoTiet: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    Buoi: Mapped[str] = mapped_column(String(10), nullable=False)
    PhongHoc: Mapped[str | None] = mapped_column(String(50), default=None)

    # Relationships
    phan_cong: Mapped["PhanCongGiangDay"] = relationship("PhanCongGiangDay", back_populates="lich_hoc")

    def __repr__(self) -> str:
        return f"<LichHoc(MaLH={self.MaLH}, Thu={self.Thu}, Buoi={self.Buoi}, Tiết {self.TietBatDau})>"


from backend.models.phan_cong_giang_day import PhanCongGiangDay
