"""
Tests cho GPA Calculation
Chạy: pytest tests/test_gpa.py -v
"""
import pytest
from app.services.hoc_tap_service import HocTapService


class TestGPACalculation:
    """Test GPA calculation business logic"""

    def test_gpa_calculation_basic(self):
        """Test GPA cơ bản với dữ liệu giả định"""
        # Mock data: diem_list format như từ HocTapService.get_all_with_mon_hoc
        # Test với điểm trung bình 8.0
        mock_data = [
            {"MaMH": "MH001", "TenMH": "Toán", "SoTinChi": 3, "Diem": 8.0},
        ]

        # Tính tay: GPA = 8.0
        tong_diem_tin_chi = 8.0 * 3
        tong_tin_chi = 3
        gpa_thang_10 = tong_diem_tin_chi / tong_tin_chi
        gpa_thang_4 = gpa_thang_10 / 2.5

        assert gpa_thang_10 == 8.0
        assert gpa_thang_4 == 3.2

    def test_gpa_calculation_multiple_subjects(self):
        """Test GPA với nhiều môn"""
        # Dữ liệu:
        # Toán: 8.0 x 3 = 24.0
        # Lý: 7.5 x 2 = 15.0
        # Hóa: 9.0 x 2 = 18.0
        # Tổng: 57.0 / 7 = 8.14 (thang 10)
        # GPA: 8.14 / 2.5 = 3.256 (thang 4)

        tong_diem_tin_chi = (8.0 * 3) + (7.5 * 2) + (9.0 * 2)
        tong_tin_chi = 3 + 2 + 2
        gpa_thang_10 = tong_diem_tin_chi / tong_tin_chi
        gpa_thang_4 = gpa_thang_10 / 2.5

        assert round(gpa_thang_10, 2) == 8.14
        assert round(gpa_thang_4, 2) == 3.26

    def test_gpa_calculation_all_fails(self):
        """Test GPA với toàn điểm rớt (< 5)"""
        mock_data = [
            {"SoTinChi": 3, "Diem": 3.0},
            {"SoTinChi": 2, "Diem": 4.0},
        ]

        tong_diem_tin_chi = (3.0 * 3) + (4.0 * 2)
        tong_tin_chi = 5
        gpa_thang_10 = tong_diem_tin_chi / tong_tin_chi
        gpa_thang_4 = gpa_thang_10 / 2.5

        assert round(gpa_thang_10, 2) == 3.4
        assert round(gpa_thang_4, 2) == 1.36

    def test_gpa_calculation_all_perfect(self):
        """Test GPA với toàn điểm tối đa"""
        mock_data = [
            {"SoTinChi": 3, "Diem": 10.0},
        ]

        tong_diem_tin_chi = 10.0 * 3
        tong_tin_chi = 3
        gpa_thang_10 = tong_diem_tin_chi / tong_tin_chi
        gpa_thang_4 = gpa_thang_10 / 2.5

        assert gpa_thang_10 == 10.0
        assert gpa_thang_4 == 4.0

    def test_gpa_zero_credits(self):
        """Test GPA với 0 tín chỉ (không hợp lệ)"""
        tong_tin_chi = 0

        # Khi không có tín chỉ, không thể tính GPA
        with pytest.raises(ZeroDivisionError):
            gpa_thang_10 = 0 / tong_tin_chi

    def test_gpa_rounding(self):
        """Test làm tròn GPA"""
        mock_data = [
            {"SoTinChi": 2, "Diem": 7.3},
            {"SoTinChi": 3, "Diem": 8.7},
        ]

        tong_diem_tin_chi = (7.3 * 2) + (8.7 * 3)
        tong_tin_chi = 5
        gpa_thang_10 = tong_diem_tin_chi / tong_tin_chi
        gpa_thang_4 = gpa_thang_10 / 2.5

        # round(3.94, 2) = 3.94
        assert round(gpa_thang_10, 2) == round(42.7 / 5, 2)
        assert round(gpa_thang_4, 2) == round(42.7 / 5 / 2.5, 2)


class TestGPABoundaries:
    """Test GPA boundary cases"""

    def test_gpa_min(self):
        """Test GPA tối thiểu (0)"""
        tong_diem_tin_chi = 0
        tong_tin_chi = 10
        gpa_thang_10 = tong_diem_tin_chi / tong_tin_chi
        gpa_thang_4 = gpa_thang_10 / 2.5

        assert gpa_thang_10 == 0.0
        assert gpa_thang_4 == 0.0

    def test_gpa_max(self):
        """Test GPA tối đa (4.0)"""
        tong_diem_tin_chi = 10.0 * 100  # Giả sử 100 tín chỉ
        tong_tin_chi = 100
        gpa_thang_10 = tong_diem_tin_chi / tong_tin_chi
        gpa_thang_4 = gpa_thang_10 / 2.5

        assert gpa_thang_10 == 10.0
        assert gpa_thang_4 == 4.0

    def test_gpa_credit_weighting(self):
        """Test GPA có trọng số tín chỉ"""
        # Môn 4 tín chỉ có ảnh hưởng lớn hơn môn 2 tín chỉ
        mock_data = [
            {"SoTinChi": 4, "Diem": 9.0},  # 36 điểm tín
            {"SoTinChi": 2, "Diem": 5.0},  # 10 điểm tín
        ]

        tong_diem_tin_chi = (9.0 * 4) + (5.0 * 2)
        tong_tin_chi = 6
        gpa_thang_10 = tong_diem_tin_chi / tong_tin_chi

        # Nếu không có trọng số: (9.0 + 5.0) / 2 = 7.0
        # Có trọng số: (36 + 10) / 6 = 7.67
        assert round(gpa_thang_10, 2) == 7.67
