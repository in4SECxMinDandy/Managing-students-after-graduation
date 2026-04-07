"""LopHocPhan model - Lớp học phần."""
from sqlalchemy import BigInteger, ForeignKey, SmallInteger, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class LopHocPhan(BaseTable):
    """Bảng Lớp học phần."""

    __tablename__ = "LopHocPhan"
    __table_args__ = (
        UniqueConstraint("MaMH", "MaHK", "TenNhom", name="uq_lophp_mh_hk_tennhom"),
    )

    MaLopHP: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaMH: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE"), nullable=False)
    MaHK: Mapped[str] = mapped_column(String(10), ForeignKey("HocKy.MaHK", ondelete="CASCADE"), nullable=False)
    MaGV: Mapped[str] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="RESTRICT"), nullable=False)
    TenNhom: Mapped[str | None] = mapped_column(String(50), default=None)
    SiSoToiDa: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=50)
    SiSoHienTai: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    MoTa: Mapped[str | None] = mapped_column(Text, default=None)

    # Relationships
    mon_hoc: Mapped["MonHoc"] = relationship("MonHoc", back_populates="lop_hoc_phan")
    hoc_ky: Mapped["HocKy"] = relationship("HocKy", back_populates="lop_hoc_phan")
    giang_vien: Mapped["GiangVien"] = relationship("GiangVien", back_populates="lop_hoc_phan")
    dang_ky: Mapped[list["DangKyHocPhan"]] = relationship("DangKyHocPhan", back_populates="lop_hoc_phan")
    phan_cong: Mapped[list["PhanCongGiangDay"]] = relationship("PhanCongGiangDay", back_populates="lop_hoc_phan")

    def __repr__(self) -> str:
        return f"<LopHocPhan(MaLopHP={self.MaLopHP}, MaMH={self.MaMH})>"


from backend.models.mon_hoc import MonHoc
from backend.models.hoc_ky import HocKy
from backend.models.giang_vien import GiangVien
from backend.models.dang_ky_hoc_phan import DangKyHocPhan
from backend.models.phan_cong_giang_day import PhanCongGiangDay
