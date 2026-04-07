-- ============================================================
-- PostgreSQL Schema - Quản lý Sinh viên Sau Đại học (v3.0 - Cải tiến)
-- ============================================================

-- ============================================================
-- 1. ENUM TYPES (giữ nguyên)
-- ============================================================
CREATE TYPE trang_thai_xet_tuyen AS ENUM ('ChoDuyet', 'DaDuyet', 'TuChoi');
CREATE TYPE trang_thai_hoc_phi AS ENUM ('ChuaDong', 'DaDong', 'DongMotPhan');
CREATE TYPE hoc_vi AS ENUM ('CuNhan', 'ThacSi', 'TienSi', 'PhoGiaoSu', 'GiaoSu');
CREATE TYPE hoc_ham AS ENUM ('GiangVien', 'PhoGiaoSu', 'GiaoSu');
CREATE TYPE xep_loai_tot_nghiep AS ENUM ('XuatSac', 'Gioi', 'Kha', 'TrungBinh', 'Yeu');
CREATE TYPE trang_thai_luan_van AS ENUM ('ChuaBaoVe', 'DangThucHien', 'DaBaoVe', 'CanChinhSua', 'TuChoi');
CREATE TYPE trang_thai_de_cuong AS ENUM ('Nhap', 'ChoDuyet', 'DaDuyet', 'CanChinhSua', 'TuChoi');
CREATE TYPE loai_cong_trinh AS ENUM ('BaiBao', 'SachChuyenKhao', 'DeTaiNCKH', 'HoiThao', 'Patent', 'Khac');
CREATE TYPE trang_thai_dang_ky AS ENUM ('ChoDuyet', 'DaDongHP', 'DaDuyet', 'Huy');
CREATE TYPE he_dao_tao AS ENUM ('ChinhQuy', 'KhongChinhQuy', 'VuaHocVuaLam');
CREATE TYPE gioi_tinh AS ENUM ('Nam', 'Nu', 'Khac');
CREATE TYPE trang_thai_hoi_dong AS ENUM ('ChuaThanhLap', 'DaThanhLap', 'DangHoatDong', 'DaKetThuc', 'Huy');
CREATE TYPE trang_thai_thu_lao AS ENUM ('ChuaChiTra', 'DaChiTra', 'Huy');

