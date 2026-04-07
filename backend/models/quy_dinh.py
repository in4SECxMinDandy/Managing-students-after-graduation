"""QuyDinhDacThu model."""
from sqlalchemy import BigInteger, Boolean, DECIMAL, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class QuyDinhDacThu(BaseTable):
    """Bảng Quy định Đặc thù."""

    __tablename__ = "QuyDinhDacThu"

    MaQD: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    TenQD: Mapped[str] = mapped_column(String(200), nullable=False)
    MoTa: Mapped[str | None] = mapped_column(String, default=None)
    MaNganh: Mapped[str | None] = mapped_column(String(10), ForeignKey("Nganh.MaNganh", ondelete="SET NULL"), default=None)
    KhoaTuyen: Mapped[str | None] = mapped_column(String(9), default=None)
    LoaiQuyDinh: Mapped[str] = mapped_column(String(30), nullable=False)
    GiaTri: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    DonVi: Mapped[str | None] = mapped_column(String(30), default=None)
    BatBuoc: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    nganh: Mapped[Nganh | None] = relationship("Nganh", back_populates="quy_dinh_dac_thu")

    def __repr__(self) -> str:
        return f"<QuyDinhDacThu(MaQD={self.MaQD}, TenQD={self.TenQD})>"


from backend.models.nganh import Nganh
