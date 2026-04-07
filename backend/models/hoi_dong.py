"""HoiDongBaoVe models."""
from datetime import date
from sqlalchemy import BigInteger, Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class HoiDongBaoVe(BaseTable):
    """Bảng Hội đồng Bảo vệ."""

    __tablename__ = "HoiDongBaoVe"

    MaHD: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaLV: Mapped[str] = mapped_column(String(15), ForeignKey("LuanVan.MaLV", ondelete="CASCADE"), nullable=False, unique=True)
    TenHD: Mapped[str | None] = mapped_column(String(200), default=None)
    NgayThanhLap: Mapped[date | None] = mapped_column(Date, default=None)
    NgayBaoVe: Mapped[date | None] = mapped_column(Date, default=None)
    DiaDiem: Mapped[str | None] = mapped_column(String(200), default=None)
    TrangThai: Mapped[str] = mapped_column(String(20), default="ChuaThanhLap")
    GhiChu: Mapped[str | None] = mapped_column(String, default=None)

    # Relationships
    luan_van: Mapped["LuanVan"] = relationship("LuanVan", back_populates="hoi_dong")
    thanh_vien: Mapped[list["ThanhVienHoiDong"]] = relationship("ThanhVienHoiDong", back_populates="hoi_dong")

    def __repr__(self) -> str:
        return f"<HoiDongBaoVe(MaHD={self.MaHD}, MaLV={self.MaLV})>"


class ThanhVienHoiDong(BaseTable):
    """Bảng Thành viên Hội đồng."""

    __tablename__ = "ThanhVienHoiDong"
    __table_args__ = (
        UniqueConstraint("MaHD", "MaGV", name="uq_tvhd_hd_gv"),
    )

    MaTVHD: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaHD: Mapped[int] = mapped_column(BigInteger, ForeignKey("HoiDongBaoVe.MaHD", ondelete="CASCADE"), nullable=False)
    MaGV: Mapped[str] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="RESTRICT"), nullable=False)
    VaiTro: Mapped[str] = mapped_column(String(30), nullable=False)
    DiemDanhGia: Mapped[float | None] = mapped_column(DECIMAL(4, 2), default=None)
    NhanXet: Mapped[str | None] = mapped_column(String, default=None)

    # Relationships
    hoi_dong: Mapped["HoiDongBaoVe"] = relationship("HoiDongBaoVe", back_populates="thanh_vien")
    giang_vien: Mapped["GiangVien"] = relationship("GiangVien", back_populates="thanh_vien_hoi_dong")
    thu_lao: Mapped[list["ThuLaoHoiDong"]] = relationship("ThuLaoHoiDong", back_populates="thanh_vien")

    def __repr__(self) -> str:
        return f"<ThanhVienHoiDong(MaTVHD={self.MaTVHD}, VaiTro={self.VaiTro})>"


class ThuLaoHoiDong(BaseTable):
    """Bảng Thù lao Hội đồng."""

    __tablename__ = "ThuLaoHoiDong"
    __table_args__ = (
        UniqueConstraint("MaTVHD", "MaHD", name="uq_thulao_tvhd_hd"),
    )

    MaTL: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaTVHD: Mapped[int] = mapped_column(BigInteger, ForeignKey("ThanhVienHoiDong.MaTVHD", ondelete="CASCADE"), nullable=False)
    MaHD: Mapped[int] = mapped_column(BigInteger, ForeignKey("HoiDongBaoVe.MaHD", ondelete="CASCADE"), nullable=False)
    SoTien: Mapped[int] = mapped_column(DECIMAL(12, 0), nullable=False)
    TrangThai: Mapped[str] = mapped_column(String(20), default="ChuaChiTra")
    NgayChiTra: Mapped[date | None] = mapped_column(Date, default=None)
    MaGiaoDich: Mapped[str | None] = mapped_column(String(100), default=None)
    GhiChu: Mapped[str | None] = mapped_column(String, default=None)

    # Relationships
    thanh_vien: Mapped["ThanhVienHoiDong"] = relationship("ThanhVienHoiDong", back_populates="thu_lao")
    hoi_dong: Mapped["HoiDongBaoVe"] = relationship("HoiDongBaoVe")

    def __repr__(self) -> str:
        return f"<ThuLaoHoiDong(MaTL={self.MaTL}, SoTien={self.SoTien})>"


from backend.models.luan_van import LuanVan
from backend.models.giang_vien import GiangVien
