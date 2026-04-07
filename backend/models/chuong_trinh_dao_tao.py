"""ChuongTrinhDaoTao model."""
from sqlalchemy import BigInteger, ForeignKey, SmallInteger, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class ChuongTrinhDaoTao(BaseTable):
    """Bảng Chương trình Đào tạo."""

    __tablename__ = "ChuongTrinhDaoTao"
    __table_args__ = (
        UniqueConstraint("MaNganh", "MaMH", name="uq_ctdt_nganh_mh"),
    )

    MaCTDT: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaNganh: Mapped[str] = mapped_column(String(10), ForeignKey("Nganh.MaNganh", ondelete="CASCADE"), nullable=False)
    MaMH: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE"), nullable=False)
    HocKy: Mapped[int | None] = mapped_column(SmallInteger, default=None)
    LoaiMH: Mapped[str] = mapped_column(String(20), default="BatBuoc")

    # Relationships
    nganh: Mapped["Nganh"] = relationship("Nganh", back_populates="chuong_trinh_dao_tao")
    mon_hoc: Mapped["MonHoc"] = relationship("MonHoc", back_populates="chuong_trinh_dao_tao")

    def __repr__(self) -> str:
        return f"<ChuongTrinhDaoTao(MaCTDT={self.MaCTDT}, MaNganh={self.MaNganh})>"


from backend.models.nganh import Nganh
from backend.models.mon_hoc import MonHoc
