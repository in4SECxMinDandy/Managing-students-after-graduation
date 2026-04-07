"""Tests for grade utility functions."""
import pytest
from backend.utils.grade import (
    diem_10_to_chu,
    diem_10_to_he4,
    gpa_to_xep_loai,
    tinh_tong_tin_chi,
)


class TestDiem10ToHe4:
    """Test diem_10_to_he4 conversion."""

    def test_a_plus(self):
        assert diem_10_to_he4(9.0) == 4.0

    def test_a(self):
        assert diem_10_to_he4(8.5) == 4.0

    def test_b(self):
        assert diem_10_to_he4(7.0) == 3.0
        assert diem_10_to_he4(7.9) == 3.0

    def test_c(self):
        assert diem_10_to_he4(5.5) == 2.0
        assert diem_10_to_he4(6.9) == 2.0

    def test_d(self):
        assert diem_10_to_he4(4.0) == 1.0
        assert diem_10_to_he4(5.4) == 1.0

    def test_f(self):
        assert diem_10_to_he4(0.0) == 0.0
        assert diem_10_to_he4(3.9) == 0.0


class TestDiem10ToChu:
    """Test diem_10_to_chu conversion."""

    def test_a(self):
        assert diem_10_to_chu(8.5) == "A"

    def test_b(self):
        assert diem_10_to_chu(7.0) == "B"

    def test_c(self):
        assert diem_10_to_chu(5.5) == "C"

    def test_d(self):
        assert diem_10_to_chu(4.0) == "D"

    def test_f(self):
        assert diem_10_to_chu(3.9) == "F"


class TestGpaToXepLoai:
    """Test graduation classification."""

    def test_xuat_sac(self):
        assert gpa_to_xep_loai(3.6) == "XuatSac"
        assert gpa_to_xep_loai(4.0) == "XuatSac"

    def test_gioi(self):
        assert gpa_to_xep_loai(3.2) == "Gioi"
        assert gpa_to_xep_loai(3.5) == "Gioi"

    def test_kha(self):
        assert gpa_to_xep_loai(2.5) == "Kha"
        assert gpa_to_xep_loai(3.1) == "Kha"

    def test_trung_binh(self):
        assert gpa_to_xep_loai(2.0) == "TrungBinh"
        assert gpa_to_xep_loai(2.4) == "TrungBinh"

    def test_yeu(self):
        assert gpa_to_xep_loai(0.0) == "Yeu"
        assert gpa_to_xep_loai(1.9) == "Yeu"


class TestTinhTongTinChi:
    """Test GPA and credit accumulation."""

    def test_empty(self):
        gpa, tc = tinh_tong_tin_chi([])
        assert gpa == 0.0
        assert tc == 0

    def test_single_course(self):
        gpa, tc = tinh_tong_tin_chi([(4.0, 3)])
        assert gpa == 4.0
        assert tc == 3

    def test_multiple_courses(self):
        # A(4.0, 3tc) + B(3.0, 2tc) = (4*3 + 3*2) / 5 = 18/5 = 3.6
        gpa, tc = tinh_tong_tin_chi([(4.0, 3), (3.0, 2)])
        assert tc == 5
        assert abs(gpa - 3.6) < 0.01

    def test_all_failing(self):
        # F(0, 3tc) + F(0, 2tc) = 0
        gpa, tc = tinh_tong_tin_chi([(0.0, 3), (0.0, 2)])
        assert gpa == 0.0
        assert tc == 5
