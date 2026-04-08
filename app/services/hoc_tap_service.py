"""
HocTap Service - Business logic cho Kết quả học tập và GPA
"""
from app.models.kq_hoc_tap import KQHocTap
from app.models.mon_hoc import MonHoc


class HocTapService:
    """Service xử lý điểm số và tính GPA"""

    @classmethod
    def nhap_diem(cls, ma_sv: str, ma_mh: str, diem: float) -> dict:
        """
        Nhập điểm cho sinh viên
        Validation:
        - Diem: 0-10
        - SinhVien tồn tại
        - MonHoc tồn tại
        """
        if diem < 0 or diem > 10:
            return {"success": False, "message": "Điểm phải từ 0 đến 10"}

        # Check SinhVien exists
        from app.models.sinh_vien import SinhVien
        if not SinhVien.exists(ma_sv):
            return {"success": False, "message": "Sinh viên không tồn tại"}

        # Check MonHoc exists
        if not MonHoc.exists(ma_mh):
            return {"success": False, "message": "Môn học không tồn tại"}

        result = KQHocTap.upsert(ma_sv, ma_mh, diem)
        return {"success": True, "data": result}

    @classmethod
    def delete_diem(cls, ma_sv: str, ma_mh: str) -> dict:
        """Xóa điểm"""
        if KQHocTap.delete_by_sv_mh(ma_sv, ma_mh):
            return {"success": True, "message": "Xóa điểm thành công"}
        return {"success": False, "message": "Không tìm thấy điểm"}

    @classmethod
    def get_bang_diem(cls, ma_sv: str) -> dict:
        """Lấy bảng điểm đầy đủ"""
        from app.models.sinh_vien import SinhVien
        if not SinhVien.exists(ma_sv):
            return {"success": False, "message": "Sinh viên không tồn tại"}

        diem_list = KQHocTap.get_all_with_mon_hoc(ma_sv)
        return {"success": True, "data": diem_list}

    @classmethod
    def calculate_gpa(cls, ma_sv: str) -> dict:
        """
        Tính GPA theo công thức:
        GPA = (Σ(Diem × SoTinChi)) / Σ(SoTinChi) / 2.5

        Thang điểm: Thang 10 → Thang 4
        """
        from app.models.sinh_vien import SinhVien
        if not SinhVien.exists(ma_sv):
            return {"success": False, "message": "Sinh viên không tồn tại"}

        diem_list = KQHocTap.get_all_with_mon_hoc(ma_sv)

        if not diem_list:
            return {
                "success": True,
                "data": {
                    "ma_sv": ma_sv,
                    "gpa": 0.0,
                    "gpa_thang_4": 0.0,
                    "tong_diem_tin_chi": 0.0,
                    "tong_tin_chi": 0,
                    "so_mon": 0
                }
            }

        # Tính GPA
        tong_diem_tin_chi = 0.0
        tong_tin_chi = 0

        for diem in diem_list:
            tong_diem_tin_chi += float(diem["diem"]) * int(diem["so_tin_chi"])
            tong_tin_chi += int(diem["so_tin_chi"])

        if tong_tin_chi == 0:
            return {"success": False, "message": "Chưa có điểm để tính GPA"}

        # GPA thang 10
        gpa_thang_10 = tong_diem_tin_chi / tong_tin_chi
        # GPA thang 4 (quy đổi)
        gpa_thang_4 = gpa_thang_10 / 2.5

        return {
            "success": True,
            "data": {
                "ma_sv": ma_sv,
                "gpa_thang_10": round(gpa_thang_10, 2),
                "gpa_thang_4": round(gpa_thang_4, 2),
                "tong_diem_tin_chi": round(tong_diem_tin_chi, 2),
                "tong_tin_chi": tong_tin_chi,
                "so_mon": len(diem_list)
            }
        }

    @classmethod
    def nhap_nhieu_diem(cls, diem_list: list) -> dict:
        """
        Nhập nhiều điểm cùng lúc
        diem_list: [{"ma_sv": "...", "ma_mh": "...", "diem": ...}]
        """
        success_count = 0
        errors = []

        for item in diem_list:
            result = cls.nhap_diem(
                item.get("ma_sv"),
                item.get("ma_mh"),
                item.get("diem")
            )
            if result["success"]:
                success_count += 1
            else:
                errors.append({
                    "ma_sv": item.get("ma_sv"),
                    "ma_mh": item.get("ma_mh"),
                    "message": result["message"]
                })

        return {
            "success": success_count > 0,
            "success_count": success_count,
            "total": len(diem_list),
            "errors": errors
        }
