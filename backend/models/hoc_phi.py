"""HocPhi models - Học phí và Đơn giá tín chỉ."""
from datetime import date
from sqlalchemy import BigInteger, DECIMAL, Date, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class DonGiaTinChi(BaseTable):
    """Bảng Đơn giá Tín chỉ."""

    __tablename__ = "DonGiaTinChi"

    MaDonGia: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    NamHoc: Mapped[str] = mapped_column(String(9), nullable=False)
    HeDaoTao: Mapped[str] = mapped_column(String(20), nullable=False)
    MaNganh: Mapped[str | None] = mapped_column(String(10), ForeignKey("Nganh.MaNganh", ondelete="CASCADE"), default=None)
    DonGia: Mapped[int] = mapped_column(DECIMAL(12, 0), nullable=False)

    # Relationships
    nganh: Mapped[Nganh | None] = relationship("Nganh", back_populates="don_gia_tin_chi")

    def __repr__(self) -> str:
        return f"<DonGiaTinChi(MaDonGia={self.MaDonGia}, NamHoc={self.NamHoc}, DonGia={self.DonGia})>"


class HocPhi(BaseTable):
    """Bảng Học phí."""

    __tablename__ = "HocPhi"
    __table_args__ = (
        UniqueConstraint("MaSV", "MaHK", name="uq_hocphi_sv_hk"),
    )

    MaHP: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE"), nullable=False)
    MaHK: Mapped[str] = mapped_column(String(10), ForeignKey("HocKy.MaHK", ondelete="RESTRICT"), nullable=False)
    SoTien: Mapped[int] = mapped_column(DECIMAL(15, 0), nullable=False)
    TrangThai: Mapped[str] = mapped_column(String(20), default="ChuaDong")
    NgayHanNop: Mapped[date | None] = mapped_column(Date, default=None)
    NgayDong: Mapped[date | None] = mapped_column(Date, default=None)
    MaGiaoDich: Mapped[str | None] = mapped_column(String(100), default=None)
    GhiChu: Mapped[str | None] = mapped_column(String, default=None)

    # Relationships
    sinh_vien: Mapped["SinhVien"] = relationship("SinhVien", back_populates="hoc_phi")
    hoc_ky: Mapped["HocKy"] = relationship("HocKy", back_populates="hoc_phi")

    def __repr__(self) -> str:
        return f"<HocPhi(MaHP={self.MaHP}, MaSV={self.MaSV}, SoTien={self.SoTien})>"


from backend.models.nganh import Nganh
from backend.models.sinh_vien import SinhVien
from backend.models.hoc_ky import HocKy
