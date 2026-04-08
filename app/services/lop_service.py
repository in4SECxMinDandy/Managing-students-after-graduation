"""
Lop Service - Business logic cho Lop
"""
from app.models.lop import Lop as LopModel
from app.services.base_service import BaseService


class LopService(BaseService):
    model = LopModel

    @classmethod
    def create_with_validation(cls, ma_lop: str, ten_lop: str, ma_nganh: str, khoa_hoc: str = None) -> dict:
        """Tạo lớp với validation"""
        if cls.model.exists(ma_lop):
            return {"success": False, "message": "Mã lớp đã tồn tại"}

        # Check unique ten_lop
        existing = cls.model.where({"ten_lop": ten_lop})
        if existing:
            return {"success": False, "message": "Tên lớp đã tồn tại"}

        lop = cls.model.create({
            "ma_lop": ma_lop,
            "ten_lop": ten_lop,
            "ma_nganh": ma_nganh,
            "khoa_hoc": khoa_hoc or ""
        })
        return {"success": True, "data": lop}

    @classmethod
    def get_sinh_vien_by_lop(cls, ma_lop: str) -> list:
        """Lấy danh sách sinh viên thuộc lớp"""
        if not cls.model.exists(ma_lop):
            return {"success": False, "message": "Lớp không tồn tại"}
        return {"success": True, "data": cls.model.get_sinh_vien(ma_lop)}
