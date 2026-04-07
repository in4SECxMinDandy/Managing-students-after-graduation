"""NCKH models."""
from sqlalchemy import BigInteger, ForeignKey, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class NghienCuuKhoaHoc(BaseTable):
    """Bảng Nghiên cứu Khoa học."""

    __tablename__ = "NghienCuuKhoaHoc"

    MaNCKH: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    TenCongTrinh: Mapped[str] = mapped_column(String(255), nullable=False)
    LoaiCongTrinh: Mapped[str] = mapped_column(String(20), nullable=False)
    MoTa: Mapped[str | None] = mapped_column(String, default=None)
    Cap: Mapped[str] = mapped_column(String(20), default="Truong")
    Nam: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    Link: Mapped[str | None] = mapped_column(String(500), default=None)
    FileMinhChung: Mapped[str | None] = mapped_column(String(500), default=None)

    # Relationships
    tac_gia: Mapped[list["TacGiaCongTrinh"]] = relationship("TacGiaCongTrinh", back_populates="cong_trinh")

    def __repr__(self) -> str:
        return f"<NghienCuuKhoaHoc(MaNCKH={self.MaNCKH}, TenCongTrinh={self.TenCongTrinh})>"


class TacGiaCongTrinh(BaseTable):
    """Bảng Tác giả Công trình."""

    __tablename__ = "TacGiaCongTrinh"

    MaTacGia: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaNCKH: Mapped[int] = mapped_column(BigInteger, ForeignKey("NghienCuuKhoaHoc.MaNCKH", ondelete="CASCADE"), nullable=False)
    MaGV: Mapped[str | None] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="CASCADE"), default=None)
    MaSV: Mapped[str | None] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE"), default=None)
    VaiTro: Mapped[str] = mapped_column(String(30), nullable=False, default="DongTacGia")
    ThuTu: Mapped[int] = mapped_column(SmallInteger, default=1)

    # Relationships
    cong_trinh: Mapped["NghienCuuKhoaHoc"] = relationship("NghienCuuKhoaHoc", back_populates="tac_gia")
    giang_vien: Mapped[GiangVien | None] = relationship("GiangVien", back_populates="tac_gia")
    sinh_vien: Mapped[SinhVien | None] = relationship("SinhVien", back_populates="tac_gia")

    def __repr__(self) -> str:
        return f"<TacGiaCongTrinh(MaTacGia={self.MaTacGia}, VaiTro={self.VaiTro})>"


from backend.models.giang_vien import GiangVien
from backend.models.sinh_vien import SinhVien
