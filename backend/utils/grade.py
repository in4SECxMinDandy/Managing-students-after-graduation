"""Grade conversion utilities."""
from decimal import Decimal


def diem_10_to_he4(diem_10: float | Decimal) -> float:
    """Convert 10-point scale to 4-point scale."""
    if diem_10 >= 8.5:
        return 4.0
    if diem_10 >= 7.0:
        return 3.0
    if diem_10 >= 5.5:
        return 2.0
    if diem_10 >= 4.0:
        return 1.0
    return 0.0


def diem_10_to_chu(diem_10: float | Decimal) -> str:
    """Convert 10-point scale to letter grade."""
    if diem_10 >= 8.5:
        return "A"
    if diem_10 >= 7.0:
        return "B"
    if diem_10 >= 5.5:
        return "C"
    if diem_10 >= 4.0:
        return "D"
    return "F"


def gpa_to_xep_loai(gpa: float) -> str:
    """Convert GPA to graduation classification."""
    if gpa >= 3.6:
        return "XuatSac"
    if gpa >= 3.2:
        return "Gioi"
    if gpa >= 2.5:
        return "Kha"
    if gpa >= 2.0:
        return "TrungBinh"
    return "Yeu"


def tinh_tong_tin_chi(diem_he4_list: list[tuple[float, int]]) -> tuple[float, int]:
    """
    Tính GPA tích lũy từ danh sách (điểm_hệ_4, số_tín_chỉ).
    Returns (GPA, tổng_tín_chỉ).
    """
    if not diem_he4_list:
        return 0.0, 0
    tong_tc = sum(tc for _, tc in diem_he4_list)
    if tong_tc == 0:
        return 0.0, 0
    tong_diem_tc = sum(diem * tc for diem, tc in diem_he4_list)
    return round(tong_diem_tc / tong_tc, 2), tong_tc
