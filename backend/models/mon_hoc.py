"""MonHoc model."""
from sqlalchemy import SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class MonHoc(BaseTable):
    """Bảng Môn Học."""

    __tablename__ = "MonHoc"

    MaMH: Mapped[str] = mapped_column(String(10), primary_key=True)
    TenMH: Mapped[str] = mapped_column(String(100), nullable=False)
    SoTinChi: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    MoTa: Mapped[str | None] = mapped_column(Text, default=None)

    # Relationships
    lop_hoc_phan: Mapped[list["LopHocPhan"]] = relationship("LopHocPhan", back_populates="mon_hoc")
    kq_hoc_tap: Mapped[list["KQHocTap"]] = relationship("KQHocTap", back_populates="mon_hoc")
    chuong_trinh_dao_tao: Mapped[list["ChuongTrinhDaoTao"]] = relationship("ChuongTrinhDaoTao", back_populates="mon_hoc")
    lich_thi: Mapped[list["LichThi"]] = relationship("LichThi", back_populates="mon_hoc")
    mon_tien_quyet: Mapped[list["MonHocTienQuyet"]] = relationship(
        "MonHocTienQuyet", foreign_keys="MonHocTienQuyet.MaMH", back_populates="mon_hoc"
    )
    mon_duoc_tien_quyet: Mapped[list["MonHocTienQuyet"]] = relationship(
        "MonHocTienQuyet", foreign_keys="MonHocTienQuyet.MaMHTienQuyet", back_populates="mon_hoc_duoc"
    )

    def __repr__(self) -> str:
        return f"<MonHoc(MaMH={self.MaMH}, TenMH={self.TenMH}, SoTinChi={self.SoTinChi})>"


from backend.models.lop_hoc_phan import LopHocPhan
from backend.models.kq_hoc_tap import KQHocTap
from backend.models.chuong_trinh_dao_tao import ChuongTrinhDaoTao
from backend.models.lich_thi import LichThi
from backend.models.mon_hoc_tien_quyet import MonHocTienQuyet