-- ============================================================
-- 2. BẢNG CƠ SỞ (giữ nguyên)
-- ============================================================
CREATE TABLE Khoa (
    MaKhoa     VARCHAR(5)   PRIMARY KEY,
    TenKhoa    VARCHAR(100) NOT NULL UNIQUE,
    DiaChi     VARCHAR(255),
    SDT        VARCHAR(11)  CHECK (SDT ~ '^\d{10,11}$'),
    Email      VARCHAR(100) CHECK (Email ~ '^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$'),
    is_active  BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

CREATE TABLE Nganh (
    MaNganh     VARCHAR(10)  PRIMARY KEY,
    TenNganh    VARCHAR(100) NOT NULL,
    MaKhoa      VARCHAR(5),
    MoTa        TEXT,
    is_active   BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at  TIMESTAMPTZ,
    FOREIGN KEY (MaKhoa) REFERENCES Khoa(MaKhoa)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE Lop (
    MaLop     VARCHAR(15)  PRIMARY KEY,
    TenLop    VARCHAR(100) NOT NULL UNIQUE,
    MaNganh   VARCHAR(10),
    SiSo      SMALLINT     CHECK (SiSo >= 0 AND SiSo <= 500),
    is_active BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaNganh) REFERENCES Nganh(MaNganh)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE MonHoc (
    MaMH       VARCHAR(10)  PRIMARY KEY,
    TenMH      VARCHAR(100) NOT NULL,
    SoTinChi   SMALLINT     NOT NULL CHECK (SoTinChi BETWEEN 1 AND 10),
    MoTa       TEXT,
    is_active  BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

CREATE TABLE HocKy (
    MaHK      VARCHAR(10)  PRIMARY KEY,
    TenHK     VARCHAR(50)  NOT NULL,
    NamHoc    VARCHAR(9)   NOT NULL CHECK (NamHoc ~ '^\d{4}-\d{4}$'),
    ThoiGianBD DATE        NOT NULL,
    ThoiGianKT DATE        NOT NULL,
    is_active  BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (ThoiGianKT > ThoiGianBD)
);

-- ============================================================
-- 3. QUẢN TRỊ VIÊN (giữ nguyên)
-- ============================================================
CREATE TABLE QuanTri (
    MaAdmin    VARCHAR(10)  PRIMARY KEY,
    TenDN      VARCHAR(50) NOT NULL UNIQUE,
    MatKhau    VARCHAR(255) NOT NULL,
    HoTen      VARCHAR(100) NOT NULL,
    Email      VARCHAR(100) NOT NULL UNIQUE
        CHECK (Email ~ '^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$'),
    SDT        VARCHAR(11)  CHECK (SDT ~ '^\d{10,11}$'),
    VaiTro     VARCHAR(20)  NOT NULL DEFAULT 'admin'
        CHECK (VaiTro IN ('admin', 'super_admin', 'khoa')),
    is_active  BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

-- ============================================================
-- 4. XÉT TUYỂN (giữ nguyên)
-- ============================================================
CREATE TABLE TK_XetTuyen (
    MaTK      VARCHAR(10) PRIMARY KEY,
    Email     VARCHAR(100) NOT NULL UNIQUE
        CHECK (Email ~ '^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$'),
    MatKhau   VARCHAR(255)  NOT NULL,
    is_active BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

CREATE TABLE HSO_XetTuyen (
    MaHSO          VARCHAR(10)  PRIMARY KEY,
    MaTK            VARCHAR(10),
    HoTen           VARCHAR(100) NOT NULL,
    GioiTinh    gioi_tinh,
    NgaySinh        DATE,
    CCCD            VARCHAR(12)  NOT NULL UNIQUE CHECK (CCCD ~ '^\d{12}$'),
    SDT             VARCHAR(11)  NOT NULL UNIQUE CHECK (SDT ~ '^\d{10,11}$'),
    Email           VARCHAR(100),
    DiaChi          VARCHAR(255),
    QueQuan         VARCHAR(100),
    NoiSinh         VARCHAR(100),
    DanToc          VARCHAR(50),
    TrinhDoNgoaiNgu VARCHAR(50) DEFAULT 'Không',
    BangTotNghiep   TEXT,
    FileCCCD        VARCHAR(500),
    FileBangDiem    VARCHAR(500),
    is_active       BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at       TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at       TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at       TIMESTAMPTZ,
    FOREIGN KEY (MaTK) REFERENCES TK_XetTuyen(MaTK)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE PT_XetTuyen (
    MaPTXT     VARCHAR(15)         PRIMARY KEY,
    MaNganh    VARCHAR(10),
    PhuongThuc VARCHAR(100)        NOT NULL,
    Diem       DECIMAL(4,2)        NOT NULL CHECK (Diem >= 0 AND Diem <= 10),
    TrangThai  trang_thai_xet_tuyen NOT NULL DEFAULT 'ChoDuyet',
    MaHSO      VARCHAR(10),
    MaAdmin    VARCHAR(10),
    NgayNop    TIMESTAMPTZ         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    NgayDuyet  TIMESTAMPTZ,
    GhiChu     TEXT,
    is_active  BOOLEAN             NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ         NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaAdmin) REFERENCES QuanTri(MaAdmin)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (MaHSO) REFERENCES HSO_XetTuyen(MaHSO)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaNganh) REFERENCES Nganh(MaNganh)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================================
-- 5. SINH VIÊN & GIẢNG VIÊN (SinhVien giữ nguyên, GiangVien giữ nguyên)
-- ============================================================
CREATE TABLE SinhVien (
    MaSV           VARCHAR(15)  PRIMARY KEY,
    HoTen          VARCHAR(100) NOT NULL,
    NgaySinh       DATE         NOT NULL,
    GioiTinh       gioi_tinh,
    Email          VARCHAR(100) NOT NULL UNIQUE
        CHECK (Email ~ '^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$'),
    MatKhau        VARCHAR(255)  NOT NULL,
    MaLop          VARCHAR(15),
    MaHSO          VARCHAR(10),
    MaTK           VARCHAR(10),
    HeDaoTao       he_dao_tao   NOT NULL DEFAULT 'ChinhQuy',
    QueQuan        VARCHAR(100),
    NoiSinh        VARCHAR(100),
    DanToc         VARCHAR(50),
    DiaChi         VARCHAR(255),
    SDT            VARCHAR(11)  CHECK (SDT ~ '^\d{10,11}$'),
    CCCD           VARCHAR(12)  UNIQUE CHECK (CCCD ~ '^\d{12}$'),
    BangTotNghiepURL VARCHAR(500),
    is_active      BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at     TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at     TIMESTAMPTZ,
    FOREIGN KEY (MaLop) REFERENCES Lop(MaLop)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (MaHSO) REFERENCES HSO_XetTuyen(MaHSO)
        ON DELETE SET NULL ON UPDATE CASCADE,
    FOREIGN KEY (MaTK) REFERENCES TK_XetTuyen(MaTK)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE GiangVien (
    MaGV            VARCHAR(15)  PRIMARY KEY,
    HoTen           VARCHAR(100) NOT NULL,
    Email           VARCHAR(100) NOT NULL UNIQUE
        CHECK (Email ~ '^[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}$'),
    SDT             VARCHAR(11)  CHECK (SDT ~ '^\d{10,11}$'),
    HocVi           hoc_vi,
    HocHam          hoc_ham,
    ChuyenNganh      VARCHAR(100),
    DiaChi          VARCHAR(255),
    MaKhoa          VARCHAR(5),
    MatKhau         VARCHAR(255)  NOT NULL,
    is_active       BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at      TIMESTAMPTZ,
    FOREIGN KEY (MaKhoa) REFERENCES Khoa(MaKhoa)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================================
-- 6. LỚP HỌC PHẦN (MỚI) - Cải tiến quan trọng
-- ============================================================
CREATE TABLE LopHocPhan (
    MaLopHP       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaMH          VARCHAR(10) NOT NULL,
    MaHK          VARCHAR(10) NOT NULL,
    MaGV          VARCHAR(15) NOT NULL,          -- Giảng viên chính
    TenNhom       VARCHAR(50),                   -- Ví dụ: "Nhóm 1", "Chiều thứ 2"
    SiSoToiDa     SMALLINT NOT NULL DEFAULT 50 CHECK (SiSoToiDa > 0),
    SiSoHienTai   SMALLINT NOT NULL DEFAULT 0 CHECK (SiSoHienTai >= 0),
    MoTa          TEXT,
    is_active     BOOLEAN NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at    TIMESTAMPTZ,
    FOREIGN KEY (MaMH) REFERENCES MonHoc(MaMH)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaHK) REFERENCES HocKy(MaHK)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaGV) REFERENCES GiangVien(MaGV)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    UNIQUE (MaMH, MaHK, TenNhom)  -- Mỗi môn trong một HK chỉ có một nhóm trùng tên
);

-- ============================================================
-- 7. ĐĂNG KÝ HỌC PHẦN (sửa: đăng ký theo LopHocPhan)
-- ============================================================
CREATE TABLE DangKyHocPhan (
    MaDK         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaSV         VARCHAR(15) NOT NULL,
    MaLopHP      BIGINT NOT NULL,
    TrangThai    trang_thai_dang_ky NOT NULL DEFAULT 'ChoDuyet',
    DuocMien     BOOLEAN DEFAULT FALSE,
    LyDoMien     TEXT,
    NgayDK       TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    NgayDuyet    TIMESTAMPTZ,
    NguoiDuyet   VARCHAR(10),
    is_active    BOOLEAN NOT NULL DEFAULT TRUE,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at   TIMESTAMPTZ,
    FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaLopHP) REFERENCES LopHocPhan(MaLopHP)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (NguoiDuyet) REFERENCES QuanTri(MaAdmin)
        ON DELETE SET NULL ON UPDATE CASCADE,
    UNIQUE (MaSV, MaLopHP)  -- Mỗi SV chỉ đăng ký một lần cho một lớp học phần
);

-- Trigger cập nhật sĩ số hiện tại của LopHocPhan khi đăng ký (khi duyệt)
CREATE OR REPLACE FUNCTION fn_update_siso_lophp()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' AND NEW.TrangThai = 'DaDuyet' THEN
        UPDATE LopHocPhan SET SiSoHienTai = SiSoHienTai + 1
        WHERE MaLopHP = NEW.MaLopHP;
    ELSIF TG_OP = 'UPDATE' AND OLD.TrangThai != 'DaDuyet' AND NEW.TrangThai = 'DaDuyet' THEN
        UPDATE LopHocPhan SET SiSoHienTai = SiSoHienTai + 1
        WHERE MaLopHP = NEW.MaLopHP;
    ELSIF TG_OP = 'UPDATE' AND OLD.TrangThai = 'DaDuyet' AND NEW.TrangThai != 'DaDuyet' THEN
        UPDATE LopHocPhan SET SiSoHienTai = SiSoHienTai - 1
        WHERE MaLopHP = NEW.MaLopHP;
    ELSIF TG_OP = 'DELETE' AND OLD.TrangThai = 'DaDuyet' THEN
        UPDATE LopHocPhan SET SiSoHienTai = SiSoHienTai - 1
        WHERE MaLopHP = OLD.MaLopHP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_dangky_siso
    AFTER INSERT OR UPDATE OF TrangThai OR DELETE ON DangKyHocPhan
    FOR EACH ROW EXECUTE FUNCTION fn_update_siso_lophp();

-- ============================================================
-- 8. PHÂN CÔNG GIẢNG DẠY (cập nhật: liên kết với LopHocPhan, có thể có nhiều GV cho một lớp)
-- ============================================================
CREATE TABLE PhanCongGiangDay (
    MaPC       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaLopHP    BIGINT NOT NULL,
    MaGV       VARCHAR(15) NOT NULL,
    VaiTro     VARCHAR(30) DEFAULT 'GiangVienChinh' CHECK (VaiTro IN ('GiangVienChinh', 'TroGiang', 'GiangVienPhuTro')),
    SoTiet     SMALLINT CHECK (SoTiet > 0 AND SoTiet <= 200),
    is_active  BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaLopHP) REFERENCES LopHocPhan(MaLopHP)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaGV) REFERENCES GiangVien(MaGV)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (MaLopHP, MaGV)  -- Mỗi GV chỉ phân công một lần cho một lớp học phần
);

-- ============================================================
-- 9. LỊCH HỌC (sửa: liên kết với PhanCongGiangDay, sửa UNIQUE, thêm kiểm tra xung đột)
-- ============================================================
CREATE OR REPLACE FUNCTION fn_lichhoc_check_conflict()
RETURNS TRIGGER AS $$
DECLARE
    gv_id VARCHAR(15);
    hk_id VARCHAR(10);
BEGIN
    -- Lấy MaGV và MaHK từ PhanCongGiangDay và LopHocPhan
    SELECT pc.MaGV, lhp.MaHK INTO gv_id, hk_id
    FROM PhanCongGiangDay pc
    JOIN LopHocPhan lhp ON pc.MaLopHP = lhp.MaLopHP
    WHERE pc.MaPC = NEW.MaPC;

    -- Kiểm tra xung đột phòng học
    IF EXISTS (
        SELECT 1 FROM LichHoc lh
        JOIN PhanCongGiangDay pc2 ON lh.MaPC = pc2.MaPC
        JOIN LopHocPhan lhp2 ON pc2.MaLopHP = lhp2.MaLopHP
        WHERE lh.PhongHoc = NEW.PhongHoc
          AND lh.Thu = NEW.Thu
          AND lh.Buoi = NEW.Buoi
          AND lh.MaPC != NEW.MaPC
          AND lhp2.MaHK = hk_id
          AND (NEW.TietBatDau BETWEEN lh.TietBatDau AND lh.TietBatDau + lh.SoTiet - 1
               OR lh.TietBatDau BETWEEN NEW.TietBatDau AND NEW.TietBatDau + NEW.SoTiet - 1)
    ) THEN
        RAISE EXCEPTION 'Phòng % đã có lịch vào thứ %, buổi %, tiết % trong học kỳ này!',
            NEW.PhongHoc, NEW.Thu, NEW.Buoi, NEW.TietBatDau;
    END IF;

    -- Kiểm tra xung đột lịch của giảng viên
    IF EXISTS (
        SELECT 1 FROM LichHoc lh
        JOIN PhanCongGiangDay pc2 ON lh.MaPC = pc2.MaPC
        WHERE pc2.MaGV = gv_id
          AND lh.Thu = NEW.Thu
          AND lh.Buoi = NEW.Buoi
          AND lh.MaPC != NEW.MaPC
          AND (NEW.TietBatDau BETWEEN lh.TietBatDau AND lh.TietBatDau + lh.SoTiet - 1
               OR lh.TietBatDau BETWEEN NEW.TietBatDau AND NEW.TietBatDau + NEW.SoTiet - 1)
    ) THEN
        RAISE EXCEPTION 'Giảng viên % đã có lịch dạy vào thứ %, buổi %, tiết %!',
            gv_id, NEW.Thu, NEW.Buoi, NEW.TietBatDau;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE LichHoc (
    MaLH        BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaPC        BIGINT NOT NULL,
    Thu         SMALLINT CHECK (Thu BETWEEN 2 AND 8),  -- 2=Thứ 2, 8=Chủ nhật
    TietBatDau  SMALLINT CHECK (TietBatDau BETWEEN 1 AND 15),
    SoTiet      SMALLINT CHECK (SoTiet BETWEEN 1 AND 6),
    Buoi        VARCHAR(10) CHECK (Buoi IN ('Sang', 'Chieu', 'Toi')),
    PhongHoc    VARCHAR(50),
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at  TIMESTAMPTZ,
    FOREIGN KEY (MaPC) REFERENCES PhanCongGiangDay(MaPC)
        ON DELETE CASCADE ON UPDATE CASCADE
    -- Bỏ UNIQUE (MaPC, Thu, Buoi) để cho phép một lớp học nhiều buổi
);

CREATE TRIGGER trg_lichhoc_check_conflict
    BEFORE INSERT OR UPDATE ON LichHoc
    FOR EACH ROW EXECUTE FUNCTION fn_lichhoc_check_conflict();

-- ============================================================
-- 10. KẾT QUẢ HỌC TẬP (thêm trigger quy đổi điểm, sửa kiểm tra đăng ký thành EXCEPTION)
-- ============================================================
CREATE OR REPLACE FUNCTION fn_quy_doi_diem()
RETURNS TRIGGER AS $$
BEGIN
    -- Quy đổi thang 4 và điểm chữ theo thang điểm 10
    NEW.DiemHe4 := CASE
        WHEN NEW.Diem >= 8.5 THEN 4.0
        WHEN NEW.Diem >= 7.0 THEN 3.0
        WHEN NEW.Diem >= 5.5 THEN 2.0
        WHEN NEW.Diem >= 4.0 THEN 1.0
        ELSE 0.0
    END;
    NEW.DiemChu := CASE
        WHEN NEW.Diem >= 8.5 THEN 'A'
        WHEN NEW.Diem >= 7.0 THEN 'B'
        WHEN NEW.Diem >= 5.5 THEN 'C'
        WHEN NEW.Diem >= 4.0 THEN 'D'
        ELSE 'F'
    END;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_check_dangky_truockhi_nhapdiem()
RETURNS TRIGGER AS $$
DECLARE
    lop_hp_id BIGINT;
BEGIN
    -- Tìm MaLopHP từ MaMH, MaHK (cần xác định lớp học phần nào SV đã đăng ký)
    -- Giả sử điểm được nhập với MaMH và MaHK, cần tìm lớp học phần tương ứng
    -- Nếu có nhiều lớp, cần logic phức tạp hơn. Ở đây lấy bất kỳ lớp hợp lệ.
    SELECT lhp.MaLopHP INTO lop_hp_id
    FROM LopHocPhan lhp
    WHERE lhp.MaMH = NEW.MaMH AND lhp.MaHK = NEW.MaHK
    LIMIT 1;

    IF NOT EXISTS (
        SELECT 1 FROM DangKyHocPhan dk
        WHERE dk.MaSV = NEW.MaSV
          AND dk.MaLopHP = lop_hp_id
          AND dk.is_active = TRUE
          AND dk.TrangThai IN ('DaDuyet', 'DaDongHP')
    ) THEN
        RAISE EXCEPTION 'Sinh viên % chưa đăng ký hoặc chưa được duyệt học phần % trong học kỳ %',
            NEW.MaSV, NEW.MaMH, NEW.MaHK;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE KQ_HocTap (
    MaSV      VARCHAR(15),
    MaMH      VARCHAR(10),
    MaHK      VARCHAR(10),
    Diem      DECIMAL(4,2) NOT NULL CHECK (Diem >= 0 AND Diem <= 10),
    LoaiDiem  VARCHAR(20)   DEFAULT 'Thi'
        CHECK (LoaiDiem IN ('Giuaky', 'CuoiKy', 'TongKet', 'BaoVeLuanVan')),
    DiemHe4   DECIMAL(3,2) CHECK (DiemHe4 IS NULL OR (DiemHe4 >= 0 AND DiemHe4 <= 4.0)),
    DiemChu   VARCHAR(2)   CHECK (DiemChu IS NULL OR DiemChu IN ('A+','A','B+','B','C+','C','D+','D','F')),
    GhiChu    TEXT,
    is_active BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (MaSV, MaMH, MaHK),
    FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaMH) REFERENCES MonHoc(MaMH)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaHK) REFERENCES HocKy(MaHK)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TRIGGER trg_kqhoctap_quy_doi
    BEFORE INSERT OR UPDATE OF Diem ON KQ_HocTap
    FOR EACH ROW EXECUTE FUNCTION fn_quy_doi_diem();

CREATE TRIGGER trg_kqhoctap_check_dangky
    BEFORE INSERT OR UPDATE ON KQ_HocTap
    FOR EACH ROW EXECUTE FUNCTION fn_check_dangky_truockhi_nhapdiem();

-- ============================================================
-- 11. LUẬN VĂN / LUẬN ÁN (giữ nguyên, thêm khóa ngoại cho NguoiDuyet)
-- ============================================================
CREATE TABLE LuanVan (
    MaLV          VARCHAR(15)                PRIMARY KEY,
    MaSV          VARCHAR(15)                 NOT NULL UNIQUE,
    MaGV          VARCHAR(15),
    TenDeTai      VARCHAR(255)                NOT NULL,
    NgayDangKy    DATE,
    NgayBaoVe     DATE,
    TrangThai     trang_thai_luan_van         NOT NULL DEFAULT 'ChuaBaoVe',
    DiemBaoVe     DECIMAL(4,2) CHECK (DiemBaoVe IS NULL OR (DiemBaoVe >= 0 AND DiemBaoVe <= 10)),
    DiemHe4       DECIMAL(3,2) CHECK (DiemHe4 IS NULL OR (DiemHe4 >= 0 AND DiemHe4 <= 4.0)),
    DiemChu       VARCHAR(2) CHECK (DiemChu IS NULL OR DiemChu IN ('A+','A','B+','B','C+','C','D+','D','F')),
    GhiChu        TEXT,
    is_active     BOOLEAN                     NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ                  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMPTZ                  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at    TIMESTAMPTZ,
    CHECK (NgayBaoVe IS NULL OR NgayBaoVe >= NgayDangKy),
    FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaGV) REFERENCES GiangVien(MaGV)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE DeCuongLuanAn (
    MaDC         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaLV         VARCHAR(15)                    NOT NULL,
    MaSV         VARCHAR(15)                    NOT NULL,
    PhienBan     SMALLINT                       NOT NULL DEFAULT 1,
    TieuDe       VARCHAR(255)                   NOT NULL,
    TomTat       TEXT,
    NoiDung      TEXT,
    FileDeCuong  VARCHAR(500),
    TrangThai    trang_thai_de_cuong           NOT NULL DEFAULT 'Nhap',
    NgayNop      TIMESTAMPTZ                   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    NgayDuyet    TIMESTAMPTZ,
    NguoiDuyet   VARCHAR(10),
    BinhLuan     TEXT,
    is_active    BOOLEAN                        NOT NULL DEFAULT TRUE,
    created_at   TIMESTAMPTZ                    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMPTZ                    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at   TIMESTAMPTZ,
    FOREIGN KEY (MaLV) REFERENCES LuanVan(MaLV)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (NguoiDuyet) REFERENCES QuanTri(MaAdmin)   -- ĐÃ SỬA: thêm khóa ngoại
        ON DELETE SET NULL ON UPDATE CASCADE,
    UNIQUE (MaLV, PhienBan)
);

-- ============================================================
-- 12. HỌC PHÍ (thêm bảng DonGiaTinChi, giữ nguyên HocPhi nhưng có thể tính tự động)
-- ============================================================
CREATE TABLE DonGiaTinChi (
    MaDonGia   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    NamHoc     VARCHAR(9) NOT NULL CHECK (NamHoc ~ '^\d{4}-\d{4}$'),
    HeDaoTao   he_dao_tao NOT NULL,
    MaNganh    VARCHAR(10),   -- NULL nếu áp dụng cho tất cả ngành
    DonGia     DECIMAL(12,0) NOT NULL CHECK (DonGia > 0),  -- VND/tín chỉ
    is_active  BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaNganh) REFERENCES Nganh(MaNganh)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- Bảng HocPhi vẫn giữ, nhưng có thể trigger tính số tiền từ đơn giá và số tín chỉ đăng ký
CREATE TABLE HocPhi (
    MaHP        BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaSV        VARCHAR(15) NOT NULL,
    MaHK        VARCHAR(10) NOT NULL,
    SoTien      DECIMAL(15,0) NOT NULL CHECK (SoTien > 0 AND SoTien <= 1000000000),
    TrangThai   trang_thai_hoc_phi NOT NULL DEFAULT 'ChuaDong',
    NgayHanNop  DATE,
    NgayDong    TIMESTAMPTZ,
    MaGiaoDich  VARCHAR(100),
    GhiChu      TEXT,
    is_active   BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at  TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at  TIMESTAMPTZ,
    UNIQUE (MaSV, MaHK),
    FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaHK) REFERENCES HocKy(MaHK)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

-- Trigger tính học phí tự động dựa trên số tín chỉ đăng ký (khi duyệt đăng ký)
CREATE OR REPLACE FUNCTION fn_tinh_hoc_phi()
RETURNS TRIGGER AS $$
DECLARE
    so_tin_chi INT;
    don_gia DECIMAL(12,0);
    tong_tien DECIMAL(15,0);
    hk_row RECORD;
    sv_row RECORD;
BEGIN
    IF NEW.TrangThai = 'DaDuyet' AND OLD.TrangThai != 'DaDuyet' THEN
        -- Lấy số tín chỉ của môn học từ LopHocPhan
        SELECT mh.SoTinChi INTO so_tin_chi
        FROM LopHocPhan lhp
        JOIN MonHoc mh ON lhp.MaMH = mh.MaMH
        WHERE lhp.MaLopHP = NEW.MaLopHP;
        
        -- Lấy thông tin học kỳ và sinh viên
        SELECT lhp.MaHK, sv.MaSV, sv.HeDaoTao, sv.MaLop, l.MaNganh
        INTO hk_row, sv_row
        FROM LopHocPhan lhp
        JOIN SinhVien sv ON sv.MaSV = NEW.MaSV
        JOIN Lop l ON sv.MaLop = l.MaLop
        WHERE lhp.MaLopHP = NEW.MaLopHP;
        
        -- Lấy đơn giá phù hợp
        SELECT dg.DonGia INTO don_gia
        FROM DonGiaTinChi dg
        WHERE dg.NamHoc = (SELECT NamHoc FROM HocKy WHERE MaHK = hk_row.MaHK)
          AND dg.HeDaoTao = sv_row.HeDaoTao
          AND (dg.MaNganh = sv_row.MaNganh OR dg.MaNganh IS NULL)
          AND dg.is_active = TRUE
        ORDER BY dg.MaNganh NULLS LAST
        LIMIT 1;
        
        IF don_gia IS NULL THEN
            RAISE EXCEPTION 'Chưa có đơn giá học phí cho học kỳ %', hk_row.MaHK;
        END IF;
        
        tong_tien := so_tin_chi * don_gia;
        
        -- Cập nhật hoặc chèn vào HocPhi
        INSERT INTO HocPhi (MaSV, MaHK, SoTien, TrangThai, NgayHanNop)
        VALUES (NEW.MaSV, hk_row.MaHK, tong_tien, 'ChuaDong', 
                (SELECT ThoiGianKT + INTERVAL '15 days' FROM HocKy WHERE MaHK = hk_row.MaHK))
        ON CONFLICT (MaSV, MaHK) DO UPDATE
        SET SoTien = EXCLUDED.SoTien, updated_at = CURRENT_TIMESTAMP;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_dangky_tinh_hocphi
    AFTER UPDATE OF TrangThai ON DangKyHocPhan
    FOR EACH ROW
    WHEN (NEW.TrangThai = 'DaDuyet' AND OLD.TrangThai != 'DaDuyet')
    EXECUTE FUNCTION fn_tinh_hoc_phi();

-- ============================================================
-- 13. TỐT NGHIỆP (giữ nguyên)
-- ============================================================
CREATE TABLE TotNghiep (
    MaSV          VARCHAR(15) PRIMARY KEY,
    GPA           DECIMAL(4,2) NOT NULL CHECK (GPA >= 0 AND GPA <= 4.0),
    TongTinChi    SMALLINT     NOT NULL DEFAULT 0 CHECK (TongTinChi >= 0),
    XepLoai       xep_loai_tot_nghiep NOT NULL,
    NgayTotNghiep DATE,
    SoHieuBang    VARCHAR(50)  UNIQUE,
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMPTZ  NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at    TIMESTAMPTZ,
    FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 14. THÔNG BÁO (giữ nguyên)
-- ============================================================
CREATE TABLE ThongBao (
    MaTB     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    TieuDe   VARCHAR(255) NOT NULL,
    NoiDung  TEXT        NOT NULL,
    LoaiTB   VARCHAR(30) DEFAULT 'Chung'
        CHECK (LoaiTB IN ('Chung', 'HocPhi', 'LichThi', 'LuanVan', 'HocTap', 'TuyenDung')),
    MucDo    VARCHAR(10) DEFAULT 'BinhThuong'
        CHECK (MucDo IN ('BinhThuong', 'QuanTrong', 'KhanCap')),
    MaAdmin  VARCHAR(10),
    is_active BOOLEAN    NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaAdmin) REFERENCES QuanTri(MaAdmin)
        ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TABLE TB_NguoiNhan (
    MaTBNN     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaTB       BIGINT,
    MaSV       VARCHAR(15),
    MaGV       VARCHAR(15),
    TrangThaiDoc BOOLEAN DEFAULT FALSE,
    ThoiGianDoc  TIMESTAMPTZ,
    is_active   BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at   TIMESTAMPTZ,
    FOREIGN KEY (MaTB) REFERENCES ThongBao(MaTB)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaGV) REFERENCES GiangVien(MaGV)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 15. NGHIÊN CỨU KHOA HỌC (giữ nguyên)
-- ============================================================
CREATE TABLE NghienCuuKhoaHoc (
    MaNCKH   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    TenCongTrinh VARCHAR(255) NOT NULL,
    LoaiCongTrinh loai_cong_trinh NOT NULL,
    MoTa     TEXT,
    Cap      VARCHAR(20) DEFAULT 'Truong'
        CHECK (Cap IN ('Truong', 'Bo', 'QuocTe')),
    Nam      SMALLINT   NOT NULL CHECK (Nam BETWEEN 2000 AND 2100),
    Link     VARCHAR(500),
    FileMinhChung VARCHAR(500),
    is_active BOOLEAN   NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

CREATE TABLE TacGiaCongTrinh (
    MaTacGia BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaNCKH   BIGINT NOT NULL,
    MaGV     VARCHAR(15),
    MaSV     VARCHAR(15),
    VaiTro   VARCHAR(30) NOT NULL DEFAULT 'DongTacGia'
        CHECK (VaiTro IN ('ChuTri', 'DongTacGia', 'HuongDan', 'ThamGia')),
    ThuTu    SMALLINT DEFAULT 1 CHECK (ThuTu >= 1),
    is_active BOOLEAN   NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaNCKH) REFERENCES NghienCuuKhoaHoc(MaNCKH)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaGV) REFERENCES GiangVien(MaGV)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaSV) REFERENCES SinhVien(MaSV)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (MaGV IS NOT NULL OR MaSV IS NOT NULL),
    UNIQUE (MaNCKH, MaGV, MaSV)
);

