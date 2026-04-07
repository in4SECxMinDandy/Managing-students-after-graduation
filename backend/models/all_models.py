"""SQLAlchemy models for all 29 tables."""
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    Time,
    UniqueConstraint,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database.base_model import TimestampSoftDeleteMixin


# =============================================================================
# 1. Khoa
# =============================================================================
class Khoa(TimestampSoftDeleteMixin):
    """Khoa model."""

    __tablename__ = "Khoa"

    MaKhoa: Mapped[str] = mapped_column(String(5), primary_key=True)
    TenKhoa: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    DiaChi: Mapped[str | None] = mapped_column(String(255), nullable=True)
    SDT: Mapped[str | None] = mapped_column(String(11), nullable=True)
    Email: Mapped[str | None] = mapped_column(String(100), nullable=True)

    # Relationships
    nganh: Mapped[list["Nganh"]] = relationship("Nganh", back_populates="khoa")
    giang_vien: Mapped[list["GiangVien"]] = relationship("GiangVien", back_populates="khoa")


# =============================================================================
# 2. Nganh
# =============================================================================
class Nganh(TimestampSoftDeleteMixin):
    """Nganh model."""

    __tablename__ = "Nganh"

    MaNganh: Mapped[str] = mapped_column(String(10), primary_key=True)
    TenNganh: Mapped[str] = mapped_column(String(100), nullable=False)
    MaKhoa: Mapped[str | None] = mapped_column(String(5), ForeignKey("Khoa.MaKhoa", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    MoTa: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    khoa: Mapped[Khoa | None] = relationship("Khoa", back_populates="nganh")
    lop: Mapped[list["Lop"]] = relationship("Lop", back_populates="nganh")
    chuong_trinh_dao_tao: Mapped[list["ChuongTrinhDaoTao"]] = relationship("ChuongTrinhDaoTao", back_populates="nganh")
    don_gia: Mapped[list["DonGiaTinChi"]] = relationship("DonGiaTinChi", back_populates="nganh")


# =============================================================================
# 3. Lop
# =============================================================================
class Lop(TimestampSoftDeleteMixin):
    """Lop model."""

    __tablename__ = "Lop"

    MaLop: Mapped[str] = mapped_column(String(15), primary_key=True)
    TenLop: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    MaNganh: Mapped[str | None] = mapped_column(String(10), ForeignKey("Nganh.MaNganh", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    SiSo: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)

    # Relationships
    nganh: Mapped[Nganh | None] = relationship("Nganh", back_populates="lop")
    sinh_vien: Mapped[list["SinhVien"]] = relationship("SinhVien", back_populates="lop")


# =============================================================================
# 4. MonHoc
# =============================================================================
class MonHoc(TimestampSoftDeleteMixin):
    """MonHoc model."""

    __tablename__ = "MonHoc"

    MaMH: Mapped[str] = mapped_column(String(10), primary_key=True)
    TenMH: Mapped[str] = mapped_column(String(100), nullable=False)
    SoTinChi: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    MoTa: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("SoTinChi BETWEEN 1 AND 10", name="chk_monhoc_sotc"),
    )

    # Relationships
    mon_tien_quyet: Mapped[list["MonHocTienQuyet"]] = relationship(
        "MonHocTienQuyet",
        foreign_keys=lambda: [MonHocTienQuyet.MaMH],
        back_populates="mon_hoc",
    )
    mon_duoc_tien_quyet: Mapped[list["MonHocTienQuyet"]] = relationship(
        "MonHocTienQuyet",
        foreign_keys=lambda: [MonHocTienQuyet.MaMHTienQuyet],
        back_populates="mon_tien_quyet",
    )
    chuong_trinh: Mapped[list["ChuongTrinhDaoTao"]] = relationship("ChuongTrinhDaoTao", back_populates="mon_hoc")
    lop_hoc_phan: Mapped[list["LopHocPhan"]] = relationship("LopHocPhan", back_populates="mon_hoc")
    kq_hoctap: Mapped[list["KQ_HocTap"]] = relationship("KQ_HocTap", back_populates="mon_hoc")


# =============================================================================
# 5. HocKy
# =============================================================================
class HocKy(TimestampSoftDeleteMixin):
    """HocKy model."""

    __tablename__ = "HocKy"

    MaHK: Mapped[str] = mapped_column(String(10), primary_key=True)
    TenHK: Mapped[str] = mapped_column(String(50), nullable=False)
    NamHoc: Mapped[str] = mapped_column(String(9), nullable=False)
    ThoiGianBD: Mapped[date] = mapped_column(Date, nullable=False)
    ThoiGianKT: Mapped[date] = mapped_column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint("ThoiGianKT > ThoiGianBD", name="chk_hocky_tg"),
    )

    # Relationships
    lop_hoc_phan: Mapped[list["LopHocPhan"]] = relationship("LopHocPhan", back_populates="hoc_ky")
    hoc_phi: Mapped[list["HocPhi"]] = relationship("HocPhi", back_populates="hoc_ky")
    lich_thi: Mapped[list["LichThi"]] = relationship("LichThi", back_populates="hoc_ky")


# =============================================================================
# 6. QuanTri
# =============================================================================
class QuanTri(TimestampSoftDeleteMixin):
    """QuanTri model.

    PostgreSQL folds unquoted DDL identifiers to lowercase; schema_postgresql.sql creates
    table ``quantri`` with columns ``maadmin``, ``tendn``, etc. Map explicitly so ORM matches.
    """

    __tablename__ = "quantri"

    MaAdmin: Mapped[str] = mapped_column("maadmin", String(10), primary_key=True)
    TenDN: Mapped[str] = mapped_column("tendn", String(50), nullable=False, unique=True)
    MatKhau: Mapped[str] = mapped_column("matkhau", String(255), nullable=False)
    HoTen: Mapped[str] = mapped_column("hoten", String(100), nullable=False)
    Email: Mapped[str] = mapped_column("email", String(100), nullable=False, unique=True)
    SDT: Mapped[str | None] = mapped_column("sdt", String(11), nullable=True)
    VaiTro: Mapped[str] = mapped_column("vaitro", String(20), nullable=False, default="admin")

    # Relationships
    pt_xet_tuyen: Mapped[list["PT_XetTuyen"]] = relationship("PT_XetTuyen", back_populates="nguoi_duyet")
    thong_bao: Mapped[list["ThongBao"]] = relationship("ThongBao", back_populates="nguoi_tao")


# =============================================================================
# 7. TK_XetTuyen
# =============================================================================
class TK_XetTuyen(TimestampSoftDeleteMixin):
    """TK_XetTuyen model (tài khoản xét tuyển)."""

    __tablename__ = "TK_XetTuyen"

    MaTK: Mapped[str] = mapped_column(String(10), primary_key=True)
    Email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    MatKhau: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    hso: Mapped["HSO_XetTuyen | None"] = relationship("HSO_XetTuyen", back_populates="tai_khoan")
    sinh_vien: Mapped["SinhVien | None"] = relationship("SinhVien", back_populates="tai_khoan")


# =============================================================================
# 8. HSO_XetTuyen
# =============================================================================
class HSO_XetTuyen(TimestampSoftDeleteMixin):
    """HSO_XetTuyen model (hồ sơ ứng tuyển)."""

    __tablename__ = "HSO_XetTuyen"

    MaHSO: Mapped[str] = mapped_column(String(10), primary_key=True)
    MaTK: Mapped[str | None] = mapped_column(String(10), ForeignKey("TK_XetTuyen.MaTK", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    HoTen: Mapped[str] = mapped_column(String(100), nullable=False)
    GioiTinh: Mapped[str | None] = mapped_column(String(10), nullable=True)
    NgaySinh: Mapped[date | None] = mapped_column(Date, nullable=True)
    CCCD: Mapped[str | None] = mapped_column(String(12), nullable=True)
    SDT: Mapped[str] = mapped_column(String(11), nullable=False)
    Email: Mapped[str | None] = mapped_column(String(100), nullable=True)
    DiaChi: Mapped[str | None] = mapped_column(String(255), nullable=True)
    QueQuan: Mapped[str | None] = mapped_column(String(100), nullable=True)
    NoiSinh: Mapped[str | None] = mapped_column(String(100), nullable=True)
    DanToc: Mapped[str | None] = mapped_column(String(50), nullable=True)
    TrinhDoNgoaiNgu: Mapped[str | None] = mapped_column(String(50), nullable=True, default="Không")
    BangTotNghiep: Mapped[str | None] = mapped_column(Text, nullable=True)
    FileCCCD: Mapped[str | None] = mapped_column(String(500), nullable=True)
    FileBangDiem: Mapped[str | None] = mapped_column(String(500), nullable=True)

    __table_args__ = (
        UniqueConstraint("CCCD", name="uq_hso_cccd"),
        UniqueConstraint("SDT", name="uq_hso_sdt"),
    )

    # Relationships
    tai_khoan: Mapped[TK_XetTuyen | None] = relationship("TK_XetTuyen", back_populates="hso")
    pt_xet_tuyen: Mapped[list["PT_XetTuyen"]] = relationship("PT_XetTuyen", back_populates="hso")
    sinh_vien: Mapped["SinhVien | None"] = relationship("SinhVien", back_populates="hso")


# =============================================================================
# 9. PT_XetTuyen
# =============================================================================
class PT_XetTuyen(TimestampSoftDeleteMixin):
    """PT_XetTuyen model (phương thức xét tuyển)."""

    __tablename__ = "PT_XetTuyen"

    MaPTXT: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaNganh: Mapped[str | None] = mapped_column(String(10), ForeignKey("Nganh.MaNganh", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    PhuongThuc: Mapped[str] = mapped_column(String(100), nullable=False)
    Diem: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    TrangThai: Mapped[str] = mapped_column(String(20), nullable=False, default="ChoDuyet")
    MaHSO: Mapped[str | None] = mapped_column(String(10), ForeignKey("HSO_XetTuyen.MaHSO", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    MaAdmin: Mapped[str | None] = mapped_column(String(10), ForeignKey("quantri.maadmin", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    NgayNop: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    NgayDuyet: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    GhiChu: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("Diem >= 0 AND Diem <= 10", name="chk_ptxt_diem"),
    )

    # Relationships
    nganh: Mapped[Nganh | None] = relationship("Nganh")
    hso: Mapped[HSO_XetTuyen | None] = relationship("HSO_XetTuyen", back_populates="pt_xet_tuyen")
    nguoi_duyet: Mapped[QuanTri | None] = relationship("QuanTri", back_populates="pt_xet_tuyen")


# =============================================================================
# 10. SinhVien
# =============================================================================
class SinhVien(TimestampSoftDeleteMixin):
    """SinhVien model."""

    __tablename__ = "SinhVien"

    MaSV: Mapped[str] = mapped_column(String(15), primary_key=True)
    HoTen: Mapped[str] = mapped_column(String(100), nullable=False)
    NgaySinh: Mapped[date] = mapped_column(Date, nullable=False)
    GioiTinh: Mapped[str | None] = mapped_column(String(10), nullable=True)
    Email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    MatKhau: Mapped[str] = mapped_column(String(255), nullable=False)
    MaLop: Mapped[str | None] = mapped_column(String(15), ForeignKey("Lop.MaLop", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    MaHSO: Mapped[str | None] = mapped_column(String(10), ForeignKey("HSO_XetTuyen.MaHSO", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    MaTK: Mapped[str | None] = mapped_column(String(10), ForeignKey("TK_XetTuyen.MaTK", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    HeDaoTao: Mapped[str] = mapped_column(String(20), nullable=False, default="ChinhQuy")
    QueQuan: Mapped[str | None] = mapped_column(String(100), nullable=True)
    NoiSinh: Mapped[str | None] = mapped_column(String(100), nullable=True)
    DanToc: Mapped[str | None] = mapped_column(String(50), nullable=True)
    DiaChi: Mapped[str | None] = mapped_column(String(255), nullable=True)
    SDT: Mapped[str | None] = mapped_column(String(11), nullable=True)
    CCCD: Mapped[str | None] = mapped_column(String(12), nullable=True)
    BangTotNghiepURL: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Relationships
    lop: Mapped[Lop | None] = relationship("Lop", back_populates="sinh_vien")
    hso: Mapped[HSO_XetTuyen | None] = relationship("HSO_XetTuyen", back_populates="sinh_vien")
    tai_khoan: Mapped[TK_XetTuyen | None] = relationship("TK_XetTuyen", back_populates="sinh_vien")
    tac_gia: Mapped[list["TacGiaCongTrinh"]] = relationship("TacGiaCongTrinh", back_populates="sinh_vien")
    kq_hoctap: Mapped[list["KQ_HocTap"]] = relationship("KQ_HocTap", back_populates="sinh_vien")
    dang_ky: Mapped[list["DangKyHocPhan"]] = relationship("DangKyHocPhan", back_populates="sinh_vien")
    hoc_phi: Mapped[list["HocPhi"]] = relationship("HocPhi", back_populates="sinh_vien")
    luan_van: Mapped["LuanVan | None"] = relationship("LuanVan", back_populates="sinh_vien", uselist=False)
    de_cuong: Mapped[list["DeCuongLuanAn"]] = relationship("DeCuongLuanAn", back_populates="sinh_vien")
    tot_nghiep: Mapped["TotNghiep | None"] = relationship("TotNghiep", back_populates="sinh_vien", uselist=False)
    thong_bao: Mapped[list["TB_NguoiNhan"]] = relationship("TB_NguoiNhan", back_populates="sinh_vien")


# =============================================================================
# 11. GiangVien
# =============================================================================
class GiangVien(TimestampSoftDeleteMixin):
    """GiangVien model."""

    __tablename__ = "GiangVien"

    MaGV: Mapped[str] = mapped_column(String(15), primary_key=True)
    HoTen: Mapped[str] = mapped_column(String(100), nullable=False)
    Email: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    SDT: Mapped[str | None] = mapped_column(String(11), nullable=True)
    HocVi: Mapped[str | None] = mapped_column(String(20), nullable=True)
    HocHam: Mapped[str | None] = mapped_column(String(20), nullable=True)
    ChuyenNganh: Mapped[str | None] = mapped_column(String(100), nullable=True)
    DiaChi: Mapped[str | None] = mapped_column(String(255), nullable=True)
    MaKhoa: Mapped[str | None] = mapped_column(String(5), ForeignKey("Khoa.MaKhoa", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    MatKhau: Mapped[str] = mapped_column(String(255), nullable=False)

    # Relationships
    khoa: Mapped[Khoa | None] = relationship("Khoa", back_populates="giang_vien")
    luan_van: Mapped[list["LuanVan"]] = relationship("LuanVan", back_populates="giang_vien")
    lop_hoc_phan: Mapped[list["LopHocPhan"]] = relationship("LopHocPhan", back_populates="giang_vien")
    phan_cong: Mapped[list["PhanCongGiangDay"]] = relationship("PhanCongGiangDay", back_populates="giang_vien")
    thanh_vien_hd: Mapped[list["ThanhVienHoiDong"]] = relationship("ThanhVienHoiDong", back_populates="giang_vien")
    tac_gia: Mapped[list["TacGiaCongTrinh"]] = relationship("TacGiaCongTrinh", back_populates="giang_vien")
    thong_bao: Mapped[list["TB_NguoiNhan"]] = relationship("TB_NguoiNhan", back_populates="giang_vien")


# =============================================================================
# 12. LopHocPhan
# =============================================================================
class LopHocPhan(TimestampSoftDeleteMixin):
    """LopHocPhan model."""

    __tablename__ = "LopHocPhan"

    MaLopHP: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaMH: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    MaHK: Mapped[str] = mapped_column(String(10), ForeignKey("HocKy.MaHK", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    MaGV: Mapped[str] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    TenNhom: Mapped[str | None] = mapped_column(String(50), nullable=True)
    SiSoToiDa: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=50)
    SiSoHienTai: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    MoTa: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("MaMH", "MaHK", "TenNhom", name="uq_lophp_mamh_mahk_tennhom"),
        CheckConstraint("SiSoToiDa > 0", name="chk_lophp_sisomax"),
        CheckConstraint("SiSoHienTai >= 0", name="chk_lophp_sisohientai"),
    )

    # Relationships
    mon_hoc: Mapped[MonHoc] = relationship("MonHoc", back_populates="lop_hoc_phan")
    hoc_ky: Mapped[HocKy] = relationship("HocKy", back_populates="lop_hoc_phan")
    giang_vien: Mapped[GiangVien] = relationship("GiangVien", back_populates="lop_hoc_phan")
    dang_ky: Mapped[list["DangKyHocPhan"]] = relationship("DangKyHocPhan", back_populates="lop_hoc_phan")
    phan_cong: Mapped[list["PhanCongGiangDay"]] = relationship("PhanCongGiangDay", back_populates="lop_hoc_phan")


# =============================================================================
# 13. DangKyHocPhan
# =============================================================================
class DangKyHocPhan(TimestampSoftDeleteMixin):
    """DangKyHocPhan model."""

    __tablename__ = "DangKyHocPhan"

    MaDK: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    MaLopHP: Mapped[int] = mapped_column(BigInteger, ForeignKey("LopHocPhan.MaLopHP", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    TrangThai: Mapped[str] = mapped_column(String(20), nullable=False, default="ChoDuyet")
    DuocMien: Mapped[bool] = mapped_column(Boolean, default=False)
    LyDoMien: Mapped[str | None] = mapped_column(Text, nullable=True)
    NgayDK: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    NgayDuyet: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    NguoiDuyet: Mapped[str | None] = mapped_column(String(10), ForeignKey("quantri.maadmin", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)

    __table_args__ = (
        UniqueConstraint("MaSV", "MaLopHP", name="uq_dk_masv_malophp"),
    )

    # Relationships
    sinh_vien: Mapped[SinhVien] = relationship("SinhVien", back_populates="dang_ky")
    lop_hoc_phan: Mapped[LopHocPhan] = relationship("LopHocPhan", back_populates="dang_ky")
    nguoi_duyet: Mapped[QuanTri | None] = relationship("QuanTri")


# =============================================================================
# 14. PhanCongGiangDay
# =============================================================================
class PhanCongGiangDay(TimestampSoftDeleteMixin):
    """PhanCongGiangDay model."""

    __tablename__ = "PhanCongGiangDay"

    MaPC: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaLopHP: Mapped[int] = mapped_column(BigInteger, ForeignKey("LopHocPhan.MaLopHP", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    MaGV: Mapped[str] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    VaiTro: Mapped[str | None] = mapped_column(String(30), nullable=True, default="GiangVienChinh")
    SoTiet: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)

    __table_args__ = (
        UniqueConstraint("MaLopHP", "MaGV", name="uq_pc_lophp_gv"),
        CheckConstraint("VaiTro IN ('GiangVienChinh','TroGiang','GiangVienPhuTro')", name="chk_pc_vaitro"),
    )

    # Relationships
    lop_hoc_phan: Mapped[LopHocPhan] = relationship("LopHocPhan", back_populates="phan_cong")
    giang_vien: Mapped[GiangVien] = relationship("GiangVien", back_populates="phan_cong")
    lich_hoc: Mapped[list["LichHoc"]] = relationship("LichHoc", back_populates="phan_cong")


# =============================================================================
# 15. LichHoc
# =============================================================================
class LichHoc(TimestampSoftDeleteMixin):
    """LichHoc model."""

    __tablename__ = "LichHoc"

    MaLH: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaPC: Mapped[int] = mapped_column(BigInteger, ForeignKey("PhanCongGiangDay.MaPC", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    Thu: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    TietBatDau: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    SoTiet: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    Buoi: Mapped[str | None] = mapped_column(String(10), nullable=True)
    PhongHoc: Mapped[str | None] = mapped_column(String(50), nullable=True)

    __table_args__ = (
        CheckConstraint("Thu BETWEEN 2 AND 8", name="chk_lichhoc_thu"),
        CheckConstraint("TietBatDau BETWEEN 1 AND 15", name="chk_lichhoc_tietbd"),
        CheckConstraint("SoTiet BETWEEN 1 AND 6", name="chk_lichhoc_sotiet"),
    )

    # Relationships
    phan_cong: Mapped[PhanCongGiangDay] = relationship("PhanCongGiangDay", back_populates="lich_hoc")


# =============================================================================
# 16. KQ_HocTap
# =============================================================================
class KQ_HocTap(TimestampSoftDeleteMixin):
    """KQ_HocTap model."""

    __tablename__ = "KQ_HocTap"

    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    MaMH: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    MaHK: Mapped[str] = mapped_column(String(10), ForeignKey("HocKy.MaHK", ondelete="RESTRICT", onupdate="CASCADE"), primary_key=True)
    Diem: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    LoaiDiem: Mapped[str | None] = mapped_column(String(20), nullable=True, default="Thi")
    DiemHe4: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)
    DiemChu: Mapped[str | None] = mapped_column(String(2), nullable=True)
    GhiChu: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("Diem >= 0 AND Diem <= 10", name="chk_kq_diem"),
    )

    # Relationships
    sinh_vien: Mapped[SinhVien] = relationship("SinhVien", back_populates="kq_hoctap")
    mon_hoc: Mapped[MonHoc] = relationship("MonHoc", back_populates="kq_hoctap")
    hoc_ky: Mapped[HocKy] = relationship("HocKy")


# =============================================================================
# 17. LuanVan
# =============================================================================
class LuanVan(TimestampSoftDeleteMixin):
    """LuanVan model."""

    __tablename__ = "LuanVan"

    MaLV: Mapped[str] = mapped_column(String(15), primary_key=True)
    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, unique=True)
    MaGV: Mapped[str | None] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    TenDeTai: Mapped[str] = mapped_column(String(255), nullable=False)
    NgayDangKy: Mapped[date | None] = mapped_column(Date, nullable=True)
    NgayBaoVe: Mapped[date | None] = mapped_column(Date, nullable=True)
    TrangThai: Mapped[str] = mapped_column(String(20), nullable=False, default="ChuaBaoVe")
    DiemBaoVe: Mapped[Decimal | None] = mapped_column(Numeric(4, 2), nullable=True)
    DiemHe4: Mapped[Decimal | None] = mapped_column(Numeric(3, 2), nullable=True)
    DiemChu: Mapped[str | None] = mapped_column(String(2), nullable=True)
    GhiChu: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("DiemBaoVe IS NULL OR (DiemBaoVe >= 0 AND DiemBaoVe <= 10)", name="chk_lv_diem"),
    )

    # Relationships
    sinh_vien: Mapped[SinhVien] = relationship("SinhVien", back_populates="luan_van")
    giang_vien: Mapped[GiangVien | None] = relationship("GiangVien", back_populates="luan_van")
    de_cuong: Mapped[list["DeCuongLuanAn"]] = relationship("DeCuongLuanAn", back_populates="luan_van")
    hoi_dong: Mapped["HoiDongBaoVe | None"] = relationship("HoiDongBaoVe", back_populates="luan_van", uselist=False)


# =============================================================================
# 18. DeCuongLuanAn
# =============================================================================
class DeCuongLuanAn(TimestampSoftDeleteMixin):
    """DeCuongLuanAn model."""

    __tablename__ = "DeCuongLuanAn"

    MaDC: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaLV: Mapped[str] = mapped_column(String(15), ForeignKey("LuanVan.MaLV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    PhienBan: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=1)
    TieuDe: Mapped[str] = mapped_column(String(255), nullable=False)
    TomTat: Mapped[str | None] = mapped_column(Text, nullable=True)
    NoiDung: Mapped[str | None] = mapped_column(Text, nullable=True)
    FileDeCuong: Mapped[str | None] = mapped_column(String(500), nullable=True)
    TrangThai: Mapped[str] = mapped_column(String(20), nullable=False, default="Nhap")
    NgayNop: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    NgayDuyet: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    NguoiDuyet: Mapped[str | None] = mapped_column(String(10), ForeignKey("quantri.maadmin", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    BinhLuan: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("MaLV", "PhienBan", name="uq_dc_malv_phienban"),
    )

    # Relationships
    luan_van: Mapped[LuanVan] = relationship("LuanVan", back_populates="de_cuong")
    sinh_vien: Mapped[SinhVien] = relationship("SinhVien", back_populates="de_cuong")


# =============================================================================
# 19. DonGiaTinChi
# =============================================================================
class DonGiaTinChi(TimestampSoftDeleteMixin):
    """DonGiaTinChi model."""

    __tablename__ = "DonGiaTinChi"

    MaDonGia: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    NamHoc: Mapped[str] = mapped_column(String(9), nullable=False)
    HeDaoTao: Mapped[str] = mapped_column(String(20), nullable=False)
    MaNganh: Mapped[str | None] = mapped_column(String(10), ForeignKey("Nganh.MaNganh", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    DonGia: Mapped[Decimal] = mapped_column(Numeric(12, 0), nullable=False)

    __table_args__ = (
        CheckConstraint("DonGia > 0", name="chk_dongia_dongia"),
    )

    # Relationships
    nganh: Mapped[Nganh | None] = relationship("Nganh", back_populates="don_gia")


# =============================================================================
# 20. HocPhi
# =============================================================================
class HocPhi(TimestampSoftDeleteMixin):
    """HocPhi model."""

    __tablename__ = "HocPhi"

    MaHP: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    MaHK: Mapped[str] = mapped_column(String(10), ForeignKey("HocKy.MaHK", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    SoTien: Mapped[Decimal] = mapped_column(Numeric(15, 0), nullable=False)
    TrangThai: Mapped[str] = mapped_column(String(20), nullable=False, default="ChuaDong")
    NgayHanNop: Mapped[date | None] = mapped_column(Date, nullable=True)
    NgayDong: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    MaGiaoDich: Mapped[str | None] = mapped_column(String(100), nullable=True)
    GhiChu: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("MaSV", "MaHK", name="uq_hocphi_masv_mahk"),
        CheckConstraint("SoTien > 0 AND SoTien <= 1000000000", name="chk_hocphi_sotien"),
    )

    # Relationships
    sinh_vien: Mapped[SinhVien] = relationship("SinhVien", back_populates="hoc_phi")
    hoc_ky: Mapped[HocKy] = relationship("HocKy", back_populates="hoc_phi")


# =============================================================================
# 21. TotNghiep
# =============================================================================
class TotNghiep(TimestampSoftDeleteMixin):
    """TotNghiep model."""

    __tablename__ = "TotNghiep"

    MaSV: Mapped[str] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    GPA: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    TongTinChi: Mapped[int] = mapped_column(SmallInteger, nullable=False, default=0)
    XepLoai: Mapped[str] = mapped_column(String(20), nullable=False)
    NgayTotNghiep: Mapped[date | None] = mapped_column(Date, nullable=True)
    SoHieuBang: Mapped[str | None] = mapped_column(String(50), nullable=True, unique=True)

    __table_args__ = (
        CheckConstraint("GPA >= 0 AND GPA <= 4.0", name="chk_totnghiep_gpa"),
    )

    # Relationships
    sinh_vien: Mapped[SinhVien] = relationship("SinhVien", back_populates="tot_nghiep")


# =============================================================================
# 22. ThongBao
# =============================================================================
class ThongBao(TimestampSoftDeleteMixin):
    """ThongBao model."""

    __tablename__ = "ThongBao"

    MaTB: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    TieuDe: Mapped[str] = mapped_column(String(255), nullable=False)
    NoiDung: Mapped[str] = mapped_column(Text, nullable=False)
    LoaiTB: Mapped[str | None] = mapped_column(String(30), nullable=True, default="Chung")
    MucDo: Mapped[str | None] = mapped_column(String(10), nullable=True, default="BinhThuong")
    MaAdmin: Mapped[str | None] = mapped_column(String(10), ForeignKey("quantri.maadmin", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)

    # Relationships
    nguoi_tao: Mapped[QuanTri | None] = relationship("QuanTri", back_populates="thong_bao")
    nguoi_nhan: Mapped[list["TB_NguoiNhan"]] = relationship("TB_NguoiNhan", back_populates="thong_bao")


# =============================================================================
# 23. TB_NguoiNhan
# =============================================================================
class TB_NguoiNhan(TimestampSoftDeleteMixin):
    """TB_NguoiNhan model."""

    __tablename__ = "TB_NguoiNhan"

    MaTBNN: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaTB: Mapped[int | None] = mapped_column(BigInteger, ForeignKey("ThongBao.MaTB", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    MaSV: Mapped[str | None] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    MaGV: Mapped[str | None] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    TrangThaiDoc: Mapped[bool] = mapped_column(Boolean, default=False)
    ThoiGianDoc: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    # Relationships
    thong_bao: Mapped[ThongBao | None] = relationship("ThongBao", back_populates="nguoi_nhan")
    sinh_vien: Mapped[SinhVien | None] = relationship("SinhVien", back_populates="thong_bao")
    giang_vien: Mapped[GiangVien | None] = relationship("GiangVien", back_populates="thong_bao")


# =============================================================================
# 24. NghienCuuKhoaHoc
# =============================================================================
class NghienCuuKhoaHoc(TimestampSoftDeleteMixin):
    """NghienCuuKhoaHoc model."""

    __tablename__ = "NghienCuuKhoaHoc"

    MaNCKH: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    TenCongTrinh: Mapped[str] = mapped_column(String(255), nullable=False)
    LoaiCongTrinh: Mapped[str] = mapped_column(String(20), nullable=False)
    MoTa: Mapped[str | None] = mapped_column(Text, nullable=True)
    Cap: Mapped[str | None] = mapped_column(String(20), nullable=True, default="Truong")
    Nam: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    Link: Mapped[str | None] = mapped_column(String(500), nullable=True)
    FileMinhChung: Mapped[str | None] = mapped_column(String(500), nullable=True)

    __table_args__ = (
        CheckConstraint("Nam BETWEEN 2000 AND 2100", name="chk_nckh_nam"),
    )

    # Relationships
    tac_gia: Mapped[list["TacGiaCongTrinh"]] = relationship("TacGiaCongTrinh", back_populates="cong_trinh")


# =============================================================================
# 25. TacGiaCongTrinh
# =============================================================================
class TacGiaCongTrinh(TimestampSoftDeleteMixin):
    """TacGiaCongTrinh model."""

    __tablename__ = "TacGiaCongTrinh"

    MaTacGia: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaNCKH: Mapped[int] = mapped_column(BigInteger, ForeignKey("NghienCuuKhoaHoc.MaNCKH", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    MaGV: Mapped[str | None] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    MaSV: Mapped[str | None] = mapped_column(String(15), ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=True)
    VaiTro: Mapped[str] = mapped_column(String(30), nullable=False, default="DongTacGia")
    ThuTu: Mapped[int | None] = mapped_column(SmallInteger, nullable=True, default=1)

    __table_args__ = (
        UniqueConstraint("MaNCKH", "MaGV", "MaSV", name="uq_tacgia_nckh_gv_sv"),
    )

    # Relationships
    cong_trinh: Mapped[NghienCuuKhoaHoc] = relationship("NghienCuuKhoaHoc", back_populates="tac_gia")
    giang_vien: Mapped[GiangVien | None] = relationship("GiangVien", back_populates="tac_gia")
    sinh_vien: Mapped[SinhVien | None] = relationship("SinhVien", back_populates="tac_gia")


# =============================================================================
# 26. QuyDinhDacThu
# =============================================================================
class QuyDinhDacThu(TimestampSoftDeleteMixin):
    """QuyDinhDacThu model."""

    __tablename__ = "QuyDinhDacThu"

    MaQD: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    TenQD: Mapped[str] = mapped_column(String(200), nullable=False)
    MoTa: Mapped[str | None] = mapped_column(Text, nullable=True)
    MaNganh: Mapped[str | None] = mapped_column(String(10), ForeignKey("Nganh.MaNganh", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    KhoaTuyen: Mapped[str | None] = mapped_column(String(9), nullable=True)
    LoaiQuyDinh: Mapped[str] = mapped_column(String(30), nullable=False)
    GiaTri: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    DonVi: Mapped[str | None] = mapped_column(String(30), nullable=True)
    BatBuoc: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    nganh: Mapped[Nganh | None] = relationship("Nganh")


# =============================================================================
# 27. HoiDongBaoVe
# =============================================================================
class HoiDongBaoVe(TimestampSoftDeleteMixin):
    """HoiDongBaoVe model."""

    __tablename__ = "HoiDongBaoVe"

    MaHD: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaLV: Mapped[str] = mapped_column(String(15), ForeignKey("LuanVan.MaLV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, unique=True)
    TenHD: Mapped[str | None] = mapped_column(String(200), nullable=True)
    NgayThanhLap: Mapped[date | None] = mapped_column(Date, nullable=True)
    NgayBaoVe: Mapped[date | None] = mapped_column(Date, nullable=True)
    DiaDiem: Mapped[str | None] = mapped_column(String(200), nullable=True)
    TrangThai: Mapped[str] = mapped_column(String(20), nullable=False, default="ChuaThanhLap")
    GhiChu: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    luan_van: Mapped[LuanVan] = relationship("LuanVan", back_populates="hoi_dong")
    thanh_vien: Mapped[list["ThanhVienHoiDong"]] = relationship("ThanhVienHoiDong", back_populates="hoi_dong")
    thu_lao: Mapped[list["ThuLaoHoiDong"]] = relationship("ThuLaoHoiDong", back_populates="hoi_dong")


# =============================================================================
# 28. ThanhVienHoiDong
# =============================================================================
class ThanhVienHoiDong(TimestampSoftDeleteMixin):
    """ThanhVienHoiDong model."""

    __tablename__ = "ThanhVienHoiDong"

    MaTVHD: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaHD: Mapped[int] = mapped_column(BigInteger, ForeignKey("HoiDongBaoVe.MaHD", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    MaGV: Mapped[str] = mapped_column(String(15), ForeignKey("GiangVien.MaGV", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    VaiTro: Mapped[str] = mapped_column(String(30), nullable=False)
    DiemDanhGia: Mapped[Decimal | None] = mapped_column(Numeric(4, 2), nullable=True)
    NhanXet: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("MaHD", "MaGV", name="uq_tvhd_mahd_gv"),
    )

    # Relationships
    hoi_dong: Mapped[HoiDongBaoVe] = relationship("HoiDongBaoVe", back_populates="thanh_vien")
    giang_vien: Mapped[GiangVien] = relationship("GiangVien", back_populates="thanh_vien_hd")
    thu_lao: Mapped[list["ThuLaoHoiDong"]] = relationship("ThuLaoHoiDong", back_populates="thanh_vien")


# =============================================================================
# 29. ThuLaoHoiDong
# =============================================================================
class ThuLaoHoiDong(TimestampSoftDeleteMixin):
    """ThuLaoHoiDong model."""

    __tablename__ = "ThuLaoHoiDong"

    MaTL: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaTVHD: Mapped[int] = mapped_column(BigInteger, ForeignKey("ThanhVienHoiDong.MaTVHD", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    MaHD: Mapped[int] = mapped_column(BigInteger, ForeignKey("HoiDongBaoVe.MaHD", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    SoTien: Mapped[Decimal] = mapped_column(Numeric(12, 0), nullable=False)
    TrangThai: Mapped[str] = mapped_column(String(20), nullable=False, default="ChuaChiTra")
    NgayChiTra: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    MaGiaoDich: Mapped[str | None] = mapped_column(String(100), nullable=True)
    GhiChu: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint("MaTVHD", "MaHD", name="uq_thulao_matvhd_mahd"),
    )

    # Relationships
    thanh_vien: Mapped[ThanhVienHoiDong] = relationship("ThanhVienHoiDong", back_populates="thu_lao")
    hoi_dong: Mapped[HoiDongBaoVe] = relationship("HoiDongBaoVe", back_populates="thu_lao")


# =============================================================================
# 30. MonHocTienQuyet
# =============================================================================
class MonHocTienQuyet(TimestampSoftDeleteMixin):
    """MonHocTienQuyet model."""

    __tablename__ = "MonHocTienQuyet"

    MaMH: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    MaMHTienQuyet: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True)
    MoTa: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("MaMH != MaMHTienQuyet", name="chk_mhtq_mamh"),
    )

    # Relationships
    mon_hoc: Mapped[MonHoc] = relationship(
        "MonHoc", foreign_keys=lambda: [MonHocTienQuyet.MaMH], back_populates="mon_tien_quyet"
    )
    mon_tien_quyet: Mapped[MonHoc] = relationship(
        "MonHoc", foreign_keys=lambda: [MonHocTienQuyet.MaMHTienQuyet], back_populates="mon_duoc_tien_quyet"
    )


# =============================================================================
# 31. ChuongTrinhDaoTao
# =============================================================================
class ChuongTrinhDaoTao(TimestampSoftDeleteMixin):
    """ChuongTrinhDaoTao model."""

    __tablename__ = "ChuongTrinhDaoTao"

    MaCTDT: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaNganh: Mapped[str] = mapped_column(String(10), ForeignKey("Nganh.MaNganh", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    MaMH: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    HocKy: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    LoaiMH: Mapped[str | None] = mapped_column(String(20), nullable=True, default="BatBuoc")

    __table_args__ = (
        UniqueConstraint("MaNganh", "MaMH", name="uq_ctdt_manganh_mamh"),
    )

    # Relationships
    nganh: Mapped[Nganh] = relationship("Nganh", back_populates="chuong_trinh_dao_tao")
    mon_hoc: Mapped[MonHoc] = relationship("MonHoc", back_populates="chuong_trinh")


# =============================================================================
# 32. LichThi
# =============================================================================
class LichThi(TimestampSoftDeleteMixin):
    """LichThi model."""

    __tablename__ = "LichThi"

    MaLT: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    MaMH: Mapped[str] = mapped_column(String(10), ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    MaHK: Mapped[str] = mapped_column(String(10), ForeignKey("HocKy.MaHK", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    LoaiThi: Mapped[str | None] = mapped_column(String(20), nullable=True, default="CuoiKy")
    NgayThi: Mapped[date] = mapped_column(Date, nullable=False)
    GioThi: Mapped[datetime] = mapped_column(Time, nullable=False)
    ThoiLuong: Mapped[int | None] = mapped_column(SmallInteger, nullable=True)
    DiaDiem: Mapped[str | None] = mapped_column(String(200), nullable=True)
    HinhThuc: Mapped[str | None] = mapped_column(String(30), nullable=True, default="Viet")
    GhiChu: Mapped[str | None] = mapped_column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint("ThoiLuong > 0 AND ThoiLuong <= 300", name="chk_lichthi_thoiluong"),
    )

    # Relationships
    mon_hoc: Mapped[MonHoc] = relationship("MonHoc")
    hoc_ky: Mapped[HocKy] = relationship("HocKy", back_populates="lich_thi")


# =============================================================================
# 33. AuditLog
# =============================================================================
class AuditLog:
    """AuditLog model (no soft delete, system-managed)."""

    __tablename__ = "AuditLog"

    MaAudit: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    UserId: Mapped[str | None] = mapped_column(String(15), nullable=True)
    UserType: Mapped[str | None] = mapped_column(String(20), nullable=True)
    Action: Mapped[str] = mapped_column(String(10), nullable=False)
    TableName: Mapped[str] = mapped_column(String(50), nullable=False)
    RecordId: Mapped[str | None] = mapped_column(String(15), nullable=True)
    OldData: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSONB stored as TEXT
    NewData: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSONB stored as TEXT
    IpAddress: Mapped[str | None] = mapped_column(String(45), nullable=True)
    UserAgent: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
