"""PhanCongGiangDay model - Phân công giảng dạy."""
from sqlalchemy import BigInteger, ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class PhanCongGiangDay(BaseTable):
    """Bảng Phân công Giảng dạy."""

    __tablename__ = "PhanCongGiangDay"
    __table_args__ = (
        UniqueConstraint("MaLopHP", "MaGV", name="uq_phancong_lophp_gv"),
    )

    MaPC: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaLopHP: Mapped[int] = mapped_column(BigInteger, ForeignKey("LopHocPhan.MaLopHP", ondelete="CASCADE"), nullable=False)
    MaGV: Mapped[str] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="CASCADE"), nullable=False)
    VaiTro: Mapped[str] = mapped_column(String(30), default="GiangVienChinh")
    SoTiet: Mapped[int | None] = mapped_column(SmallInteger, default=None)

    # Relationships
    lop_hoc_phan: Mapped["LopHocPhan"] = relationship("LopHocPhan", back_populates="phan_cong")
    giang_vien: Mapped["GiangVien"] = relationship("GiangVien", back_populates="phan_cong")
    lich_hoc: Mapped[list["LichHoc"]] = relationship("LichHoc", back_populates="phan_cong")

    def __repr__(self) -> str:
        return f"<PhanCongGiangDay(MaPC={self.MaPC}, MaGV={self.MaGV}, VaiTro={self.VaiTro})>"


from backend.models.lop_hoc_phan import LopHocPhan
from backend.models.giang_vien import GiangVien
from backend.models.lich_hoc import LichHoc