-- ============================================================
-- 16. QUY ĐỊNH ĐẶC THÙ (giữ nguyên)
-- ============================================================
CREATE TABLE QuyDinhDacThu (
    MaQD    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    TenQD   VARCHAR(200) NOT NULL,
    MoTa    TEXT,
    MaNganh VARCHAR(10),
    KhoaTuyen VARCHAR(9) CHECK (KhoaTuyen IS NULL OR KhoaTuyen ~ '^\d{4}-\d{4}$'),
    LoaiQuyDinh VARCHAR(30) NOT NULL
        CHECK (LoaiQuyDinh IN (
            'SoTinChiToiThieu', 'SoTinChiToiDa',
            'YeuCauBaiBao', 'ThoiGianBaoVeToiDa',
            'ThoiGianBaoVeToiThieu', 'TyLeDatTotNghiep',
            'LePhiBaoVe', 'LePhiHocPhi'
        )),
    GiaTri    DECIMAL(10,2) NOT NULL,
    DonVi     VARCHAR(30),
    BatBuoc   BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaNganh) REFERENCES Nganh(MaNganh)
        ON DELETE SET NULL ON UPDATE CASCADE
);

-- ============================================================
-- 17. HỘI ĐỒNG BẢO VỆ (giữ nguyên)
-- ============================================================
CREATE TABLE HoiDongBaoVe (
    MaHD      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaLV      VARCHAR(15) NOT NULL UNIQUE,
    TenHD     VARCHAR(200),
    NgayThanhLap DATE,
    NgayBaoVe DATE,
    DiaDiem   VARCHAR(200),
    TrangThai trang_thai_hoi_dong NOT NULL DEFAULT 'ChuaThanhLap',
    GhiChu    TEXT,
    is_active BOOLEAN    NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaLV) REFERENCES LuanVan(MaLV)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE ThanhVienHoiDong (
    MaTVHD  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaHD    BIGINT NOT NULL,
    MaGV    VARCHAR(15) NOT NULL,
    VaiTro  VARCHAR(30) NOT NULL
        CHECK (VaiTro IN ('ChuTich', 'PhoChuTich', 'ThuKy', 'PhanBien1', 'PhanBien2', 'UyVien')),
    DiemDanhGia DECIMAL(4,2) CHECK (DiemDanhGia IS NULL OR (DiemDanhGia >= 0 AND DiemDanhGia <= 10)),
    NhanXet   TEXT,
    is_active BOOLEAN    NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaHD) REFERENCES HoiDongBaoVe(MaHD)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaGV) REFERENCES GiangVien(MaGV)
        ON DELETE RESTRICT ON UPDATE CASCADE,
    UNIQUE (MaHD, MaGV)
);

