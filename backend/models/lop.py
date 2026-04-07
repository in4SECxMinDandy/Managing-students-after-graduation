"""Lop model."""
from sqlalchemy import ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class Lop(BaseTable):
    """Bảng Lớp."""

    __tablename__ = "Lop"

    MaLop: Mapped[str] = mapped_column(String(15), primary_key=True)
    TenLop: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    MaNganh: Mapped[str | None] = mapped_column(String(10), ForeignKey("Nganh.MaNganh", ondelete="SET NULL"), default=None)
    SiSo: Mapped[int | None] = mapped_column(SmallInteger, default=None)

    # Relationships
    nganh: Mapped[Nganh | None] = relationship("Nganh", back_populates="lop")
    sinh_vien: Mapped[list["SinhVien"]] = relationship("SinhVien", back_populates="lop")

    def __repr__(self) -> str:
        return f"<Lop(MaLop={self.MaLop}, TenLop={self.TenLop})>"


from backend.models.nganh import Nganh
from backend.models.sinh_vien import SinhVien
