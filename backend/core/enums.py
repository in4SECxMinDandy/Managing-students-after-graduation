"""Application enums mirrored from PostgreSQL types."""
from enum import Enum


class TrangThaiXetTuyen(str, Enum):
    CHO_DUYET = "ChoDuyet"
    DA_DUYET = "DaDuyet"
    TU_CHOI = "TuChoi"


class TrangThaiHocPhi(str, Enum):
    CHUA_DONG = "ChuaDong"
    DA_DONG = "DaDong"
    DONG_MOT_PHAN = "DongMotPhan"


class HocVi(str, Enum):
    CU_NHAN = "CuNhan"
    THAC_SI = "ThacSi"
    TIEN_SI = "TienSi"
    PHO_GIAO_SU = "PhoGiaoSu"
    GIAO_SU = "GiaoSu"


class HocHam(str, Enum):
    GIANG_VIEN = "GiangVien"
    PHO_GIAO_SU = "PhoGiaoSu"
    GIAO_SU = "GiaoSu"


class XepLoaiTotNghiep(str, Enum):
    XUAT_SAC = "XuatSac"
    GIOI = "Gioi"
    KHA = "Kha"
    TRUNG_BINH = "TrungBinh"
    YEU = "Yeu"


class TrangThaiLuanVan(str, Enum):
    CHUA_BAO_VE = "ChuaBaoVe"
    DANG_THUC_HIEN = "DangThucHien"
    DA_BAO_VE = "DaBaoVe"
    CAN_CHINH_SUA = "CanChinhSua"
    TU_CHOI = "TuChoi"


class TrangThaiDeCuong(str, Enum):
    NHAP = "Nhap"
    CHO_DUYET = "ChoDuyet"
    DA_DUYET = "DaDuyet"
    CAN_CHINH_SUA = "CanChinhSua"
    TU_CHOI = "TuChoi"


class LoaiCongTrinh(str, Enum):
    BAI_BAO = "BaiBao"
    SACH_CHUYEN_KHAO = "SachChuyenKhao"
    DE_TAI_NCKH = "DeTaiNCKH"
    HOI_THAO = "HoiThao"
    PATENT = "Patent"
    KHAC = "Khac"


class TrangThaiDangKy(str, Enum):
    CHO_DUYET = "ChoDuyet"
    DA_DONG_HP = "DaDongHP"
    DA_DUYET = "DaDuyet"
    HUY = "Huy"


class HeDaoTao(str, Enum):
    CHINH_QUY = "ChinhQuy"
    KHONG_CHINH_QUY = "KhongChinhQuy"
    VUA_HOC_VUA_LAM = "VuaHocVuaLam"


class GioiTinh(str, Enum):
    NAM = "Nam"
    NU = "Nu"
    KHAC = "Khac"


class TrangThaiHoiDong(str, Enum):
    CHUA_THANH_LAP = "ChuaThanhLap"
    DA_THANH_LAP = "DaThanhLap"
    DANG_HOAT_DONG = "DangHoatDong"
    DA_KET_THUC = "DaKetThuc"
    HUY = "Huy"


class TrangThaiThuLao(str, Enum):
    CHUA_CHI_TRA = "ChuaChiTra"
    DA_CHI_TRA = "DaChiTra"
    HUY = "Huy"


class VaiTroPhanCong(str, Enum):
    GIANG_VIEN_CHINH = "GiangVienChinh"
    TRO_GIANG = "TroGiang"
    GIANG_VIEN_PHU_TRO = "GiangVienPhuTro"


class VaiTroThanhVienHD(str, Enum):
    CHU_TICH = "ChuTich"
    PHO_CHU_TICH = "PhoChuTich"
    THU_KY = "ThuKy"
    PHAN_BIEN_1 = "PhanBien1"
    PHAN_BIEN_2 = "PhanBien2"
    UY_VIEN = "UyVien"


class VaiTroTacGia(str, Enum):
    CHU_TRI = "ChuTri"
    DONG_TAC_GIA = "DongTacGia"
    HUONG_DAN = "HuongDan"
    THAM_GIA = "ThamGia"


class LoaiMonHocCTDT(str, Enum):
    BAT_BUOC = "BatBuoc"
    TU_CHON = "TuChon"
    CHUYEN_NGANH = "ChuyenNganh"
    CO_SO = "CoSo"


class LoaiThi(str, Enum):
    GIUA_KY = "Giuaky"
    CUOI_KY = "CuoiKy"
    THI_LAI = "ThiLai"
    THI_GIUA_KY = "ThiGiuaKy"


class HinhThucThi(str, Enum):
    VIET = "Viet"
    TRUC_TUYEN = "TrucTuyen"
    TRA_BAI = "TraBai"
    THUC_HANH = "ThucHanh"


class MucDoThongBao(str, Enum):
    BINH_THUONG = "BinhThuong"
    QUAN_TRONG = "QuanTrong"
    KHAN_CAP = "KhanCap"


class LoaiThongBao(str, Enum):
    CHUNG = "Chung"
    HOC_PHI = "HocPhi"
    LICH_THI = "LichThi"
    LUAN_VAN = "LuanVan"
    HOC_TAP = "HocTap"
    TUYEN_DUNG = "TuyenDung"


class LoaiQuyDinh(str, Enum):
    SO_TIN_CHI_TOI_THIEU = "SoTinChiToiThieu"
    SO_TIN_CHI_TOI_DA = "SoTinChiToiDa"
    YEU_CAU_BAI_BAO = "YeuCauBaiBao"
    THOI_GIAN_BAO_VE_TOI_DA = "ThoiGianBaoVeToiDa"
    THOI_GIAN_BAO_VE_TOI_THIEU = "ThoiGianBaoVeToiThieu"
    TY_LE_DAT_TOT_NGHIEP = "TyLeDatTotNghiep"
    LE_PHI_BAO_VE = "LePhiBaoVe"
    LE_PHI_HOC_PHI = "LePhiHocPhi"


class LoaiDiem(str, Enum):
    GIUA_KY = "Giuaky"
    CUOI_KY = "CuoiKy"
    TONG_KET = "TongKet"
    BAO_VE_LUAN_VAN = "BaoVeLuanVan"


class UserType(str, Enum):
    ADMIN = "admin"
    GIANG_VIEN = "giangvien"
    SINH_VIEN = "sinhvien"
    SYSTEM = "system"


class VaiTroAdmin(str, Enum):
    ADMIN = "admin"
    SUPER_ADMIN = "super_admin"
    KHOA = "khoa"