CREATE TABLE ThuLaoHoiDong (
    MaTL     BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaTVHD   BIGINT NOT NULL,
    MaHD     BIGINT NOT NULL,
    SoTien   DECIMAL(12,0) NOT NULL CHECK (SoTien >= 0),
    TrangThai trang_thai_thu_lao NOT NULL DEFAULT 'ChuaChiTra',
    NgayChiTra TIMESTAMPTZ,
    MaGiaoDich VARCHAR(100),
    GhiChu   TEXT,
    is_active BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaTVHD) REFERENCES ThanhVienHoiDong(MaTVHD)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaHD) REFERENCES HoiDongBaoVe(MaHD)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (MaTVHD, MaHD)
);

-- ============================================================
-- 18. MÔN HỌC TIÊN QUYẾT (thêm trigger updated_at)
-- ============================================================
CREATE TABLE MonHocTienQuyet (
    MaMH           VARCHAR(10) NOT NULL,
    MaMHTienQuyet  VARCHAR(10) NOT NULL,
    MoTa           TEXT,
    is_active      BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at     TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at     TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (MaMH, MaMHTienQuyet),
    FOREIGN KEY (MaMH) REFERENCES MonHoc(MaMH)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaMHTienQuyet) REFERENCES MonHoc(MaMH)
        ON DELETE CASCADE ON UPDATE CASCADE,
    CHECK (MaMH != MaMHTienQuyet)
);

