"""Nganh model."""
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class Nganh(BaseTable):
    """Bảng Ngành."""

    __tablename__ = "Nganh"

    MaNganh: Mapped[str] = mapped_column(String(10), primary_key=True)
    TenNganh: Mapped[str] = mapped_column(String(100), nullable=False)
    MaKhoa: Mapped[str | None] = mapped_column(String(5), ForeignKey("Khoa.MaKhoa", ondelete="SET NULL"), default=None)
    MoTa: Mapped[str | None] = mapped_column(Text, default=None)

    # Relationships
    khoa: Mapped[Khoa | None] = relationship("Khoa", back_populates="nganh")
    lop: Mapped[list["Lop"]] = relationship("Lop", back_populates="nganh")
    pt_xet_tuyen: Mapped[list["PTXetTuyen"]] = relationship("PTXetTuyen", back_populates="nganh")
    chuong_trinh_dao_tao: Mapped[list["ChuongTrinhDaoTao"]] = relationship("ChuongTrinhDaoTao", back_populates="nganh")
    don_gia_tin_chi: Mapped[list["DonGiaTinChi"]] = relationship("DonGiaTinChi", back_populates="nganh")
    quy_dinh_dac_thu: Mapped[list["QuyDinhDacThu"]] = relationship("QuyDinhDacThu", back_populates="nganh")

    def __repr__(self) -> str:
        return f"<Nganh(MaNganh={self.MaNganh}, TenNganh={self.TenNganh})>"


from backend.models.khoa import Khoa
from backend.models.lop import Lop
from backend.models.pt_xet_tuyen import PTXetTuyen
from backend.models.chuong_trinh_dao_tao import ChuongTrinhDaoTao
from backend.models.hoc_phi import DonGiaTinChi
from backend.models.quy_dinh import QuyDinhDacThu
