"""TotNghiep model."""
from datetime import date
from sqlalchemy import DECIMAL, Date, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class TotNghiep(BaseTable):
    """Bảng Tốt nghiệp."""

    __tablename__ = "TotNghiep"

    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE"), primary_key=True)
    GPA: Mapped[float] = mapped_column(DECIMAL(4, 2), nullable=False)
    TongTinChi: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    XepLoai: Mapped[str] = mapped_column(String(20), nullable=False)
    NgayTotNghiep: Mapped[date | None] = mapped_column(Date, default=None)
    SoHieuBang: Mapped[str | None] = mapped_column(String(50), default=None, unique=True)

    # Relationships
    sinh_vien: Mapped["SinhVien"] = relationship("SinhVien", back_populates="tot_nghiep")

    def __repr__(self) -> str:
        return f"<TotNghiep(MaSV={self.MaSV}, GPA={self.GPA}, XepLoai={self.XepLoai})>"


from backend.models.sinh_vien import SinhVien