CREATE TRIGGER trg_mhtq_updated_at
    BEFORE UPDATE ON MonHocTienQuyet
    FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();

-- ============================================================
-- 19. CHƯƠNG TRÌNH ĐÀO TẠO (giữ nguyên)
-- ============================================================
CREATE TABLE ChuongTrinhDaoTao (
    MaCTDT    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaNganh   VARCHAR(10) NOT NULL,
    MaMH      VARCHAR(10) NOT NULL,
    HocKy     SMALLINT   CHECK (HocKy >= 1 AND HocKy <= 20),
    LoaiMH    VARCHAR(20) DEFAULT 'BatBuoc'
        CHECK (LoaiMH IN ('BatBuoc', 'TuChon', 'ChuyenNganh', 'CoSo')),
    is_active BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaNganh) REFERENCES Nganh(MaNganh)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaMH) REFERENCES MonHoc(MaMH)
        ON DELETE CASCADE ON UPDATE CASCADE,
    UNIQUE (MaNganh, MaMH)
);

-- ============================================================
-- 20. LỊCH THI (giữ nguyên)
-- ============================================================
CREATE TABLE LichThi (
    MaLT      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    MaMH      VARCHAR(10) NOT NULL,
    MaHK      VARCHAR(10) NOT NULL,
    LoaiThi   VARCHAR(20) DEFAULT 'CuoiKy'
        CHECK (LoaiThi IN ('Giuaky', 'CuoiKy', 'ThiLai', 'ThiGiuaKy')),
    NgayThi   DATE        NOT NULL,
    GioThi    TIME        NOT NULL,
    ThoiLuong SMALLINT    CHECK (ThoiLuong > 0 AND ThoiLuong <= 300),
    DiaDiem   VARCHAR(200),
    HinhThuc  VARCHAR(30) DEFAULT 'Viet'
        CHECK (HinhThuc IN ('Viet', 'TrucTuyen', 'TraBai', 'ThucHanh')),
    GhiChu    TEXT,
    is_active BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ,
    FOREIGN KEY (MaMH) REFERENCES MonHoc(MaMH)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (MaHK) REFERENCES HocKy(MaHK)
        ON DELETE CASCADE ON UPDATE CASCADE
);

