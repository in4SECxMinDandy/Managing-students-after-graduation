"""GiangVien model."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.models.base import BaseTable


class GiangVien(BaseTable):
    """Bảng Giảng viên."""

    __tablename__ = "GiangVien"

    MaGV: Mapped[str] = mapped_column(String(15), primary_key=True)
    HoTen: Mapped[str] = mapped_column(String(100), nullable=False)
    Email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    SDT: Mapped[str | None] = mapped_column(String(11), default=None)
    HocVi: Mapped[str | None] = mapped_column(String(20), default=None)
    HocHam: Mapped[str | None] = mapped_column(String(20), default=None)
    ChuyenNganh: Mapped[str | None] = mapped_column(String(100), default=None)
    DiaChi: Mapped[str | None] = mapped_column(String(255), default=None)
    MaKhoa: Mapped[str | None] = mapped_column(String(5), ForeignKey("Khoa.MaKhoa", ondelete="SET NULL"), default=None)
    MatKhau: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    khoa: Mapped[Khoa | None] = relationship("Khoa", back_populates="giang_vien")
    lop_hoc_phan: Mapped[list["LopHocPhan"]] = relationship("LopHocPhan", back_populates="giang_vien")
    phan_cong: Mapped[list["PhanCongGiangDay"]] = relationship("PhanCongGiangDay", back_populates="giang_vien")
    luan_van_huong_dan: Mapped[list["LuanVan"]] = relationship("LuanVan", back_populates="giang_vien")
    thanh_vien_hoi_dong: Mapped[list["ThanhVienHoiDong"]] = relationship("ThanhVienHoiDong", back_populates="giang_vien")
    tac_gia: Mapped[list["TacGiaCongTrinh"]] = relationship("TacGiaCongTrinh", back_populates="giang_vien")
    tb_nguoi_nhan: Mapped[list["TB_NguoiNhan"]] = relationship("TB_NguoiNhan", back_populates="giang_vien")

    def __repr__(self) -> str:
        return f"<GiangVien(MaGV={self.MaGV}, HoTen={self.HoTen})>"


from backend.models.khoa import Khoa
from backend.models.lop_hoc_phan import LopHocPhan
from backend.models.phan_cong_giang_day import PhanCongGiangDay
from backend.models.luan_van import LuanVan
from backend.models.hoi_dong import ThanhVienHoiDong
from backend.models.nckh import TacGiaCongTrinh
from backend.models.thong_bao import TB_NguoiNhan
