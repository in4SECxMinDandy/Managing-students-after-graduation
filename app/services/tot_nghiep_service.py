"""
TotNghiep Service - Business logic cho tốt nghiệp
"""
from app.models.tot_nghiep import TotNghiep
from app.models.sinh_vien import SinhVien
from app.services.hoc_tap_service import HocTapService


class TotNghiepService:
    """Service xử lý xét tốt nghiệp"""

    @classmethod
    def check_graduation(cls, ma_sv: str) -> dict:
        """
        Kiểm tra điều kiện tốt nghiệp
        - Tính GPA từ HocTapService
        - Tính xếp loại
        - Cập nhật bảng TotNghiep
        """
        if not SinhVien.exists(ma_sv):
            return {"success": False, "message": "Sinh viên không tồn tại"}

        # Tính GPA
        gpa_result = HocTapService.calculate_gpa(ma_sv)
        if not gpa_result["success"]:
            return gpa_result

        gpa_data = gpa_result["data"]
        gpa = gpa_data["gpa_thang_4"]

        # Tính xếp loại
        xep_loai = TotNghiep.calculate_xep_loai(gpa)

        # Cập nhật TotNghiep
        result = TotNghiep.get_or_create(ma_sv, gpa)

        return {
            "success": True,
            "data": {
                "ma_sv": ma_sv,
                "gpa_thang_10": gpa_data["gpa_thang_10"],
                "gpa_thang_4": gpa,
                "xep_loai": xep_loai,
                "tong_tin_chi": gpa_data["tong_tin_chi"],
                "so_mon": gpa_data["so_mon"],
                "tot_nghiep": result
            }
        }

    @classmethod
    def get_graduation_status(cls, ma_sv: str) -> dict:
        """Lấy trạng thái tốt nghiệp hiện tại"""
        if not SinhVien.exists(ma_sv):
            return {"success": False, "message": "Sinh viên không tồn tại"}

        tn = TotNghiep.find(ma_sv)
        if tn:
            return {
                "success": True,
                "data": {
                    "da_xet": True,
                    "gpa": float(tn["gpa"]),
                    "xep_loai": tn["xep_loai"],
                    "sinh_vien": SinhVien.find(ma_sv)
                }
            }

        # Chưa xét, tính GPA hiện tại
        gpa_result = HocTapService.calculate_gpa(ma_sv)
        if not gpa_result["success"]:
            return gpa_result

        gpa_data = gpa_result["data"]
        xep_loai = TotNghiep.calculate_xep_loai(gpa_data["gpa_thang_4"])

        return {
            "success": True,
            "data": {
                "da_xet": False,
                "gpa_thang_10_hien_tai": gpa_data["gpa_thang_10"],
                "gpa_thang_4_hien_tai": gpa_data["gpa_thang_4"],
                "xep_loai_du_kien": xep_loai,
                "tong_tin_chi": gpa_data["tong_tin_chi"],
                "so_mon": gpa_data["so_mon"]
            }
        }

    @classmethod
    def get_xep_loai_from_gpa(cls, gpa: float) -> str:
        """Helper: lấy xếp loại từ GPA"""
        return TotNghiep.calculate_xep_loai(gpa)