-- ============================================================
-- 21. TRIGGER updated_at (hàm tổng quát)
-- ============================================================
CREATE OR REPLACE FUNCTION fn_update_updated_at() RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Áp dụng trigger cho các bảng (liệt kê đầy đủ)
CREATE TRIGGER trg_sinhvien_updated_at BEFORE UPDATE ON SinhVien FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_luanvan_updated_at BEFORE UPDATE ON LuanVan FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_kqhoctap_updated_at BEFORE UPDATE ON KQ_HocTap FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_hocphi_updated_at BEFORE UPDATE ON HocPhi FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_khoa_updated_at BEFORE UPDATE ON Khoa FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_nganh_updated_at BEFORE UPDATE ON Nganh FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_lop_updated_at BEFORE UPDATE ON Lop FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_monhoc_updated_at BEFORE UPDATE ON MonHoc FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_hocky_updated_at BEFORE UPDATE ON HocKy FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_giangvien_updated_at BEFORE UPDATE ON GiangVien FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_quantri_updated_at BEFORE UPDATE ON QuanTri FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_tkxettuyen_updated_at BEFORE UPDATE ON TK_XetTuyen FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_hsoxettuyen_updated_at BEFORE UPDATE ON HSO_XetTuyen FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_ptxettuyen_updated_at BEFORE UPDATE ON PT_XetTuyen FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_decuong_updated_at BEFORE UPDATE ON DeCuongLuanAn FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_thongbao_updated_at BEFORE UPDATE ON ThongBao FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_tbnguoinhan_updated_at BEFORE UPDATE ON TB_NguoiNhan FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_dangky_updated_at BEFORE UPDATE ON DangKyHocPhan FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_phancong_updated_at BEFORE UPDATE ON PhanCongGiangDay FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_nghiencuu_updated_at BEFORE UPDATE ON NghienCuuKhoaHoc FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_quydinh_updated_at BEFORE UPDATE ON QuyDinhDacThu FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_hoi_dong_updated_at BEFORE UPDATE ON HoiDongBaoVe FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_tvhd_updated_at BEFORE UPDATE ON ThanhVienHoiDong FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_thulao_updated_at BEFORE UPDATE ON ThuLaoHoiDong FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_totnghiep_updated_at BEFORE UPDATE ON TotNghiep FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_lophp_updated_at BEFORE UPDATE ON LopHocPhan FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_lichhoc_updated_at BEFORE UPDATE ON LichHoc FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_dongia_updated_at BEFORE UPDATE ON DonGiaTinChi FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_ctdt_updated_at BEFORE UPDATE ON ChuongTrinhDaoTao FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();
CREATE TRIGGER trg_lichthi_updated_at BEFORE UPDATE ON LichThi FOR EACH ROW EXECUTE FUNCTION fn_update_updated_at();

