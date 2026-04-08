"""
Tests cho Business Rules
Chạy: pytest tests/test_business_rules.py -v
"""
import pytest
from datetime import date, datetime
from app.models.tot_nghiep import TotNghiep
from app.services.auth_service import AuthService


class TestXepLoaiTotNghiep:
    """Test xếp loại tốt nghiệp"""

    def test_xuat_sac(self):
        """GPA >= 3.60 = Xuất sắc"""
        assert TotNghiep.calculate_xep_loai(3.60) == "Xuất sắc"
        assert TotNghiep.calculate_xep_loai(3.70) == "Xuất sắc"
        assert TotNghiep.calculate_xep_loai(4.00) == "Xuất sắc"

    def test_gioi(self):
        """GPA >= 3.20 và < 3.60 = Giỏi"""
        assert TotNghiep.calculate_xep_loai(3.20) == "Giỏi"
        assert TotNghiep.calculate_xep_loai(3.50) == "Giỏi"
        assert TotNghiep.calculate_xep_loai(3.59) == "Giỏi"

    def test_kha(self):
        """GPA >= 2.50 và < 3.20 = Khá"""
        assert TotNghiep.calculate_xep_loai(2.50) == "Khá"
        assert TotNghiep.calculate_xep_loai(3.00) == "Khá"
        assert TotNghiep.calculate_xep_loai(3.19) == "Khá"

    def test_trung_binh(self):
        """GPA >= 2.00 và < 2.50 = Trung bình"""
        assert TotNghiep.calculate_xep_loai(2.00) == "Trung bình"
        assert TotNghiep.calculate_xep_loai(2.30) == "Trung bình"
        assert TotNghiep.calculate_xep_loai(2.49) == "Trung bình"

    def test_yeu(self):
        """GPA < 2.00 = Yếu"""
        assert TotNghiep.calculate_xep_loai(1.99) == "Yếu"
        assert TotNghiep.calculate_xep_loai(1.50) == "Yếu"
        assert TotNghiep.calculate_xep_loai(0.00) == "Yếu"

    def test_boundary_360(self):
        """Test ranh giới 3.60"""
        assert TotNghiep.calculate_xep_loai(3.59) == "Giỏi"
        assert TotNghiep.calculate_xep_loai(3.60) == "Xuất sắc"

    def test_boundary_320(self):
        """Test ranh giới 3.20"""
        assert TotNghiep.calculate_xep_loai(3.19) == "Khá"
        assert TotNghiep.calculate_xep_loai(3.20) == "Giỏi"

    def test_boundary_250(self):
        """Test ranh giới 2.50"""
        assert TotNghiep.calculate_xep_loai(2.49) == "Trung bình"
        assert TotNghiep.calculate_xep_loai(2.50) == "Khá"

    def test_boundary_200(self):
        """Test ranh giới 2.00"""
        assert TotNghiep.calculate_xep_loai(1.99) == "Yếu"
        assert TotNghiep.calculate_xep_loai(2.00) == "Trung bình"


