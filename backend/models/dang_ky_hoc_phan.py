"""DangKyHocPhan model - Đăng ký học phần."""
from datetime import datetime, timezone
from sqlalchemy import BigInteger, Boolean, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class DangKyHocPhan(BaseTable):
    """Bảng Đăng ký Học phần."""

    __tablename__ = "DangKyHocPhan"
    __table_args__ = (
        UniqueConstraint("MaSV", "MaLopHP", name="uq_dangky_sv_lophp"),
    )

    MaDK: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE"), nullable=False)
    MaLopHP: Mapped[int] = mapped_column(BigInteger, ForeignKey("LopHocPhan.MaLopHP", ondelete="CASCADE"), nullable=False)
    TrangThai: Mapped[str] = mapped_column(String(20), default="ChoDuyet")
    DuocMien: Mapped[bool] = mapped_column(Boolean, default=False)
    LyDoMien: Mapped[str | None] = mapped_column(String, default=None)
    NgayDK: Mapped[datetime] = mapped_column(
        String, default=lambda: datetime.now(timezone.utc)
    )
    NgayDuyet: Mapped[datetime | None] = mapped_column(String, default=None)
    NguoiDuyet: Mapped[str | None] = mapped_column(String(10), ForeignKey("QuanTri.MaAdmin", ondelete="SET NULL"), default=None)

    # Relationships
    sinh_vien: Mapped["SinhVien"] = relationship("SinhVien", back_populates="dang_ky")
    lop_hoc_phan: Mapped["LopHocPhan"] = relationship("LopHocPhan", back_populates="dang_ky")

    def __repr__(self) -> str:
        return f"<DangKyHocPhan(MaDK={self.MaDK}, MaSV={self.MaSV}, TrangThai={self.TrangThai})>"


from backend.models.sinh_vien import SinhVien
from backend.models.lop_hoc_phan import LopHocPhan
