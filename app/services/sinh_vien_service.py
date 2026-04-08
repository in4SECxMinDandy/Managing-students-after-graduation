"""
SinhVien Service - Business logic cho SinhVien
"""
from datetime import date
from werkzeug.security import generate_password_hash

from app.models.sinh_vien import SinhVien as SinhVienModel
from app.services.base_service import BaseService


class SinhVienService(BaseService):
    model = SinhVienModel

    @classmethod
    def create_with_validation(cls, ma_sv: str, ho_ten: str, ngay_sinh: str,
                              email: str, mat_khau: str, ma_lop: str = None,
                              cccd: str = None, so_dien_thoai: str = None) -> dict:
        """Tạo sinh viên với validation"""
        # Validate email unique
        if SinhVienModel.find_by_email(email):
            return {"success": False, "message": "Email đã được sử dụng"}

        # Validate password min 6 chars
        if len(mat_khau) < 6:
            return {"success": False, "message": "Mật khẩu phải tối thiểu 6 ký tự"}

        sinh_vien = cls.model.create({
            "ma_sv": ma_sv,
            "ho_ten": ho_ten,
            "email": email,
            "mat_khau": generate_password_hash(mat_khau),
            "ma_lop": ma_lop,
            "cccd": cccd or "",
            "so_dien_thoai": so_dien_thoai or ""
        })

        return {"success": True, "data": sinh_vien}

    @classmethod
    def update_profile(cls, ma_sv: str, data: dict) -> dict:
        """Cập nhật thông tin sinh viên"""
        update_data = {}

        if "ho_ten" in data:
            update_data["ho_ten"] = data["ho_ten"]
        if "email" in data:
            # Check unique
            existing = SinhVienModel.find_by_email(data["email"])
            if existing and existing["ma_sv"] != ma_sv:
                return {"success": False, "message": "Email đã được sử dụng"}
            update_data["email"] = data["email"]
        if "ma_lop" in data:
            update_data["ma_lop"] = data["ma_lop"]

        if not update_data:
            return {"success": False, "message": "Không có thông tin để cập nhật"}

        sinh_vien = cls.model.update(ma_sv, update_data)
        return {"success": True, "data": sinh_vien}

    @classmethod
    def get_profile_with_details(cls, ma_sv: str) -> dict:
        """Lấy profile đầy đủ với lớp, ngành, khoa"""
        sinh_vien = cls.model.find(ma_sv)
        if not sinh_vien:
            return {"success": False, "message": "Sinh viên không tồn tại"}

        lop = cls.model.get_lop(ma_sv) if sinh_vien.get("ma_lop") else None
        nganh = None
        khoa = None
        if lop:
            from app.models.nganh import Nganh
            nganh = Nganh.get_khoa(lop["ma_nganh"])
            if nganh:
                from app.models.khoa import Khoa
                khoa = Khoa.find(nganh["ma_khoa"])

        return {
            "success": True,
            "data": {
                "sinh_vien": sinh_vien,
                "lop": lop,
                "nganh": nganh,
                "khoa": khoa
            }
        }
