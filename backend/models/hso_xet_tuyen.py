"""HSO_XetTuyen model - Hồ sơ ứng viên xét tuyển."""
from datetime import date
from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class HSOXetTuyen(BaseTable):
    """Bảng Hồ sơ Xét tuyển."""

    __tablename__ = "HSO_XetTuyen"

    MaHSO: Mapped[str] = mapped_column(String(10), primary_key=True)
    MaTK: Mapped[str | None] = mapped_column(String(10), ForeignKey("TK_XetTuyen.MaTK", ondelete="SET NULL"), default=None)
    HoTen: Mapped[str] = mapped_column(String(100), nullable=False)
    GioiTinh: Mapped[str | None] = mapped_column(String(10), default=None)
    NgaySinh: Mapped[date | None] = mapped_column(Date, default=None)
    CCCD: Mapped[str | None] = mapped_column(String(12), default=None, unique=True)
    SDT: Mapped[str | None] = mapped_column(String(11), default=None, unique=True)
    Email: Mapped[str | None] = mapped_column(String(100), default=None)
    DiaChi: Mapped[str | None] = mapped_column(String(255), default=None)
    QueQuan: Mapped[str | None] = mapped_column(String(100), default=None)
    NoiSinh: Mapped[str | None] = mapped_column(String(100), default=None)
    DanToc: Mapped[str | None] = mapped_column(String(50), default=None)
    TrinhDoNgoaiNgu: Mapped[str] = mapped_column(String(50), default="Không")
    BangTotNghiep: Mapped[str | None] = mapped_column(Text, default=None)
    FileCCCD: Mapped[str | None] = mapped_column(String(500), default=None)
    FileBangDiem: Mapped[str | None] = mapped_column(String(500), default=None)

    # Relationships
    tai_khoan: Mapped[TKXetTuyen | None] = relationship("TKXetTuyen", back_populates="hso")
    pt_xet_tuyen: Mapped[list["PTXetTuyen"]] = relationship("PTXetTuyen", back_populates="hso")
    sinh_vien: Mapped["SinhVien"] = relationship("SinhVien", back_populates="hso", uselist=False)

    def __repr__(self) -> str:
        return f"<HSOXetTuyen(MaHSO={self.MaHSO}, HoTen={self.HoTen})>"


from backend.models.tk_xet_tuyen import TKXetTuyen
from backend.models.pt_xet_tuyen import PTXetTuyen
from backend.models.sinh_vien import SinhVien
