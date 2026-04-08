"""
Nganh Service - Business logic cho Nganh
"""
from app.models.nganh import Nganh as NganhModel
from app.services.base_service import BaseService


class NganhService(BaseService):
    model = NganhModel

    @classmethod
    def create_with_validation(cls, ma_nganh: str, ten_nganh: str, ma_khoa: str) -> dict:
        """Tạo ngành với validation"""
        if len(ma_nganh) < 2:
            return {"success": False, "message": "Mã ngành phải có ít nhất 2 ký tự"}

        if cls.model.exists(ma_nganh):
            return {"success": False, "message": "Mã ngành đã tồn tại"}

        nganh = cls.model.create({
            "ma_nganh": ma_nganh,
            "ten_nganh": ten_nganh,
            "ma_khoa": ma_khoa
        })
        return {"success": True, "data": nganh}

    @classmethod
    def get_lop_by_nganh(cls, ma_nganh: str) -> list:
        """Lấy danh sách lớp thuộc ngành"""
        if not cls.model.exists(ma_nganh):
            return {"success": False, "message": "Ngành không tồn tại"}
        return {"success": True, "data": cls.model.get_lop(ma_nganh)}
