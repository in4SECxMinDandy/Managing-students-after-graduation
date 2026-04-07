"""Khoa model."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class Khoa(BaseTable):
    """Bảng Khoa."""

    __tablename__ = "Khoa"

    MaKhoa: Mapped[str] = mapped_column(String(5), primary_key=True)
    TenKhoa: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    DiaChi: Mapped[str | None] = mapped_column(String(255), default=None)
    SDT: Mapped[str | None] = mapped_column(String(11), default=None)
    Email: Mapped[str | None] = mapped_column(String(100), default=None)

    # Relationships
    nganh: Mapped[list["Nganh"]] = relationship("Nganh", back_populates="khoa")
    giang_vien: Mapped[list["GiangVien"]] = relationship("GiangVien", back_populates="khoa")

    def __repr__(self) -> str:
        return f"<Khoa(MaKhoa={self.MaKhoa}, TenKhoa={self.TenKhoa})>"


# Forward refs
from backend.models.nganh import Nganh
from backend.models.giang_vien import GiangVien
