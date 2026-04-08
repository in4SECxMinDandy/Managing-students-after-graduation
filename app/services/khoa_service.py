"""
Khoa Service - Business logic cho Khoa
"""
from app.models.khoa import Khoa as KhoaModel
from app.services.base_service import BaseService


class KhoaService(BaseService):
    model = KhoaModel

    @classmethod
    def create_with_validation(cls, ma_khoa: str, ten_khoa: str, mo_ta: str = None) -> dict:
        """
        Tạo khoa với validation
        - ma_khoa: độ dài 2 ký tự
        - ten_khoa: unique
        """
        if len(ma_khoa) != 2:
            return {"success": False, "message": "Mã khoa phải có 2 ký tự"}

        if cls.model.exists(ma_khoa):
            return {"success": False, "message": "Mã khoa đã tồn tại"}

        # Check unique ten_khoa
        existing = cls.model.where({"ten_khoa": ten_khoa})
        if existing:
            return {"success": False, "message": "Tên khoa đã tồn tại"}

        khoa = cls.model.create({
            "ma_khoa": ma_khoa,
            "ten_khoa": ten_khoa,
            "mo_ta": mo_ta
        })
        return {"success": True, "data": khoa}

    @classmethod
    def get_nganh_by_khoa(cls, ma_khoa: str) -> list:
        """Lấy danh sách ngành thuộc khoa"""
        if not cls.model.exists(ma_khoa):
            return {"success": False, "message": "Khoa không tồn tại"}
        return {"success": True, "data": cls.model.get_nganh(ma_khoa)}
