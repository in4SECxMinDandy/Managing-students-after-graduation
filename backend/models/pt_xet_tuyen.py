"""PT_XetTuyen model - Phiếu thông tin xét tuyển."""
from datetime import datetime, timezone
from sqlalchemy import DECIMAL, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class PTXetTuyen(BaseTable):
    """Bảng Phiếu Xét tuyển."""

    __tablename__ = "PT_XetTuyen"

    MaPTXT: Mapped[str] = mapped_column(String(15), primary_key=True)
    MaNganh: Mapped[str | None] = mapped_column(String(10), ForeignKey("Nganh.MaNganh", ondelete="SET NULL"), default=None)
    PhuongThuc: Mapped[str] = mapped_column(String(100), nullable=False)
    Diem: Mapped[float] = mapped_column(DECIMAL(4, 2), nullable=False)
    TrangThai: Mapped[str] = mapped_column(String(20), default="ChoDuyet")
    MaHSO: Mapped[str | None] = mapped_column(String(10), ForeignKey("HSO_XetTuyen.MaHSO", ondelete="CASCADE"), default=None)
    MaAdmin: Mapped[str | None] = mapped_column(String(10), ForeignKey("QuanTri.MaAdmin", ondelete="SET NULL"), default=None)
    NgayNop: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    NgayDuyet: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)
    GhiChu: Mapped[str | None] = mapped_column(Text, default=None)

    # Relationships
    nganh: Mapped[Nganh | None] = relationship("Nganh", back_populates="pt_xet_tuyen")
    hso: Mapped[HSOXetTuyen | None] = relationship("HSOXetTuyen", back_populates="pt_xet_tuyen")
    nguoi_duyet: Mapped[QuanTri | None] = relationship("QuanTri")

    def __repr__(self) -> str:
        return f"<PTXetTuyen(MaPTXT={self.MaPTXT}, TrangThai={self.TrangThai})>"


from backend.models.nganh import Nganh
from backend.models.hso_xet_tuyen import HSOXetTuyen
from backend.models.quan_tri import QuanTri