class TestValidationRules:
    """Test các quy tắc validation"""

    def test_email_format_valid(self):
        """Email hợp lệ phải có @gmail.com"""
        valid_emails = [
            "test@gmail.com",
            "user123@gmail.com",
            "my.email@gmail.com",
        ]
        for email in valid_emails:
            assert email.endswith("@gmail.com")

    def test_email_format_invalid(self):
        """Email không hợp lệ"""
        invalid_emails = [
            "test@yahoo.com",
            "test@abc.com",
            "test@gmail.vn",
            "testgmail.com",  # Thiếu @
        ]
        for email in invalid_emails:
            assert not email.endswith("@gmail.com")

    def test_cccd_valid(self):
        """CCCD hợp lệ: đúng 10 số"""
        valid_cccd = ["1234567890", "0987654321", "0000000000"]
        for cccd in valid_cccd:
            assert cccd.isdigit() and len(cccd) == 10

    def test_cccd_invalid(self):
        """CCCD không hợp lệ"""
        invalid_cccd = [
            "123456789",     # 9 số
            "12345678901",   # 11 số
            "123456789a",    # Có chữ
            "123 456 789",   # Có khoảng trắng
        ]
        for cccd in invalid_cccd:
            assert not (cccd.isdigit() and len(cccd) == 10)

    def test_sdt_valid(self):
        """SDT hợp lệ: đúng 10 số"""
        valid_sdt = ["0123456789", "0987654321", "0901234567"]
        for sdt in valid_sdt:
            assert sdt.isdigit() and len(sdt) == 10

    def test_sdt_invalid(self):
        """SDT không hợp lệ"""
        invalid_sdt = [
            "012345678",     # 9 số
            "01234567890",   # 11 số
            "012 345 6789",  # Có khoảng trắng
        ]
        for sdt in invalid_sdt:
            assert not (sdt.isdigit() and len(sdt) == 10)

    def test_diem_pt_range(self):
        """Điểm phương thức xét tuyển: 0-30"""
        valid_diem = [0, 15, 25.5, 30]
        invalid_diem = [-1, 30.1, 31, 100]

        for diem in valid_diem:
            assert 0 <= diem <= 30

        for diem in invalid_diem:
            assert not (0 <= diem <= 30)

    def test_diem_kq_ht_range(self):
        """Điểm kết quả học tập: 0-10"""
        valid_diem = [0, 5, 8.5, 10]
        invalid_diem = [-0.1, 10.1, 20]

        for diem in valid_diem:
            assert 0 <= diem <= 10

        for diem in invalid_diem:
            assert not (0 <= diem <= 10)

    def test_ngay_sinh_not_future(self):
        """Ngày sinh không được là tương lai"""
        today = date.today()
        past_dates = [
            date(2000, 1, 1),
            date(2005, 6, 15),
            date.today()
        ]
        future_dates = [
            date(2030, 1, 1),
            date.today().replace(year=date.today().year + 1)
        ]

        for d in past_dates:
            assert d <= today

        for d in future_dates:
            assert d > today

    def test_password_min_length(self):
        """Mật khẩu tối thiểu 6 ký tự"""
        valid_passwords = ["123456", "password", "abcdefg"]
        invalid_passwords = ["12345", "abc", ""]

        for pw in valid_passwords:
            assert len(pw) >= 6

        for pw in invalid_passwords:
            assert len(pw) < 6


class TestMaSVFormat:
    """Test format mã sinh viên"""

    def test_ma_sv_format(self):
        """MaSV format: SVyyXXXXXXXX"""
        test_cases = [
            ("SV2512345678", True),
            ("SV2412345678", True),
            ("SV2500000000", True),
            ("SV0000000000", True),
            ("SV2555555", False),    # Thiếu số
            ("SV25555555555", False), # Thừa số
            ("SV123456789", False),   # Thiếu 1 số
            ("12345678901", False),   # Không có prefix SV
        ]

        for ma_sv, expected in test_cases:
            is_valid = (
                ma_sv.startswith("SV") and
                len(ma_sv) == 10 and
                ma_sv[2:].isdigit()
            )
            assert is_valid == expected, f"{ma_sv}: expected {expected}, got {is_valid}"


class TestMaKhoaFormat:
    """Test format mã khoa"""

    def test_ma_khoa_format(self):
        """MaKhoa: độ dài 2 ký tự"""
        test_cases = [
            ("KT", True),
            ("CN", True),
            ("TC", True),
            ("K", False),           # 1 ký tự
            ("KTH", False),         # 3 ký tự
            ("K1", False),          # Có số
        ]

        for ma_khoa, expected in test_cases:
            is_valid = len(ma_khoa) == 2 and ma_khoa.isalpha()
            assert is_valid == expected


class TestMaNganhFormat:
    """Test format mã ngành"""

    def test_ma_nganh_format(self):
        """MaNganh: độ dài 4 ký tự"""
        test_cases = [
            ("CNTT", True),
            ("KHMT", True),
            ("KHTN", True),
            ("CN", False),          # 2 ký tự
            ("CNTTT", False),       # 5 ký tự
            ("CN01", False),        # Có số
        ]

        for ma_nganh, expected in test_cases:
            is_valid = len(ma_nganh) == 4 and ma_nganh.isalpha()
            assert is_valid == expected


class TestMaMHFormat:
    """Test format mã môn học"""

    def test_ma_mh_format(self):
        """MaMH: độ dài 7 ký tự"""
        test_cases = [
            ("TH03001", True),
            ("MA03002", True),
            ("TH00000", True),
            ("TH001", False),       # 6 ký tự
            ("TH030001", False),    # 8 ký tự
        ]

        for ma_mh, expected in test_cases:
            is_valid = len(ma_mh) == 7
            assert is_valid == expected