-- ============================================================
-- 22. VIEWS (cập nhật theo cấu trúc mới)
-- ============================================================
-- VIEW: Tổng tín chỉ tích lũy (dùng KQ_HocTap và MonHoc)
CREATE OR REPLACE VIEW v_SinhVien_TongTinChi AS
WITH diem_tot_nhat AS (
    SELECT DISTINCT ON (kq.MaSV, kq.MaMH)
        kq.MaSV,
        kq.MaMH,
        kq.Diem
    FROM KQ_HocTap kq
    WHERE kq.is_active = TRUE
      AND kq.Diem >= 5.0
    ORDER BY kq.MaSV, kq.MaMH, kq.Diem DESC
)
SELECT
    sv.MaSV,
    sv.HoTen,
    COALESCE(SUM(mh.SoTinChi), 0) AS TongTinChiTL
FROM SinhVien sv
LEFT JOIN diem_tot_nhat dn ON sv.MaSV = dn.MaSV
LEFT JOIN MonHoc mh ON dn.MaMH = mh.MaMH AND mh.is_active = TRUE
WHERE sv.is_active = TRUE
GROUP BY sv.MaSV, sv.HoTen;

-- VIEW: GPA tích lũy
CREATE OR REPLACE VIEW v_SinhVien_GPA AS
WITH diem_tot_nhat AS (
    SELECT DISTINCT ON (kq.MaSV, kq.MaMH)
        kq.MaSV,
        kq.MaMH,
        kq.DiemHe4
    FROM KQ_HocTap kq
    WHERE kq.is_active = TRUE
      AND kq.DiemHe4 IS NOT NULL
    ORDER BY kq.MaSV, kq.MaMH, kq.DiemHe4 DESC
)
SELECT
    sv.MaSV,
    sv.HoTen,
    CASE
        WHEN SUM(mh.SoTinChi) = 0 THEN NULL
        ELSE ROUND(SUM(dn.DiemHe4 * mh.SoTinChi) / SUM(mh.SoTinChi), 2)
    END AS GPA,
    SUM(mh.SoTinChi) AS TongTinChi
FROM SinhVien sv
LEFT JOIN diem_tot_nhat dn ON sv.MaSV = dn.MaSV
LEFT JOIN MonHoc mh ON dn.MaMH = mh.MaMH AND mh.is_active = TRUE
WHERE sv.is_active = TRUE
GROUP BY sv.MaSV, sv.HoTen;

-- ============================================================
-- 23. TRIGGER KIỂM TRA MÔN TIÊN QUYẾT (khi đăng ký học phần)
-- ============================================================
CREATE OR REPLACE FUNCTION fn_check_tienquyet()
RETURNS TRIGGER AS $$
DECLARE
    mh_id VARCHAR(10);
BEGIN
    -- Lấy mã môn học từ lớp học phần
    SELECT MaMH INTO mh_id
    FROM LopHocPhan
    WHERE MaLopHP = NEW.MaLopHP;

    IF EXISTS (
        SELECT 1 FROM MonHocTienQuyet tq
        WHERE tq.MaMH = mh_id
          AND NOT EXISTS (
              SELECT 1 FROM KQ_HocTap kq
              WHERE kq.MaSV = NEW.MaSV
                AND kq.MaMH = tq.MaMHTienQuyet
                AND kq.Diem >= 5.0
                AND kq.is_active = TRUE
          )
    ) THEN
        RAISE EXCEPTION 'Sinh viên % chưa hoàn thành môn tiên quyết của môn %', NEW.MaSV, mh_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_dangky_check_tienquyet
    BEFORE INSERT OR UPDATE OF MaLopHP ON DangKyHocPhan
    FOR EACH ROW
    EXECUTE FUNCTION fn_check_tienquyet();

