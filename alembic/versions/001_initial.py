"""Initial migration - create all tables

Revision ID: 001_initial
Revises:
Create Date: 2026-04-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ENUM types
    op.execute("CREATE TYPE trang_thai_xet_tuyen AS ENUM ('ChoDuyet', 'DaDuyet', 'TuChoi')")
    op.execute("CREATE TYPE trang_thai_hoc_phi AS ENUM ('ChuaDong', 'DaDong', 'DongMotPhan')")
    op.execute("CREATE TYPE hoc_vi AS ENUM ('CuNhan', 'ThacSi', 'TienSi', 'PhoGiaoSu', 'GiaoSu')")
    op.execute("CREATE TYPE hoc_ham AS ENUM ('GiangVien', 'PhoGiaoSu', 'GiaoSu')")
    op.execute("CREATE TYPE xep_loai_tot_nghiep AS ENUM ('XuatSac', 'Gioi', 'Kha', 'TrungBinh', 'Yeu')")
    op.execute("CREATE TYPE trang_thai_luan_van AS ENUM ('ChuaBaoVe', 'DangThucHien', 'DaBaoVe', 'CanChinhSua', 'TuChoi')")
    op.execute("CREATE TYPE trang_thai_de_cuong AS ENUM ('Nhap', 'ChoDuyet', 'DaDuyet', 'CanChinhSua', 'TuChoi')")
    op.execute("CREATE TYPE loai_cong_trinh AS ENUM ('BaiBao', 'SachChuyenKhao', 'DeTaiNCKH', 'HoiThao', 'Patent', 'Khac')")
    op.execute("CREATE TYPE trang_thai_dang_ky AS ENUM ('ChoDuyet', 'DaDongHP', 'DaDuyet', 'Huy')")
    op.execute("CREATE TYPE he_dao_tao AS ENUM ('ChinhQuy', 'KhongChinhQuy', 'VuaHocVuaLam')")
    op.execute("CREATE TYPE gioi_tinh AS ENUM ('Nam', 'Nu', 'Khac')")
    op.execute("CREATE TYPE trang_thai_hoi_dong AS ENUM ('ChuaThanhLap', 'DaThanhLap', 'DangHoatDong', 'DaKetThuc', 'Huy')")
    op.execute("CREATE TYPE trang_thai_thu_lao AS ENUM ('ChuaChiTra', 'DaChiTra', 'Huy')")

    # 1. Khoa
    op.create_table(
        "Khoa",
        sa.Column("MaKhoa", sa.String(5), primary_key=True),
        sa.Column("TenKhoa", sa.String(100), nullable=False, unique=True),
        sa.Column("DiaChi", sa.String(255), nullable=True),
        sa.Column("SDT", sa.String(11), nullable=True),
        sa.Column("Email", sa.String(100), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 2. Nganh
    op.create_table(
        "Nganh",
        sa.Column("MaNganh", sa.String(10), primary_key=True),
        sa.Column("TenNganh", sa.String(100), nullable=False),
        sa.Column("MaKhoa", sa.String(5), sa.ForeignKey("Khoa.MaKhoa", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("MoTa", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 3. Lop
    op.create_table(
        "Lop",
        sa.Column("MaLop", sa.String(15), primary_key=True),
        sa.Column("TenLop", sa.String(100), nullable=False, unique=True),
        sa.Column("MaNganh", sa.String(10), sa.ForeignKey("Nganh.MaNganh", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("SiSo", sa.SmallInteger, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 4. MonHoc
    op.create_table(
        "MonHoc",
        sa.Column("MaMH", sa.String(10), primary_key=True),
        sa.Column("TenMH", sa.String(100), nullable=False),
        sa.Column("SoTinChi", sa.SmallInteger, nullable=False),
        sa.Column("MoTa", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("SoTinChi BETWEEN 1 AND 10", name="chk_monhoc_sotc"),
    )

    # 5. HocKy
    op.create_table(
        "HocKy",
        sa.Column("MaHK", sa.String(10), primary_key=True),
        sa.Column("TenHK", sa.String(50), nullable=False),
        sa.Column("NamHoc", sa.String(9), nullable=False),
        sa.Column("ThoiGianBD", sa.Date, nullable=False),
        sa.Column("ThoiGianKT", sa.Date, nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("ThoiGianKT > ThoiGianBD", name="chk_hocky_tg"),
    )

    # 6. QuanTri
    op.create_table(
        "QuanTri",
        sa.Column("MaAdmin", sa.String(10), primary_key=True),
        sa.Column("TenDN", sa.String(50), nullable=False, unique=True),
        sa.Column("MatKhau", sa.String(255), nullable=False),
        sa.Column("HoTen", sa.String(100), nullable=False),
        sa.Column("Email", sa.String(100), nullable=False, unique=True),
        sa.Column("SDT", sa.String(11), nullable=True),
        sa.Column("VaiTro", sa.String(20), nullable=False, server_default="admin"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("VaiTro IN ('admin','super_admin','khoa')", name="chk_quantri_vaitro"),
    )

    # 7. TK_XetTuyen
    op.create_table(
        "TK_XetTuyen",
        sa.Column("MaTK", sa.String(10), primary_key=True),
        sa.Column("Email", sa.String(100), nullable=False, unique=True),
        sa.Column("MatKhau", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 8. HSO_XetTuyen
    op.create_table(
        "HSO_XetTuyen",
        sa.Column("MaHSO", sa.String(10), primary_key=True),
        sa.Column("MaTK", sa.String(10), sa.ForeignKey("TK_XetTuyen.MaTK", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("HoTen", sa.String(100), nullable=False),
        sa.Column("GioiTinh", sa.String(10), nullable=True),
        sa.Column("NgaySinh", sa.Date, nullable=True),
        sa.Column("CCCD", sa.String(12), nullable=True),
        sa.Column("SDT", sa.String(11), nullable=False),
        sa.Column("Email", sa.String(100), nullable=True),
        sa.Column("DiaChi", sa.String(255), nullable=True),
        sa.Column("QueQuan", sa.String(100), nullable=True),
        sa.Column("NoiSinh", sa.String(100), nullable=True),
        sa.Column("DanToc", sa.String(50), nullable=True),
        sa.Column("TrinhDoNgoaiNgu", sa.String(50), nullable=True, server_default="Không"),
        sa.Column("BangTotNghiep", sa.Text, nullable=True),
        sa.Column("FileCCCD", sa.String(500), nullable=True),
        sa.Column("FileBangDiem", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("CCCD", name="uq_hso_cccd"),
        sa.UniqueConstraint("SDT", name="uq_hso_sdt"),
    )

    # 9. PT_XetTuyen
    op.create_table(
        "PT_XetTuyen",
        sa.Column("MaPTXT", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaNganh", sa.String(10), sa.ForeignKey("Nganh.MaNganh", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("PhuongThuc", sa.String(100), nullable=False),
        sa.Column("Diem", sa.Numeric(4, 2), nullable=False),
        sa.Column("TrangThai", sa.String(20), nullable=False, server_default="ChoDuyet"),
        sa.Column("MaHSO", sa.String(10), sa.ForeignKey("HSO_XetTuyen.MaHSO", ondelete="CASCADE", onupdate="CASCADE"), nullable=True),
        sa.Column("MaAdmin", sa.String(10), sa.ForeignKey("QuanTri.MaAdmin", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("NgayNop", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("NgayDuyet", sa.DateTime(timezone=True), nullable=True),
        sa.Column("GhiChu", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("Diem >= 0 AND Diem <= 10", name="chk_ptxt_diem"),
    )

    # 10. SinhVien
    op.create_table(
        "SinhVien",
        sa.Column("MaSV", sa.String(15), primary_key=True),
        sa.Column("HoTen", sa.String(100), nullable=False),
        sa.Column("NgaySinh", sa.Date, nullable=False),
        sa.Column("GioiTinh", sa.String(10), nullable=True),
        sa.Column("Email", sa.String(100), nullable=False, unique=True),
        sa.Column("MatKhau", sa.String(255), nullable=False),
        sa.Column("MaLop", sa.String(15), sa.ForeignKey("Lop.MaLop", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("MaHSO", sa.String(10), sa.ForeignKey("HSO_XetTuyen.MaHSO", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("MaTK", sa.String(10), sa.ForeignKey("TK_XetTuyen.MaTK", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("HeDaoTao", sa.String(20), nullable=False, server_default="ChinhQuy"),
        sa.Column("QueQuan", sa.String(100), nullable=True),
        sa.Column("NoiSinh", sa.String(100), nullable=True),
        sa.Column("DanToc", sa.String(50), nullable=True),
        sa.Column("DiaChi", sa.String(255), nullable=True),
        sa.Column("SDT", sa.String(11), nullable=True),
        sa.Column("CCCD", sa.String(12), nullable=True),
        sa.Column("BangTotNghiepURL", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 11. GiangVien
    op.create_table(
        "GiangVien",
        sa.Column("MaGV", sa.String(15), primary_key=True),
        sa.Column("HoTen", sa.String(100), nullable=False),
        sa.Column("Email", sa.String(100), nullable=False, unique=True),
        sa.Column("SDT", sa.String(11), nullable=True),
        sa.Column("HocVi", sa.String(20), nullable=True),
        sa.Column("HocHam", sa.String(20), nullable=True),
        sa.Column("ChuyenNganh", sa.String(100), nullable=True),
        sa.Column("DiaChi", sa.String(255), nullable=True),
        sa.Column("MaKhoa", sa.String(5), sa.ForeignKey("Khoa.MaKhoa", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("MatKhau", sa.String(255), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 12. LopHocPhan
    op.create_table(
        "LopHocPhan",
        sa.Column("MaLopHP", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaMH", sa.String(10), sa.ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("MaHK", sa.String(10), sa.ForeignKey("HocKy.MaHK", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("MaGV", sa.String(15), sa.ForeignKey("GiangVien.MaGV", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False),
        sa.Column("TenNhom", sa.String(50), nullable=True),
        sa.Column("SiSoToiDa", sa.SmallInteger, nullable=False, server_default="50"),
        sa.Column("SiSoHienTai", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("MoTa", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("MaMH", "MaHK", "TenNhom", name="uq_lophp_mamh_mahk_tennhom"),
        sa.CheckConstraint("SiSoToiDa > 0", name="chk_lophp_sisomax"),
        sa.CheckConstraint("SiSoHienTai >= 0", name="chk_lophp_sisohientai"),
    )

    # 13. DangKyHocPhan
    op.create_table(
        "DangKyHocPhan",
        sa.Column("MaDK", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaSV", sa.String(15), sa.ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("MaLopHP", sa.BigInteger, sa.ForeignKey("LopHocPhan.MaLopHP", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("TrangThai", sa.String(20), nullable=False, server_default="ChoDuyet"),
        sa.Column("DuocMien", sa.Boolean, server_default="false"),
        sa.Column("LyDoMien", sa.Text, nullable=True),
        sa.Column("NgayDK", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("NgayDuyet", sa.DateTime(timezone=True), nullable=True),
        sa.Column("NguoiDuyet", sa.String(10), sa.ForeignKey("QuanTri.MaAdmin", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("MaSV", "MaLopHP", name="uq_dk_masv_malophp"),
    )

    # 14. PhanCongGiangDay
    op.create_table(
        "PhanCongGiangDay",
        sa.Column("MaPC", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaLopHP", sa.BigInteger, sa.ForeignKey("LopHocPhan.MaLopHP", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("MaGV", sa.String(15), sa.ForeignKey("GiangVien.MaGV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("VaiTro", sa.String(30), nullable=True, server_default="GiangVienChinh"),
        sa.Column("SoTiet", sa.SmallInteger, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("MaLopHP", "MaGV", name="uq_pc_lophp_gv"),
        sa.CheckConstraint("VaiTro IN ('GiangVienChinh','TroGiang','GiangVienPhuTro')", name="chk_pc_vaitro"),
    )

    # 15. LichHoc
    op.create_table(
        "LichHoc",
        sa.Column("MaLH", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaPC", sa.BigInteger, sa.ForeignKey("PhanCongGiangDay.MaPC", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("Thu", sa.SmallInteger, nullable=False),
        sa.Column("TietBatDau", sa.SmallInteger, nullable=False),
        sa.Column("SoTiet", sa.SmallInteger, nullable=False),
        sa.Column("Buoi", sa.String(10), nullable=True),
        sa.Column("PhongHoc", sa.String(50), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("Thu BETWEEN 2 AND 8", name="chk_lichhoc_thu"),
        sa.CheckConstraint("TietBatDau BETWEEN 1 AND 15", name="chk_lichhoc_tietbd"),
        sa.CheckConstraint("SoTiet BETWEEN 1 AND 6", name="chk_lichhoc_sotiet"),
    )

    # 16. KQ_HocTap
    op.create_table(
        "KQ_HocTap",
        sa.Column("MaSV", sa.String(15), sa.ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
        sa.Column("MaMH", sa.String(10), sa.ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
        sa.Column("MaHK", sa.String(10), sa.ForeignKey("HocKy.MaHK", ondelete="RESTRICT", onupdate="CASCADE"), primary_key=True),
        sa.Column("Diem", sa.Numeric(4, 2), nullable=False),
        sa.Column("LoaiDiem", sa.String(20), nullable=True, server_default="Thi"),
        sa.Column("DiemHe4", sa.Numeric(3, 2), nullable=True),
        sa.Column("DiemChu", sa.String(2), nullable=True),
        sa.Column("GhiChu", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("Diem >= 0 AND Diem <= 10", name="chk_kq_diem"),
    )

    # 17. LuanVan
    op.create_table(
        "LuanVan",
        sa.Column("MaLV", sa.String(15), primary_key=True),
        sa.Column("MaSV", sa.String(15), sa.ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, unique=True),
        sa.Column("MaGV", sa.String(15), sa.ForeignKey("GiangVien.MaGV", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("TenDeTai", sa.String(255), nullable=False),
        sa.Column("NgayDangKy", sa.Date, nullable=True),
        sa.Column("NgayBaoVe", sa.Date, nullable=True),
        sa.Column("TrangThai", sa.String(20), nullable=False, server_default="ChuaBaoVe"),
        sa.Column("DiemBaoVe", sa.Numeric(4, 2), nullable=True),
        sa.Column("DiemHe4", sa.Numeric(3, 2), nullable=True),
        sa.Column("DiemChu", sa.String(2), nullable=True),
        sa.Column("GhiChu", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("DiemBaoVe IS NULL OR (DiemBaoVe >= 0 AND DiemBaoVe <= 10)", name="chk_lv_diem"),
    )

    # 18. DeCuongLuanAn
    op.create_table(
        "DeCuongLuanAn",
        sa.Column("MaDC", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaLV", sa.String(15), sa.ForeignKey("LuanVan.MaLV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("MaSV", sa.String(15), sa.ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("PhienBan", sa.SmallInteger, nullable=False, server_default="1"),
        sa.Column("TieuDe", sa.String(255), nullable=False),
        sa.Column("TomTat", sa.Text, nullable=True),
        sa.Column("NoiDung", sa.Text, nullable=True),
        sa.Column("FileDeCuong", sa.String(500), nullable=True),
        sa.Column("TrangThai", sa.String(20), nullable=False, server_default="Nhap"),
        sa.Column("NgayNop", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("NgayDuyet", sa.DateTime(timezone=True), nullable=True),
        sa.Column("NguoiDuyet", sa.String(10), sa.ForeignKey("QuanTri.MaAdmin", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("BinhLuan", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("MaLV", "PhienBan", name="uq_dc_malv_phienban"),
    )

    # 19. DonGiaTinChi
    op.create_table(
        "DonGiaTinChi",
        sa.Column("MaDonGia", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("NamHoc", sa.String(9), nullable=False),
        sa.Column("HeDaoTao", sa.String(20), nullable=False),
        sa.Column("MaNganh", sa.String(10), sa.ForeignKey("Nganh.MaNganh", ondelete="CASCADE", onupdate="CASCADE"), nullable=True),
        sa.Column("DonGia", sa.Numeric(12, 0), nullable=False),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("DonGia > 0", name="chk_dongia_dongia"),
    )

    # 20. HocPhi
    op.create_table(
        "HocPhi",
        sa.Column("MaHP", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaSV", sa.String(15), sa.ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("MaHK", sa.String(10), sa.ForeignKey("HocKy.MaHK", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False),
        sa.Column("SoTien", sa.Numeric(15, 0), nullable=False),
        sa.Column("TrangThai", sa.String(20), nullable=False, server_default="ChuaDong"),
        sa.Column("NgayHanNop", sa.Date, nullable=True),
        sa.Column("NgayDong", sa.DateTime(timezone=True), nullable=True),
        sa.Column("MaGiaoDich", sa.String(100), nullable=True),
        sa.Column("GhiChu", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("MaSV", "MaHK", name="uq_hocphi_masv_mahk"),
        sa.CheckConstraint("SoTien > 0 AND SoTien <= 1000000000", name="chk_hocphi_sotien"),
    )

    # 21. TotNghiep
    op.create_table(
        "TotNghiep",
        sa.Column("MaSV", sa.String(15), sa.ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
        sa.Column("GPA", sa.Numeric(4, 2), nullable=False),
        sa.Column("TongTinChi", sa.SmallInteger, nullable=False, server_default="0"),
        sa.Column("XepLoai", sa.String(20), nullable=False),
        sa.Column("NgayTotNghiep", sa.Date, nullable=True),
        sa.Column("SoHieuBang", sa.String(50), nullable=True, unique=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("GPA >= 0 AND GPA <= 4.0", name="chk_totnghiep_gpa"),
    )

    # 22. ThongBao
    op.create_table(
        "ThongBao",
        sa.Column("MaTB", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("TieuDe", sa.String(255), nullable=False),
        sa.Column("NoiDung", sa.Text, nullable=False),
        sa.Column("LoaiTB", sa.String(30), nullable=True, server_default="Chung"),
        sa.Column("MucDo", sa.String(10), nullable=True, server_default="BinhThuong"),
        sa.Column("MaAdmin", sa.String(10), sa.ForeignKey("QuanTri.MaAdmin", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 23. TB_NguoiNhan
    op.create_table(
        "TB_NguoiNhan",
        sa.Column("MaTBNN", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaTB", sa.BigInteger, sa.ForeignKey("ThongBao.MaTB", ondelete="CASCADE", onupdate="CASCADE"), nullable=True),
        sa.Column("MaSV", sa.String(15), sa.ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=True),
        sa.Column("MaGV", sa.String(15), sa.ForeignKey("GiangVien.MaGV", ondelete="CASCADE", onupdate="CASCADE"), nullable=True),
        sa.Column("TrangThaiDoc", sa.Boolean, server_default="false"),
        sa.Column("ThoiGianDoc", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 24. NghienCuuKhoaHoc
    op.create_table(
        "NghienCuuKhoaHoc",
        sa.Column("MaNCKH", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("TenCongTrinh", sa.String(255), nullable=False),
        sa.Column("LoaiCongTrinh", sa.String(20), nullable=False),
        sa.Column("MoTa", sa.Text, nullable=True),
        sa.Column("Cap", sa.String(20), nullable=True, server_default="Truong"),
        sa.Column("Nam", sa.SmallInteger, nullable=False),
        sa.Column("Link", sa.String(500), nullable=True),
        sa.Column("FileMinhChung", sa.String(500), nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("Nam BETWEEN 2000 AND 2100", name="chk_nckh_nam"),
    )

    # 25. TacGiaCongTrinh
    op.create_table(
        "TacGiaCongTrinh",
        sa.Column("MaTacGia", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaNCKH", sa.BigInteger, sa.ForeignKey("NghienCuuKhoaHoc.MaNCKH", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("MaGV", sa.String(15), sa.ForeignKey("GiangVien.MaGV", ondelete="CASCADE", onupdate="CASCADE"), nullable=True),
        sa.Column("MaSV", sa.String(15), sa.ForeignKey("SinhVien.MaSV", ondelete="CASCADE", onupdate="CASCADE"), nullable=True),
        sa.Column("VaiTro", sa.String(30), nullable=False, server_default="DongTacGia"),
        sa.Column("ThuTu", sa.SmallInteger, nullable=True, server_default="1"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("MaNCKH", "MaGV", "MaSV", name="uq_tacgia_nckh_gv_sv"),
    )

    # 26. QuyDinhDacThu
    op.create_table(
        "QuyDinhDacThu",
        sa.Column("MaQD", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("TenQD", sa.String(200), nullable=False),
        sa.Column("MoTa", sa.Text, nullable=True),
        sa.Column("MaNganh", sa.String(10), sa.ForeignKey("Nganh.MaNganh", ondelete="SET NULL", onupdate="CASCADE"), nullable=True),
        sa.Column("KhoaTuyen", sa.String(9), nullable=True),
        sa.Column("LoaiQuyDinh", sa.String(30), nullable=False),
        sa.Column("GiaTri", sa.Numeric(10, 2), nullable=False),
        sa.Column("DonVi", sa.String(30), nullable=True),
        sa.Column("BatBuoc", sa.Boolean, server_default="false"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 27. HoiDongBaoVe
    op.create_table(
        "HoiDongBaoVe",
        sa.Column("MaHD", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaLV", sa.String(15), sa.ForeignKey("LuanVan.MaLV", ondelete="CASCADE", onupdate="CASCADE"), nullable=False, unique=True),
        sa.Column("TenHD", sa.String(200), nullable=True),
        sa.Column("NgayThanhLap", sa.Date, nullable=True),
        sa.Column("NgayBaoVe", sa.Date, nullable=True),
        sa.Column("DiaDiem", sa.String(200), nullable=True),
        sa.Column("TrangThai", sa.String(20), nullable=False, server_default="ChuaThanhLap"),
        sa.Column("GhiChu", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    )

    # 28. ThanhVienHoiDong
    op.create_table(
        "ThanhVienHoiDong",
        sa.Column("MaTVHD", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaHD", sa.BigInteger, sa.ForeignKey("HoiDongBaoVe.MaHD", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("MaGV", sa.String(15), sa.ForeignKey("GiangVien.MaGV", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False),
        sa.Column("VaiTro", sa.String(30), nullable=False),
        sa.Column("DiemDanhGia", sa.Numeric(4, 2), nullable=True),
        sa.Column("NhanXet", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("MaHD", "MaGV", name="uq_tvhd_mahd_gv"),
    )

    # 29. ThuLaoHoiDong
    op.create_table(
        "ThuLaoHoiDong",
        sa.Column("MaTL", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaTVHD", sa.BigInteger, sa.ForeignKey("ThanhVienHoiDong.MaTVHD", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("MaHD", sa.BigInteger, sa.ForeignKey("HoiDongBaoVe.MaHD", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("SoTien", sa.Numeric(12, 0), nullable=False),
        sa.Column("TrangThai", sa.String(20), nullable=False, server_default="ChuaChiTra"),
        sa.Column("NgayChiTra", sa.DateTime(timezone=True), nullable=True),
        sa.Column("MaGiaoDich", sa.String(100), nullable=True),
        sa.Column("GhiChu", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("MaTVHD", "MaHD", name="uq_thulao_matvhd_mahd"),
    )

    # 30. MonHocTienQuyet
    op.create_table(
        "MonHocTienQuyet",
        sa.Column("MaMH", sa.String(10), sa.ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
        sa.Column("MaMHTienQuyet", sa.String(10), sa.ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), primary_key=True),
        sa.Column("MoTa", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("MaMH != MaMHTienQuyet", name="chk_mhtq_mamh"),
    )

    # 31. ChuongTrinhDaoTao
    op.create_table(
        "ChuongTrinhDaoTao",
        sa.Column("MaCTDT", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaNganh", sa.String(10), sa.ForeignKey("Nganh.MaNganh", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("MaMH", sa.String(10), sa.ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("HocKy", sa.SmallInteger, nullable=True),
        sa.Column("LoaiMH", sa.String(20), nullable=True, server_default="BatBuoc"),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint("MaNganh", "MaMH", name="uq_ctdt_manganh_mamh"),
    )

    # 32. LichThi
    op.create_table(
        "LichThi",
        sa.Column("MaLT", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("MaMH", sa.String(10), sa.ForeignKey("MonHoc.MaMH", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("MaHK", sa.String(10), sa.ForeignKey("HocKy.MaHK", ondelete="CASCADE", onupdate="CASCADE"), nullable=False),
        sa.Column("LoaiThi", sa.String(20), nullable=True, server_default="CuoiKy"),
        sa.Column("NgayThi", sa.Date, nullable=False),
        sa.Column("GioThi", sa.Time, nullable=False),
        sa.Column("ThoiLuong", sa.SmallInteger, nullable=True),
        sa.Column("DiaDiem", sa.String(200), nullable=True),
        sa.Column("HinhThuc", sa.String(30), nullable=True, server_default="Viet"),
        sa.Column("GhiChu", sa.Text, nullable=True),
        sa.Column("is_active", sa.Boolean, nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.CheckConstraint("ThoiLuong > 0 AND ThoiLuong <= 300", name="chk_lichthi_thoiluong"),
    )

    # 33. AuditLog
    op.create_table(
        "AuditLog",
        sa.Column("MaAudit", sa.BigInteger, primary_key=True, autoincrement=True),
        sa.Column("UserId", sa.String(15), nullable=True),
        sa.Column("UserType", sa.String(20), nullable=True),
        sa.Column("Action", sa.String(10), nullable=False),
        sa.Column("TableName", sa.String(50), nullable=False),
        sa.Column("RecordId", sa.String(15), nullable=True),
        sa.Column("OldData", sa.Text, nullable=True),
        sa.Column("NewData", sa.Text, nullable=True),
        sa.Column("IpAddress", sa.String(45), nullable=True),
        sa.Column("UserAgent", sa.String(500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.func.now()),
    )

    # Indexes
    op.create_index("idx_sinhvien_malop", "SinhVien", ["MaLop"])
    op.create_index("idx_sinhvien_email", "SinhVien", ["Email"])
    op.create_index("idx_kqhoctap_masv", "KQ_HocTap", ["MaSV"])
    op.create_index("idx_kqhoctap_mamh", "KQ_HocTap", ["MaMH"])
    op.create_index("idx_kqhoctap_mahk", "KQ_HocTap", ["MaHK"])
    op.create_index("idx_ptxettuyen_trangthai", "PT_XetTuyen", ["TrangThai"])
    op.create_index("idx_luanvan_magv", "LuanVan", ["MaGV"])
    op.create_index("idx_luanvan_masv", "LuanVan", ["MaSV"])
    op.create_index("idx_hocphi_masv", "HocPhi", ["MaSV"])
    op.create_index("idx_hocphi_mahk", "HocPhi", ["MaHK"])
    op.create_index("idx_giangvien_makhoa", "GiangVien", ["MaKhoa"])
    op.create_index("idx_dk_masv", "DangKyHocPhan", ["MaSV"])
    op.create_index("idx_dk_malophp", "DangKyHocPhan", ["MaLopHP"])
    op.create_index("idx_pc_magv", "PhanCongGiangDay", ["MaGV"])
    op.create_index("idx_pc_malophp", "PhanCongGiangDay", ["MaLopHP"])
    op.create_index("idx_lophp_mamh", "LopHocPhan", ["MaMH"])
    op.create_index("idx_lophp_mahk", "LopHocPhan", ["MaHK"])
    op.create_index("idx_lichhoc_mapc", "LichHoc", ["MaPC"])


def downgrade() -> None:
    op.drop_table("AuditLog")
    op.drop_table("LichThi")
    op.drop_table("ChuongTrinhDaoTao")
    op.drop_table("MonHocTienQuyet")
    op.drop_table("ThuLaoHoiDong")
    op.drop_table("ThanhVienHoiDong")
    op.drop_table("HoiDongBaoVe")
    op.drop_table("QuyDinhDacThu")
    op.drop_table("TacGiaCongTrinh")
    op.drop_table("NghienCuuKhoaHoc")
    op.drop_table("TB_NguoiNhan")
    op.drop_table("ThongBao")
    op.drop_table("TotNghiep")
    op.drop_table("HocPhi")
    op.drop_table("DonGiaTinChi")
    op.drop_table("DeCuongLuanAn")
    op.drop_table("LuanVan")
    op.drop_table("KQ_HocTap")
    op.drop_table("LichHoc")
    op.drop_table("PhanCongGiangDay")
    op.drop_table("DangKyHocPhan")
    op.drop_table("LopHocPhan")
    op.drop_table("GiangVien")
    op.drop_table("SinhVien")
    op.drop_table("PT_XetTuyen")
    op.drop_table("HSO_XetTuyen")
    op.drop_table("TK_XetTuyen")
    op.drop_table("QuanTri")
    op.drop_table("HocKy")
    op.drop_table("MonHoc")
    op.drop_table("Lop")
    op.drop_table("Nganh")
    op.drop_table("Khoa")
    op.execute("DROP TYPE trang_thai_xet_tuyen")
    op.execute("DROP TYPE trang_thai_hoc_phi")
    op.execute("DROP TYPE hoc_vi")
    op.execute("DROP TYPE hoc_ham")
    op.execute("DROP TYPE xep_loai_tot_nghiep")
    op.execute("DROP TYPE trang_thai_luan_van")
    op.execute("DROP TYPE trang_thai_de_cuong")
    op.execute("DROP TYPE loai_cong_trinh")
    op.execute("DROP TYPE trang_thai_dang_ky")
    op.execute("DROP TYPE he_dao_tao")
    op.execute("DROP TYPE gioi_tinh")
    op.execute("DROP TYPE trang_thai_hoi_dong")
    op.execute("DROP TYPE trang_thai_thu_lao")
