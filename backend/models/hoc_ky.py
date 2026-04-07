"""HocKy model."""
from datetime import date
from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class HocKy(BaseTable):
    """Bảng Học Kỳ."""

    __tablename__ = "HocKy"

    MaHK: Mapped[str] = mapped_column(String(10), primary_key=True)
    TenHK: Mapped[str] = mapped_column(String(50), nullable=False)
    NamHoc: Mapped[str] = mapped_column(String(9), nullable=False)
    ThoiGianBD: Mapped[date] = mapped_column(Date, nullable=False)
    ThoiGianKT: Mapped[date] = mapped_column(Date, nullable=False)

    # Relationships
    lop_hoc_phan: Mapped[list["LopHocPhan"]] = relationship("LopHocPhan", back_populates="hoc_ky")
    kq_hoc_tap: Mapped[list["KQHocTap"]] = relationship("KQHocTap", back_populates="hoc_ky")
    hoc_phi: Mapped[list["HocPhi"]] = relationship("HocPhi", back_populates="hoc_ky")
    lich_thi: Mapped[list["LichThi"]] = relationship("LichThi", back_populates="hoc_ky")

    def __repr__(self) -> str:
        return f"<HocKy(MaHK={self.MaHK}, TenHK={self.TenHK}, NamHoc={self.NamHoc})>"


from backend.models.lop_hoc_phan import LopHocPhan
from backend.models.kq_hoc_tap import KQHocTap
from backend.models.hoc_phi import HocPhi
from backend.models.lich_thi import LichThi