-- ============================================================
-- 24. INDEXES (bổ sung composite is_active, deleted_at)
-- ============================================================
-- Indexes gốc giữ nguyên, thêm các index mới
CREATE INDEX idx_sinhvien_malop    ON SinhVien(MaLop);
CREATE INDEX idx_sinhvien_email    ON SinhVien(Email);
CREATE INDEX idx_sinhvien_active_deleted ON SinhVien(is_active, deleted_at) WHERE is_active = TRUE;

CREATE INDEX idx_kqhoctap_masv     ON KQ_HocTap(MaSV);
CREATE INDEX idx_kqhoctap_mamh     ON KQ_HocTap(MaMH);
CREATE INDEX idx_kqhoctap_mahk     ON KQ_HocTap(MaHK);
CREATE INDEX idx_kqhoctap_sv_hk    ON KQ_HocTap(MaSV, MaHK);

CREATE INDEX idx_ptxettuyen_trangthai ON PT_XetTuyen(TrangThai);
CREATE INDEX idx_ptxettuyen_mahso     ON PT_XetTuyen(MaHSO);
CREATE INDEX idx_ptxettuyen_manganh   ON PT_XetTuyen(MaNganh);

CREATE INDEX idx_thongbao_createdat ON ThongBao(created_at DESC);
CREATE INDEX idx_thongbao_loai      ON ThongBao(LoaiTB);

CREATE INDEX idx_tbnguoinhan_masv   ON TB_NguoiNhan(MaSV);
CREATE INDEX idx_tbnguoinhan_matb   ON TB_NguoiNhan(MaTB);

CREATE INDEX idx_luanvan_magv   ON LuanVan(MaGV);
CREATE INDEX idx_luanvan_masv   ON LuanVan(MaSV);

CREATE INDEX idx_hocphi_masv    ON HocPhi(MaSV);
CREATE INDEX idx_hocphi_mahk    ON HocPhi(MaHK);

CREATE INDEX idx_hso_cccd       ON HSO_XetTuyen(CCCD);
CREATE INDEX idx_giangvien_makhoa ON GiangVien(MaKhoa);
CREATE INDEX idx_nganh_makhoa   ON Nganh(MaKhoa);
CREATE INDEX idx_lop_manganh    ON Lop(MaNganh);
CREATE INDEX idx_dc_malv    ON DeCuongLuanAn(MaLV);
CREATE INDEX idx_dc_masv    ON DeCuongLuanAn(MaSV);

CREATE INDEX idx_dk_masv   ON DangKyHocPhan(MaSV);
CREATE INDEX idx_dk_malophp ON DangKyHocPhan(MaLopHP);

CREATE INDEX idx_pc_magv   ON PhanCongGiangDay(MaGV);
CREATE INDEX idx_pc_malophp ON PhanCongGiangDay(MaLopHP);

CREATE INDEX idx_hd_malv   ON HoiDongBaoVe(MaLV);
CREATE INDEX idx_tvhd_mahd   ON ThanhVienHoiDong(MaHD);
CREATE INDEX idx_nckh_loai    ON NghienCuuKhoaHoc(LoaiCongTrinh);
CREATE INDEX idx_nckh_nam     ON NghienCuuKhoaHoc(Nam DESC);

-- Index cho bảng mới
CREATE INDEX idx_lophp_mamh ON LopHocPhan(MaMH);
CREATE INDEX idx_lophp_mahk ON LopHocPhan(MaHK);
CREATE INDEX idx_lophp_magv ON LopHocPhan(MaGV);
CREATE INDEX idx_lichhoc_mapc ON LichHoc(MaPC);
CREATE INDEX idx_lichhoc_thu ON LichHoc(Thu);
CREATE INDEX idx_lichhoc_phong ON LichHoc(PhongHoc);

-- ============================================================
-- 25. AUDIT LOG (giữ nguyên)
-- ============================================================
CREATE TABLE AuditLog (
    MaAudit    BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    UserId     VARCHAR(15),
    UserType   VARCHAR(20) CHECK (UserType IN ('admin', 'giangvien', 'sinhvien', 'system')),
    Action     VARCHAR(10) NOT NULL CHECK (Action IN ('INSERT', 'UPDATE', 'DELETE')),
    TableName  VARCHAR(50) NOT NULL,
    RecordId   VARCHAR(15),
    OldData    JSONB,
    NewData    JSONB,
    IpAddress  VARCHAR(45),
    UserAgent  VARCHAR(500),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION fn_audit_trigger() RETURNS TRIGGER AS $$
DECLARE
    pk_value TEXT;
    pk_col   TEXT := COALESCE(TG_ARGV[0], 'id');
BEGIN
    pk_value := COALESCE(
        (to_jsonb(NEW) ->> pk_col),
        (to_jsonb(OLD) ->> pk_col)
    );

    IF TG_OP = 'INSERT' THEN
        INSERT INTO AuditLog(UserId, UserType, Action, TableName, RecordId, NewData)
        VALUES (
            current_setting('app.current_user_id', TRUE),
            current_setting('app.current_user_type', TRUE),
            'INSERT',
            TG_TABLE_NAME,
            pk_value,
            to_jsonb(NEW)
        );
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO AuditLog(UserId, UserType, Action, TableName, RecordId, OldData, NewData)
        VALUES (
            current_setting('app.current_user_id', TRUE),
            current_setting('app.current_user_type', TRUE),
            'UPDATE',
            TG_TABLE_NAME,
            pk_value,
            to_jsonb(OLD),
            to_jsonb(NEW)
        );
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO AuditLog(UserId, UserType, Action, TableName, RecordId, OldData)
        VALUES (
            current_setting('app.current_user_id', TRUE),
            current_setting('app.current_user_type', TRUE),
            'DELETE',
            TG_TABLE_NAME,
            pk_value,
            to_jsonb(OLD)
        );
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Kích hoạt audit trigger cho các bảng quan trọng
CREATE TRIGGER trg_audit_sinhvien AFTER INSERT OR UPDATE OR DELETE ON SinhVien FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger('MaSV');
CREATE TRIGGER trg_audit_quantri AFTER INSERT OR UPDATE OR DELETE ON QuanTri FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger('MaAdmin');
CREATE TRIGGER trg_audit_luanvan AFTER INSERT OR UPDATE OR DELETE ON LuanVan FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger('MaLV');
CREATE TRIGGER trg_audit_hocphi AFTER INSERT OR UPDATE OR DELETE ON HocPhi FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger('MaHP');
CREATE TRIGGER trg_audit_dangky AFTER INSERT OR UPDATE OR DELETE ON DangKyHocPhan FOR EACH ROW EXECUTE FUNCTION fn_audit_trigger('MaDK');

-- ============================================================
-- KẾT THÚC SCHEMA
-- ============================================================